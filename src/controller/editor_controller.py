import json
from model.class_model import Class
from model.editor_model import EditorEncoder
from model.relationship_model import Relationship, Type

class EditorController:
    def __init__(self, ui, editor):
        self.ui = ui
        self.editor = editor
    
    def save(self):
        filename = self.ui.uiQuery('Save As (.JSON): ')

        output = json.dumps(self.editor, cls=EditorEncoder, indent=4)
        with open(f'{filename}.JSON', 'w') as f:
            f.write(output)
            self.ui.uiFeedback(f'Saved to {filename}.JSON!')
    
    def load(self):
        filename = self.ui.uiQuery('File Name to Open: ')

        with open(filename, 'r') as f:
            data = f.read()
            obj = json.loads(data)
            for name in obj['classes']:
                self.classAdd(name)
                for attr in obj['classes'][name]['attributes']:
                    self.addAttribute(name, attr)
            for rel in obj['relationships']:
                self.relationshipAdd(rel['src'], rel['dst'], Type.make(rel['type'].lower()))
                        
        self.ui.uiFeedback(f'=--> Loaded from {filename}!')

    def classAdd(self, name):
        if name in self.editor.classes:
            self.ui.uiError(f'Class {name} already exists')
        else:
            newclass = Class(name)
            self.editor.classes[name] = newclass
            self.ui.uiFeedback(f'Added class {name}!')
        
    def classDelete(self, name):
        if name in self.editor.classes:
            del self.editor.classes[name]
            # Deleting relationships that are no longer valid after class deletion
            toRemove = []
            for rel in self.editor.relationships:
                if name == rel.src or name == rel.dst:
                    toRemove.append(rel)
            for rel in toRemove:
                self.editor.relationships.discard(rel)
            self.ui.uiFeedback(f'Deleted class {name}!')
        else:
            self.ui.uiError(f'No class exists with the name `{name}`')

    # Function to rename a class called 'name' to a class called 'rename'.
    def classRename(self, name, rename):
        if name in self.editor.classes and rename not in self.editor.classes:
            self.editor.classes[rename] = self.editor.classes.pop(name)
            self.ui.uiFeedback(f'Renamed class `{name}` to `{rename}`')
        elif rename in self.editor.classes:
            self.ui.uiError(f'{rename} is an already existing class. Cannot rename.')
        else: 
            self.ui.uiError(f'{name} does not exist. Cannot rename.')

    # Function which adds a relationship between class1 and class2, which are both strings
    def relationshipAdd(self, class1, class2, typ):
        if self.editor.hasRelationship(class1, class2) or self.editor.hasRelationship(class2, class1):
            self.ui.uiError(f'There is already a relationship between `{class1}` and `{class2}`')
        elif class1 not in self.editor.classes:
            self.ui.uiError(f'class `{class1}` does not exist')
        elif class2 not in self.editor.classes:
            self.ui.uiError(f'class `{class2}` does not exist')
        else:
            # Note the extra parenthesis as we are adding a tuple to the set
            self.editor.relationships.add(Relationship(class1, class2, typ))
            self.ui.uiFeedback(f'Added relationship between {class1} and {class2} of type {typ.name}!')

    # Function which deletes a relationship between class1 and class2
    def relationshipDelete(self, class1, class2):
        if self.editor.hasRelationship(class1, class2):
            toRemove = None
            for rel in self.editor.relationships:
                if rel.src == class1 and rel.dst == class2:
                    toRemove = rel
            self.editor.relationships.remove(toRemove)
            self.ui.uiFeedback(f'Removed relationship between {class1} and {class2}!')
        elif class1 not in self.editor.classes:
            self.ui.uiError(f'class `{class1}` does not exist')
        elif class2 not in self.editor.classes:
            self.ui.uiError(f'class `{class2}` does not exist')
        else:
            self.ui.uiError(f'there is no relationship between `{class1}` and `{class2}`')

    # Function which changes the type of an existing relationship
    def relationshipEdit(self, class1, class2, new_typ):
        if self.editor.hasRelationship(class1, class2) or self.editor.hasRelationship(class2, class1):
            old_typ = None
            for rel in self.editor.relationships:
                if rel.src == class1 and rel.dst == class2:
                    if rel.typ == new_typ:
                        self.ui.uiError(f'The relationship from `{class1}` to `{class2}` was already of type {new_typ.name}')
                        return
                    old_typ = rel.typ
                    rel.typ = new_typ
            self.ui.uiFeedback(f'Changed type of {class1} and {class2}\'s relationship from {old_typ.name} to {new_typ.name}')
        elif class1 not in self.editor.classes:
            self.ui.uiError(f'Class `{class1}` does not exist')
        elif class2 not in self.editor.classes:
            self.ui.uiError(f'Class `{class2}` does not exist')
        else:
            self.ui.uiError(f'There is no relationship from {class1} to {class2}!')
    
    # Function renames given attribute in given class if both exist and new name does not
    def renameAttribute(self, class1, attribute1, attribute2):
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if attribute1 in item.attributtesSets:
                if attribute2 not in item.attributtesSets:
                    self.editor.classes[class1].attributtesSets.remove(attribute1)
                    self.editor.classes[class1].attributtesSets.add(attribute2)
                    self.ui.uiFeedback(f'Attribute `{attribute1}` renamed to {attribute2}!')
                else:
                    self.ui.uiError(f'Attribute `{attribute2}` already exists in the class {class1}')

    # Function deletes given attribute from given class if both exist
    def deleteAttribute(self, class1, attribute1):
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if attribute1 in item.attributtesSets:
                self.editor.classes[class1].attributtesSets.remove(attribute1)
                self.ui.uiFeedback(f'Attribute `{attribute1}` has been removed from class {class1}')
            else:
                self.ui.uiError(f'Attribute `{attribute1}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')

    # Fuction will check to see if class exists, and whether the given attribute does not already exists. If both parameters pass the attribute will be added to the class #
    def addAttribute(self, class1, attribute1):
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if attribute1 in item.attributtesSets:
                self.ui.uiError(f'Attribute `{attribute1}` already exists in the class {class1}')
            else:
                self.editor.classes[class1].attributtesSets.add(attribute1)
                self.ui.uiFeedback(f'Attribute `{attribute1}` has been added to class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')

    def editorHelp(self):
        self.ui.displayHelp()
    
    # Helper function for listClasses and listRelationships
    def findRelationships(self, class_name):
        related_classes = []
        for relationship in self.editor.relationships:
            if relationship.src == class_name:
                related_classes.append((relationship.dst, 'outgoing', relationship.typ))
            elif relationship.dst == class_name:
                related_classes.append((relationship.src, 'incoming', relationship.typ))
        return related_classes

    def listRelationships(self, class_name):
        self.ui.listRelationships(self, class_name)

    # Function that lists all contents of a specific class
    def listClass(self, class_name):
        self.ui.listClass(self, class_name)

    # Function which lists all classes and contents of each class
    def listClasses(self):
        self.ui.listClasses(self)
