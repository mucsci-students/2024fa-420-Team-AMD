import json
from model.class_model import Class
from model.editor_model import EditorEncoder

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
                        # Relationships should save tuples of a pair of class names
                        self.relationshipAdd(rel[0], rel[1])
                        
                        self.ui.uiFeedback(f'=--> Loaded from {filename}!')

    def classAdd(self, name):
        if name in self.editor.classes:
            self.ui.uiError(f'Class {name} already exists')
        else:
            newclass = Class(name)
            self.editor.classes[name] = newclass
            self.ui.uiFeedback(f'Added class {name}!')
            self.ui.addClassBox(name)
        
    def classDelete(self, name):
        if name in self.editor.classes:
            del self.editor.classes[name]
            # Deleting relationships that are no longer valid after class deletion
            self.editor.relationships = filter(lambda x: x[0] != name and x[1] != name, self.editor.relationships)
            self.ui.uiFeedback(f'Deleted class {name}!')
            self.ui.deleteClassBox(name)
        else:
            self.ui.uiError(f'No class exists with the name `{name}`')

    # Function to rename a class called 'name' to a class called 'rename'.
    def classRename(self, name, rename):
        if name in self.editor.classes and rename not in self.editor.classes:
            self.editor.classes[rename] = self.editor.classes.pop(name)
            self.ui.uiFeedback(f'Renamed class `{name}` to `{rename}`')
            self.ui.renameClassBox(name, rename)
        elif rename in self.editor.classes:
            self.ui.uiError(f'{rename} is an already existing class. Cannot rename.')
        else: 
            self.ui.uiError(f'{name} does not exist. Cannot rename.')

    # Function which adds a relationship between class1 and class2, which are both strings
    def relationshipAdd(self, class1, class2):
        # We use tuples to make it simple to check for relationship existence in both orders
        if (class1, class2) in self.editor.relationships or (class2, class1) in self.editor.relationships:
            self.ui.uiError(f'There is already a relationship between `{class1}` and `{class2}`')
        elif class1 not in self.editor.classes:
            self.ui.uiError(f'class `{class1}` does not exist')
        elif class2 not in self.editor.classes:
            self.ui.uiError(f'class `{class2}` does not exist')
        else:
            # Note the extra parenthesis as we are adding a tuple to the set
            self.editor.relationships.add((class1, class2))
            self.ui.uiFeedback(f'Added relationship between {class1} and {class2}!')

    # Function which deletes a relationship between class1 and class2
    def relationshipDelete(self, class1, class2):
        if (class1, class2) in self.editor.relationships:
            self.editor.relationships.remove((class1, class2))
            self.ui.uiFeedback(f'Removed relationship between {class1} and {class2}!')
        elif (class2, class1) in self.editor.relationships:
            self.editor.relationships.remove((class2, class1))
            self.ui.uiFeedback(f'Removed relationship between {class2} and {class1}!')
        elif class1 not in self.editor.classes:
            self.ui.uiError(f'class `{class1}` does not exist')
        elif class2 not in self.editor.classes:
            self.ui.uiError(f'class `{class2}` does not exist')
        else:
            self.ui.uiError(f'there is no relationship between `{class1}` and `{class2}`')
    
    # Function renames given attribute in given class if both exist and new name does not
    def renameAttribute(self, class1, attribute1, attribute2):
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if attribute1 in item.attributtesSets:
                if attribute2 not in item.attributtesSets:
                    self.editor.classes[class1].attributtesSets.remove(attribute1)
                    self.editor.classes[class1].attributtesSets.add(attribute2)
                    self.ui.uiFeedback(f'Attribute `{attribute1}` renamed to {attribute2}!')
                    self.ui.updateAttributesBox(class1)
                else:
                    self.ui.uiError(f'Attribute `{attribute2}` already exists in the class {class1}')

    # Function deletes given attribute from given class if both exist
    def deleteAttribute(self, class1, attribute1):
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if attribute1 in item.attributtesSets:
                self.editor.classes[class1].attributtesSets.remove(attribute1)
                self.ui.uiFeedback(f'Attribute `{attribute1}` has been removed from class {class1}')
                self.ui.updateAttributesBox(class1)
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
                self.ui.updateAttributesBox(class1)
        else:
            self.ui.uiError(f'Class {class1} does not exist')

    def editorHelp(self):
        self.ui.displayHelp()
    
    # Helper function for listClasses and listRelationships
    def findRelationships(self, class_name):
        related_classes = []
        for relationship in self.editor.relationships:
            if relationship[0] == class_name:
                related_classes.append((relationship[1], 'outgoing'))
            elif relationship[1] == class_name:
                related_classes.append((relationship[0], 'incoming'))
        return related_classes

    def listRelationships(self, class_name):
        self.ui.listRelationships(self, class_name)

    # Function that lists all contents of a specific class
    def listClass(self, class_name):
        self.ui.listClass(self, class_name)

    # Function which lists all classes and contents of each class
    def listClasses(self):
        self.ui.listClasses(self)

    # Used in GUI to prompt the user for any class buttons
    def classCommandPrompt(self, action):
        match action:
            case 'add':
                class_name = self.ui.uiQuery("Class Name to Add:")
                if class_name:
                    self.classAdd(class_name)

            case 'delete':
                class_name = self.ui.uiQuery("Class to Delete:")
                if class_name:
                    self.classDelete(class_name)

            case 'rename':
                old_name = self.ui.uiQuery("Class to change:")
                if old_name:
                    new_name = self.ui.uiQuery("New name:")
                    if new_name:
                        self.classRename(old_name, new_name)

            case _:
                self.ui.uiError("Invalid action.")

    # Used in GUI to prompt the user for any attribute commands
    def attributeCommandPrompt(self, action):
        match action:
            case 'add':
                class_name = self.ui.uiQuery("Enter the class to add an attribute to:")
                if class_name:
                    attribute_name = self.ui.uiQuery("Enter the name of the attribute to add:")
                    if attribute_name:
                        self.addAttribute(class_name, attribute_name)

            case 'delete':
                class_name = self.ui.uiQuery("Enter the class to delete an attribute from:")
                if class_name:
                    attribute_name = self.ui.uiQuery("Enter the name of the attribute to delete:")
                    if attribute_name:
                        self.deleteAttribute(class_name, attribute_name)

            case 'rename':
                class_name = self.ui.uiQuery("Enter the class whose attribute you would like to rename:")
                if class_name:
                    old_attribute_name = self.ui.uiQuery("Enter the current name of the attribute:")
                    if old_attribute_name:
                        new_attribute_name = self.ui.uiQuery("Enter the new name of the attribute:")
                        if new_attribute_name:
                            self.renameAttribute(class_name, old_attribute_name, new_attribute_name)

            case _:
                self.ui.uiError("Invalid action.")
