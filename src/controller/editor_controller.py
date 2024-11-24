import json
from model.class_model import Class, Field, Method
from model.editor_model import EditorEncoder
from model.relationship_model import Relationship, Type
from view.ui_cli import CLI
from view.ui_gui import GUI
from PIL import Image

# Controller for the Editor class
# Most functions return a boolean to indicate that an action
# was performed successfully, to indicate whether it should be
# saved in the Editor's action stack
#
# Such functions have been annotated with a return type
class EditorController:
    def __init__(self, ui, editor):
        self.ui = ui
        self.editor = editor
    
    def export_image(self):
        file_name = self.ui.uiChooseCanvasLocation()
        # For an empty filename (sent on GUI 'Cancel') do nothing
        if not file_name:
            return
        
        # Saves canvas as a postscript file and then uses Image  to turn it into an image
        self.ui.canvas.postscript(file='canvas.eps')
        img = Image.open('canvas.eps')
        img.convert()
        img.save(file_name + '.png', 'png')
    
    def save(self):
        filename = self.ui.uiChooseSaveLocation()
        # For an empty filename (sent on GUI 'Cancel') do nothing
        if not filename:
            # If it's the CLI, give clear output
            if isinstance(self.ui, CLI):
                self.ui.uiError(f'Could not save to `{filename}`')
            return

        output = json.dumps(self.editor, cls=EditorEncoder, indent=4)
        with open(f'{filename}', 'w') as f:
            f.write(output)
            self.ui.uiFeedback(f'Saved to {filename}!')
    
    def load(self):
        filename = self.ui.uiChooseLoadLocation()
        # For an empty filename (sent on GUI 'Cancel') do nothing
        if not filename:
            # If it's the CLI, give clear output
            if isinstance(self.ui, CLI):
                self.ui.uiError(f'Could not load from `{filename}`')
            return

        if isinstance(self.ui, GUI):
            # Suppress popups as we load from JSON
            self.ui.silent_mode = True

        with open(filename, 'r') as f:
            data = f.read()
            obj = json.loads(data)
            for clazz in obj['classes']:
                self.classAdd(clazz['name'])
                for attr in clazz['fields']:
                    self.addField(clazz['name'], attr['name'])
                for method in clazz['methods']:
                    params = []
                    for p in method['params']:
                        params.append(p['name'])
                    self.addMethod(clazz['name'], method['name'], params)
            for rel in obj['relationships']:
                self.relationshipAdd(rel['source'], rel['destination'], Type.make(rel['type'].lower()))
                        
        self.ui.uiFeedback(f'=--> Loaded from {filename}!')
        if isinstance(self.ui, GUI):
            # Recalculate grayed out buttons
            self.ui.updateAccess()
            # No longer suppress popups
            self.ui.silent_mode = False

    def saveGUI(self):
        filename = self.ui.uiChooseSaveLocation()
        # For an empty filename (sent on GUI 'Cancel') do nothing
        if not filename:
            # If it's the CLI, give clear output
            if isinstance(self.ui, CLI):
                self.ui.uiError(f'Could not save to `{filename}`')
            return
        
        # Prepare the list of classes with positions embedded as part of each class object
        classes_with_positions = []
        for class_name, class_obj in self.editor.classes.items():
            fields = [{'name': field.name} for field in class_obj.fields]  #REMEMBER TO ADD TYPES
            methods = [{'name': method.name,   #REMEMVER TO ADD RETURN TYPES AND PARAM TYPES
                        'params': [{'name': param} if isinstance(param, str) else {'name': param.name}
                                for param in method.params]}
                    for method in class_obj.methods]
            
            # Retrieve position from box_positions and add it to the class object
            position = self.ui.box_positions.get(class_name, {}).get('position', (0, 0))
            class_data = {
                'name': class_name,
                'fields': fields,
                'methods': methods,
                'position': {'x': position[0], 'y': position[1]}  # Embed position as x, y coordinates
            }
            classes_with_positions.append(class_data)

        # Collect relationship data to save
        relationships = []
        for (class1, class2), (line, shape) in self.ui.relationship_lines.items():

            relationship_type = self.editor.getRelationshipType(class1, class2)  
            if relationship_type is not None:
                relationships.append({
                    "source": class1,
                    "destination": class2,
                    "type": relationship_type.name 
                })
            else:
                print(f"Warning: Relationship between {class1} and {class2} not found in editor.")

        # Prepare the final JSON output
        output = {
            "classes": classes_with_positions,
            "relationships": relationships
        }
            
        # Write to the JSON file
        with open(f'{filename}.JSON', 'w') as f:
            json.dump(output, f, indent=4)
            self.ui.uiFeedback(f'Saved to {filename}.JSON!')

    
    def loadGUI(self):
        filename = self.ui.uiChooseLoadLocation()
        # For an empty filename (sent on GUI 'Cancel') do nothing
        if not filename:
            # If it's the CLI, give clear output
            if isinstance(self.ui, CLI):
                self.ui.uiError(f'Could not load from `{filename}`')
            return

        self.ui.silent_mode = True

        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                
                # Load classes, fields, methods, and positions
                for clazz in data['classes']:
                    name = clazz['name']
                    self.classAdd(name)

                    # Add fields
                    for attr in clazz.get('fields', []):
                        self.addField(name, attr['name'])

                    # Add methods
                    for method in clazz.get('methods', []):
                        params = [p['name'] for p in method.get('params', [])]
                        self.addMethod(name, method['name'], params)

                    # Set position if it exists
                    if 'position' in clazz:
                        x, y = clazz['position']['x'], clazz['position']['y']
                        self.ui.updateBoxPosition(name, x, y)  # Position the class box

                # Load relationships
                for rel in data['relationships']:
                    self.relationshipAdd(rel['source'], rel['destination'], Type.make(rel['type'].lower()))

                # Update relationship lines after setting box positions
                for (class1, class2), _ in self.ui.relationship_lines.items():
                    self.ui.updateRelationshipLines(class1)

                self.ui.uiFeedback(f'Loaded from {filename}!')
        finally:
            self.ui.silent_mode = False
    
    def undo(self):
        self.stepCmd(True)

    def redo(self):
        self.stepCmd(False)

    # Implementation function for Undo/Redo
    # Steps through the command stack in different directions depending on the command
    def stepCmd(self, undo: bool):
        if len(self.editor.action_stack) == 0:
            self.ui.uiError('No actions have been performed yet')
            return
        if undo:
            # We allow the action idx to go to -1 so that the very first command
            # is not skipped when doing redo
            if self.editor.action_idx > -1:
                self.editor.action_stack[self.editor.action_idx].undo(self)
                self.editor.action_idx -= 1
                if self.editor.action_idx >= 0:
                    # If we did not undo the first command, we have commands we can still undo
                    self.editor.can_undo = True
                else:
                    # If we did undo the first command, we can no longer undo
                    self.editor.can_undo = False
                # By undoing any command, we can redo
                self.editor.can_redo = True
            else:
                # If we did undo the first command, we can no longer undo
                self.editor.can_undo = False
        else:
            self.editor.action_idx += 1
            if self.editor.action_idx >= len(self.editor.action_stack):
                # If we are past the latest command, there is nothing left to redo
                self.editor.action_idx = len(self.editor.action_stack) - 1
                self.editor.can_redo = False
            else:
                self.editor.action_stack[self.editor.action_idx].execute(self)
                if self.editor.action_idx == len(self.editor.action_stack) - 1:
                    # If we just now called redo on the latest command, there is nothing left to redo
                    self.editor.can_redo = False
                else:
                    # Otherwise, there is more we can redo
                    self.editor.can_redo = True
                # By redoing any command, we can undo
                self.editor.can_undo = True
        # Recalculate grayed out buttons
        self.ui.updateAccess()
    
    def pushCmd(self, cmd):
        self.editor.pushCmd(cmd)
        self.editor.can_undo = True
        # Recalculate grayed out buttons
        self.ui.updateAccess()

    def classAdd(self, name) -> bool:
        if name in self.editor.classes:
            self.ui.uiError(f'Class {name} already exists')
            return False
        else:
            newclass = Class(name)
            self.editor.classes[name] = newclass
            self.ui.uiFeedback(f'Added class {name}!')
            self.ui.addClassBox(name)
            return True
        
    def classDelete(self, name) -> bool:
        if name in self.editor.classes:
            del self.editor.classes[name]
            # Deleting relationships that are no longer valid after class deletion
            toRemove = []
            for (src, dst) in self.editor.relationships:
                if name == src or name == dst:
                    toRemove.append((src, dst))
            for rel in toRemove:
                self.editor.relationships.discard(rel)
                
            self.ui.uiFeedback(f'Deleted class {name}!')
            self.ui.deleteClassBox(name)
            return True
        else:
            self.ui.uiError(f'No class exists with the name `{name}`')
            return False

    # Function to rename a class called 'name' to a class called 'rename'.
    def classRename(self, name, rename) -> bool:
        if name in self.editor.classes and rename not in self.editor.classes:
            clazz = self.editor.classes.pop(name)
            clazz.name = rename
            self.editor.classes[rename] = clazz
            self.ui.uiFeedback(f'Renamed class `{name}` to `{rename}`')
            self.ui.renameClassBox(name, rename)
            return True
        elif rename in self.editor.classes:
            self.ui.uiError(f'{rename} is an already existing class. Cannot rename.')
        else: 
            self.ui.uiError(f'{name} does not exist. Cannot rename.')
        return False

    # Function which adds a relationship between class1 and class2, which are both strings
    def relationshipAdd(self, class1, class2, typ):
        if isinstance(typ, str):
            typ = Type.make(typ.lower())  # Convert string to Type enum if needed
            if not typ:
                self.ui.uiError(f"Invalid relationship type: {typ}")
                return False

        if self.editor.hasRelationship(class1, class2) or self.editor.hasRelationship(class2, class1):
            self.ui.uiError(f'There is already a relationship between `{class1}` and `{class2}`')
        elif class1 not in self.editor.classes:
            self.ui.uiError(f'class `{class1}` does not exist')
        elif class2 not in self.editor.classes:
            self.ui.uiError(f'class `{class2}` does not exist')
        else:
            # Add relationship to the editor's relationships dictionary
            self.editor.relationships[(class1, class2)] = Relationship(class1, class2, typ.name)
            self.ui.uiFeedback(f'Added relationship between {class1} and {class2} of type {typ.name}!')
            
            # Draw the relationship line in the UI
            self.ui.drawRelationshipLine(class1, class2, typ.name.lower())
            return True
        return False

    # Function which deletes a relationship between class1 and class2
    def relationshipDelete(self, class1, class2):
        # Check if the relationship exists in either direction
        if (class1, class2) in self.editor.relationships:
            # Delete the relationship from the editor's dictionary
            del self.editor.relationships[(class1, class2)]
            self.ui.deleteRelationshipLine(class1, class2)
            self.ui.uiFeedback(f'Relationship between {class1} and {class2} deleted.')
            return True
        elif (class2, class1) in self.editor.relationships:
            # If the reverse relationship exists, delete it as well
            del self.editor.relationships[(class2, class1)]
            self.ui.deleteRelationshipLine(class2, class1)
            self.ui.uiFeedback(f'Relationship between {class2} and {class1} deleted.')
            return True
        else:
            self.ui.uiError(f'No relationship found between {class1} and {class2}.')
            return False

    # Function which changes the type of an existing relationship
    def relationshipEdit(self, class1, class2, new_typ):
        # Determine the correct key direction for the relationship
        rel_key = (class1, class2)
        if not self.editor.hasRelationship(class1, class2):
            rel_key = (class2, class1)
            if not self.editor.hasRelationship(class2, class1):
                self.ui.uiError(f'There is no relationship between `{class1}` and `{class2}`!')
                return False

        # Retrieve the relationship object from the dictionary
        rel = self.editor.relationships.get(rel_key)
        if not isinstance(rel, Relationship):
            self.ui.uiError(f'Invalid relationship data between `{class1}` and `{class2}`.')
            return False

        # Check if the new type is the same as the old type
        if rel.typ == new_typ:
            self.ui.uiError(f'The relationship from `{class1}` to `{class2}` is already of type {new_typ.name}')
            return False

        # Change the type of the relationship and provide feedback
        old_typ = rel.typ
        rel.typ = new_typ
        self.ui.uiFeedback(f'Changed relationship from {class1} to {class2} from {old_typ.name} to {new_typ.name}')

        # Update the UI by redrawing the relationship line with the new type
        self.ui.deleteRelationshipLine(class1, class2)
        self.ui.drawRelationshipLine(class1, class2, new_typ.name.lower())  # Pass relationship type as string

        return True
        
    # Function renames given attribute in given class if both exist and new name does not
    def renameField(self, class1, field1, field2):
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            
            if Field(field1) in item.fields:
                if Field(field2) not in item.fields:
                    self.editor.classes[class1].fields.remove(Field(field1))
                    self.editor.classes[class1].fields.append(Field(field2))
                    self.ui.uiFeedback(f'Field `{field1}` renamed to {field2}!')
                    self.ui.updateAttributesBox(class1)  # Update the UI
                    return True
                else:
                    self.ui.uiError(f'Field `{field2}` already exists in the class {class1}')
            else:
                self.ui.uiError(f'There is no field named `{field1}` in the class {class1}')
        return False

    # Function deletes given attribute from given class if both exist
    def deleteField(self, class1, field1) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            
            if Field(field1) in item.fields:
                self.editor.classes[class1].fields.remove(Field(field1))
                self.ui.uiFeedback(f'Field `{field1}` has been removed from class {class1}')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
            else:
                self.ui.uiError(f'Field `{field1}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    # Fuction will check to see if class exists, and whether the given attribute does not already exists. If both parameters pass the attribute will be added to the class #
    def addField(self, class1, field1) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Field(field1) in item.fields:
                self.ui.uiError(f'Field `{field1}` already exists in the class {class1}')
            else:
                self.editor.classes[class1].fields.append(Field(field1))
                self.ui.uiFeedback(f'Field `{field1}` has been added to class {class1}')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    # Adds a method to a class with a given list of parameters
    def addMethod(self, class1, method, params) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method) in item.methods:
                self.ui.uiError(f'Method `{method}` already exists in the class {class1}')
            else:
                self.editor.classes[class1].methods.append(Method(method, params))
                self.ui.uiFeedback(f'Method `{method}` has been added to class {class1}')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    # Deletes a method from a class regardless of the parameters
    def deleteMethod(self, class1, method) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method) in item.methods:
                self.editor.classes[class1].methods.remove(Method(method))
                self.ui.uiFeedback(f'Method `{method}` has been removed from class {class1}')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
            else:
                self.ui.uiError(f'Method `{method}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    # Renames a method from a class without changing the parameters
    def renameMethod(self, class1, method1, method2) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method1) in item.methods:
                if Method(method2) not in item.methods:
                    idx = self.editor.classes[class1].methods.index(Method(method1))
                    obj = self.editor.classes[class1].methods.pop(idx)
                    self.editor.classes[class1].methods.append(Method(method2, obj.params))
                    self.ui.uiFeedback(f'Method `{method1}` renamed to {method2}!')
                    self.ui.updateAttributesBox(class1)  # Update the UI
                    return True
                else:
                    self.ui.uiError(f'Method `{method2}` already exists in the class {class1}')
            else:
                self.ui.uiError(f'There is no method named `{method1}` in the class {class1}')
        return False
    
    # Removes a single parameter from a method
    def removeParameter(self, class1, method, param) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method) in item.methods:
                idx = self.editor.classes[class1].methods.index(Method(method))
                try:
                    self.editor.classes[class1].methods[idx].params.remove(param)
                except ValueError:
                    self.ui.uiError(f'Method {method} did not have the parameter {param}!')
                    return False
                self.ui.uiFeedback(f'Parameter `{param}` has been removed from method {method}!')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
            else:
                self.ui.uiError(f'Method `{method}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    # Removes every parameter from a method in a given class
    def clearParameters(self, class1, method) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method) in item.methods:
                idx = self.editor.classes[class1].methods.index(Method(method))
                self.editor.classes[class1].methods[idx].params.clear()
                self.ui.uiFeedback(f'Parameters have been removed from method {method}!')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
            else:
                self.ui.uiError(f'Method `{method}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    # Renames a single parameter
    def renameParameter(self, class1, method, param1, param2) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method) in item.methods:
                idx = self.editor.classes[class1].methods.index(Method(method))
                if param1 not in self.editor.classes[class1].methods[idx].params:
                    self.ui.uiError(f'Method `{method}` does not have a parameter named `{param1}`')
                    return False
                idx2 = self.editor.classes[class1].methods[idx].params.index(param1)
                self.editor.classes[class1].methods[idx].params[idx2] = param2
                self.ui.uiFeedback(f'Parameter `{param1}` has been renamed to `{param2}`!')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
            else:
                self.ui.uiError(f'Method `{method}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False
    
    # Replaces entire parameter list
    def replaceParameters(self, class1, method, params) -> bool:
        if class1 in self.editor.classes:
            item = self.editor.classes[class1]
            if Method(method) in item.methods:
                idx = self.editor.classes[class1].methods.index(Method(method))
                self.editor.classes[class1].methods[idx].params = params
                self.ui.uiFeedback(f'Parameter list has been inserted into `{method}`!')
                self.ui.updateAttributesBox(class1)  # Update the UI
                return True
            else:
                self.ui.uiError(f'Method `{method}` does not exist in class {class1}')
        else:
            self.ui.uiError(f'Class {class1} does not exist')
        return False

    def editorHelp(self):
        self.ui.displayHelp()
    
    # Helper function for listClasses and listRelationships
    def findRelationships(self, class_name):
        # Find all relationships associated with `class_name`
        related_classes = []
        for (src, dst), relationship in self.editor.relationships.items():
            # Ensure we’re checking the `Relationship` object, not a tuple
            if src == class_name or dst == class_name:
                # Check if the relationship has a valid `Type`
                if not isinstance(relationship.typ, Type):
                    self.ui.uiError(f"Invalid relationship type for relationship between {src} and {dst}")
                else:
                    # Determine direction and add to related_classes list
                    direction = (class_name == src)
                    related_classes.append((dst if direction else src, direction, relationship.typ))
        return related_classes

    def listRelationships(self, class_name):
        self.ui.listRelationships(self, class_name)

    # Function that lists all contents of a specific class
    def listClass(self, class_name):
        self.ui.listClass(self, class_name)

    # Function which lists all classes and contents of each class
    def listClasses(self):
        self.ui.listClasses(self)

