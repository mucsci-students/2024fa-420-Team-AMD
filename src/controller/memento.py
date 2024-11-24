import json
from model.relationship_model import Type
from model.command_model import CommandClassAdd

class Memento:
    def __init__(self, editor, ui):
       
        #Initializes the Memento with references to the editor and UI.
        #The editor holds the application's state, and the UI provides access to positions.
        
        self.editor = editor
        self.ui = ui

    def get_serialized_state(self):
        
        #Encapsulates the current state of the editor into a dictionary.
        
        # Capture classes with their fields, methods, and positions
        classes = []
        for class_name, class_obj in self.editor.classes.items():
            fields = [{'name': field.name} for field in class_obj.fields]
            methods = [{'name': method.name,
                        'params': [{'name': param} if isinstance(param, str) else {'name': param.name}
                                   for param in method.params]} 
                       for method in class_obj.methods]
            position = self.ui.box_positions.get(class_name, {}).get('position', (0, 0))
            classes.append({
                'name': class_name,
                'fields': fields,
                'methods': methods,
                'position': {'x': position[0], 'y': position[1]}
            })

        # Capture relationships
        relationships = []
        for (class1, class2), _ in self.ui.relationship_lines.items():
            relationship_type = self.editor.getRelationshipType(class1, class2)
            if relationship_type:
                relationships.append({
                    'source': class1,
                    'destination': class2,
                    'type': relationship_type.name
                })

        return {
            'classes': classes,
            'relationships': relationships
        }

    def save_to_file(self, filename):
        
        #Serializes the state and saves it to a file.
        state = self.get_serialized_state()
        with open(filename, 'w') as file:
            json.dump(state, file, indent=4)

    def load_from_file(self, filename):
        #Loads state from a file and restores it to the editor.
        # Suppress UI popups during loading
        previous_silent_mode = getattr(self.ui, 'silent_mode', False)  # Save current state
        self.ui.silent_mode = True

        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            # Clear current state
            self.editor.classes.clear()
            self.editor.relationships.clear()

            # Clear the canvas (removes all items)
            self.ui.canvas.delete("all")  # Clears all canvas elements

            # Clear any additional UI state tracking
            if hasattr(self.ui, "box_positions"):
                self.ui.box_positions.clear()
            if hasattr(self.ui, "relationship_lines"):
                self.ui.relationship_lines.clear()

            # Recreate classes
            for clazz in data.get('classes', []):
                name = clazz['name']
                self.ui.controller.classAdd(name)
                for attr in clazz.get('fields', []):
                    self.ui.controller.addField(name, attr['name'])
                for method in clazz.get('methods', []):
                    params = [p['name'] for p in method.get('params', [])]
                    self.ui.controller.addMethod(name, method['name'], params)
                if 'position' in clazz:
                    x, y = clazz['position']['x'], clazz['position']['y']
                    self.ui.updateBoxPosition(name, x, y)

            # Recreate relationships
            for rel in data.get('relationships', []):
                src, dst, typ = rel['source'], rel['destination'], Type.make(rel['type'].lower())
                self.ui.controller.relationshipAdd(src, dst, typ)

            self.ui.uiFeedback(f"Loaded from {filename}!")
        finally:
            # Restore previous silent mode
            self.ui.silent_mode = previous_silent_mode
