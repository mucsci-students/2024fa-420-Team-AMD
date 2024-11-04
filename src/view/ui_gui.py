from . import ui_interface
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from model.relationship_model import Type
from model.class_model import Field, Method
from model.command_model import *
import json
import math

class GUI(ui_interface.UI):
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("UML Program")

        # Create a toolbar
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Create a canvas where class boxes will be drawn
        self.canvas = tk.Canvas(self.root, bg="white", width=600, height=400)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add buttons to the toolbar
        self.create_toolbar()

        # Track positions for placing boxes on the canvas
        self.box_positions = {}
        self.next_x, self.next_y = 50, 50  # Initial position for the first box

        # Variable to track the selected item for dragging
        self.selected_item = None
        self.offset_x = 0
        self.offset_y = 0

        self.relationship_lines = {}

    # --------------------- USER PROMPTS CODE ------------------------------------------------------

    # prompt the user for any class buttons
    def classCommandPrompt(self, action):
        match action:
            case 'add':
                class_name = self.uiQuery("Class Name to Add:")
                if class_name:
                    cmd = CommandClassAdd(class_name)
                    cmd.execute(self.controller)
                    self.controller.editor.pushCmd(cmd)

            case 'delete':
                class_name = self.uiQuery("Class to Delete:")
                if class_name:
                    cmd = CommandClassDelete(class_name)
                    cmd.execute(self.controller)
                    self.controller.editor.pushCmd(cmd)

            case 'rename':
                old_name = self.uiQuery("Class to change:")
                if old_name:
                    new_name = self.uiQuery("New name:")
                    if new_name:
                        cmd = CommandClassRename(old_name, new_name)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case _:
                self.uiError("Invalid action.")

    # prompt the user for any attribute commands (Now managing Fields)
    def fieldsCommandPrompt(self, action):
        match action:
            case 'add':
                class_name = self.uiQuery("Class to add Field to:")
                if class_name:
                    field_name = self.uiQuery("Field name:")
                    if field_name:
                        cmd = CommandFieldAdd(class_name, field_name)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case 'delete':
                class_name = self.uiQuery("Class to delete field from:")
                if class_name:
                    field_name = self.uiQuery("Field to delete:")
                    if field_name:
                        cmd = CommandFieldDelete(class_name, field_name)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case 'rename':
                class_name = self.uiQuery("Class who's field you would like to rename:")
                if class_name:
                    old_field_name = self.uiQuery("Field you would like to rename:")
                    if old_field_name:
                        new_field_name = self.uiQuery("Field name you would like to change to:")
                        if new_field_name:
                            cmd = CommandFieldRename(class_name, old_field_name, new_field_name)
                            cmd.execute(self.controller)
                            self.controller.editor.pushCmd(cmd)

            case _:
                self.uiError("Invalid action.")

    # prompt the user for method commands
    def methodCommandPrompt(self, action):
        match action:
            case 'add':
                class_name = self.uiQuery("Class to add Method to:")
                if class_name:
                    method_name = self.uiQuery("Method name:")
                    if method_name:
                        params = self.uiQuery("Input a list of parameters in order (comma separated):")
                        # We use this lambda to strip all leading whitespace, which the user will most
                        # definitely enter in anyway
                        param_list = list(map(lambda s: s.strip(), params.split(","))) if params else []
                        cmd = CommandMethodAdd(class_name, method_name, param_list)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case 'delete':
                class_name = self.uiQuery("Class to Delete method from:")
                if class_name:
                    method_name = self.uiQuery("Method to delete:")
                    if method_name:
                        cmd = CommandMethodDelete(class_name, method_name)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case 'rename':
                class_name = self.uiQuery("Class who's method you would like to rename:")
                if class_name:
                    old_method_name = self.uiQuery("Method you would like to rename:")
                    if old_method_name:
                        new_method_name = self.uiQuery("Method name you would like to change to:")
                        if new_method_name:
                            cmd = CommandMethodRename(class_name, old_method_name, new_method_name)
                            cmd.execute(self.controller)
                            self.controller.editor.pushCmd(cmd)

            case _:
                self.uiError("Invalid action.")         

    # Prompt the user for parameter commands
    def parameterCommandPrompt(self, action):
        match action:
            case 'remove':
                class_name = self.uiQuery("Class with the desired Method:")
                method_name = self.uiQuery("Method to remove parameter from:")
                if class_name and method_name:
                    param_name = self.uiQuery("Parameter to remove:")
                    if param_name:
                        cmd = CommandParameterRemove(class_name, method_name, param_name)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case 'clear':
                class_name = self.uiQuery("Class with the desired method:")
                method_name = self.uiQuery("Method to clear parameters from:")
                if class_name and method_name:
                    cmd = CommandParameterClear(class_name, method_name)
                    cmd.execute(self.controller)
                    self.controller.editor.pushCmd(cmd)

            case 'rename':
                class_name = self.uiQuery("Class with the desired method:")
                method_name = self.uiQuery("Method to clear parameters from:")
                if class_name and method_name:
                    old_param_name = self.uiQuery("Parameter to rename:")
                    new_param_name = self.uiQuery("New parameter name:")
                    if old_param_name and new_param_name:
                        cmd = CommandParameterRename(class_name, method_name, old_param_name, new_param_name)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)

            case 'change':
                class_name = self.uiQuery("Class with the desired method:")
                method_name = self.uiQuery("Method with parameters to change:")
                if class_name and method_name:
                    param_list = self.uiQuery("Input a list of parameters in order (comma-separated):").split(",")
                    cmd = CommandParameterChange(class_name, method_name, [param.strip() for param in param_list])
                    cmd.execute(self.controller)
                    self.controller.editor.pushCmd(cmd)

            case _:
                self.uiError("Invalid action.")        

    # Prompt the user for relationship commands
    def relationshipCommandPrompt(self, action):
        match action:
            case 'add':
                class1 = self.uiQuery("First Class in Relationship: ")
                class2 = self.uiQuery("Second Class in Relationship: ")

                if class1 and class2:
                    # Prompt for the relationship type
                    relationship_type = self.uiQuery("Enter relationship type (aggregate, composition, inheritance, realization): ")

                    # Validate the relationship type using Type.make
                    relationship_type_enum = Type.make(relationship_type)
                    if relationship_type_enum:
                        cmd = CommandRelationshipAdd(class1, class2, relationship_type_enum)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)
                    else:
                        self.uiError(f'Invalid relationship type: {relationship_type}')
            case 'delete':
                class1 = self.uiQuery("First Class in Relationship to Delete: ")
                class2 = self.uiQuery("Second Class in Relationship to Delete: ")
                if class1 and class2:
                    cmd = CommandRelationshipDelete(class1, class2)
                    cmd.execute(self.controller)
                    self.controller.editor.pushCmd(cmd)
            case 'edit':
                class1 = self.uiQuery("First Class in Relationship: ")
                class2 = self.uiQuery("Second Class in Relationship: ")

                if class1 and class2:
                    # Prompt for the relationship type
                    relationship_type = self.uiQuery("Enter relationship type (aggregate, composition, inheritance, realization): ")

                    # Validate the relationship type using Type.make
                    relationship_type_enum = Type.make(relationship_type)
                    if relationship_type_enum:
                        cmd = CommandRelationshipEdit(class1, class2, relationship_type_enum)
                        cmd.execute(self.controller)
                        self.controller.editor.pushCmd(cmd)
                    else:
                        self.uiError(f'Invalid relationship type: {relationship_type}')
            case _:
                self.uiError("Invalid action.")
    
    # ------------------- END OF USER PROMPT FUNCTIONS ------------------------------------------------------------


    # ------------------ CREATING INTERFACE TOOLBAR AND BUTTONS ---------------------------------------------------

    def create_toolbar(self):
        # Create a dropdown for 'Classes'
        class_menu = tk.Menubutton(self.toolbar, text="Classes", relief=tk.RAISED)                          #command=self.classesCommands
        class_menu.menu = tk.Menu(class_menu, tearoff=0)
        class_menu["menu"] = class_menu.menu
        class_menu.menu.add_command(label="Add Class", command=lambda: self.classCommandPrompt('add'))    #LAMBDA IS NECESSARY: button should call a user prompt. Prompt is piped into classAdd to add class
        class_menu.menu.add_command(label="Delete Class", command=lambda: self.classCommandPrompt('delete'))
        class_menu.menu.add_command(label="Rename Class", command=lambda: self.classCommandPrompt('rename'))
        class_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Fields'
        field_menu = tk.Menubutton(self.toolbar, text="Fields", relief=tk.RAISED)
        field_menu.menu = tk.Menu(field_menu, tearoff=0)
        field_menu["menu"] = field_menu.menu
        field_menu.menu.add_command(label="Add Field", command=lambda: self.fieldsCommandPrompt('add'))
        field_menu.menu.add_command(label="Delete Field", command=lambda: self.fieldsCommandPrompt('delete'))
        field_menu.menu.add_command(label="Rename Field", command=lambda: self.fieldsCommandPrompt('rename'))
        field_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Methods'
        method_menu = tk.Menubutton(self.toolbar, text="Methods", relief=tk.RAISED)
        method_menu.menu = tk.Menu(method_menu, tearoff=0)
        method_menu["menu"] = method_menu.menu
        method_menu.menu.add_command(label="Add Method", command=lambda: self.methodCommandPrompt('add'))
        method_menu.menu.add_command(label="Delete Method", command=lambda: self.methodCommandPrompt('delete'))
        method_menu.menu.add_command(label="Rename Method", command=lambda: self.methodCommandPrompt('rename'))
        method_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Parameters'
        param_menu = tk.Menubutton(self.toolbar, text="Parameters", relief=tk.RAISED)
        param_menu.menu = tk.Menu(param_menu, tearoff=0)
        param_menu["menu"] = param_menu.menu
        param_menu.menu.add_command(label="Remove Parameter", command=lambda: self.parameterCommandPrompt('remove'))
        param_menu.menu.add_command(label="Clear Parameter", command=lambda: self.parameterCommandPrompt('clear'))
        param_menu.menu.add_command(label="Rename Parameter", command=lambda: self.parameterCommandPrompt('rename'))
        param_menu.menu.add_command(label="Change Parameter", command=lambda: self.parameterCommandPrompt('change'))
        param_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Relationships'
        relationship_menu = tk.Menubutton(self.toolbar, text="Relationships", relief=tk.RAISED)
        relationship_menu.menu = tk.Menu(relationship_menu, tearoff=0)
        relationship_menu["menu"] = relationship_menu.menu
        relationship_menu.menu.add_command(label="Add Relationship", command=lambda: self.relationshipCommandPrompt('add'))         ##command=self.relationshipCommands
        relationship_menu.menu.add_command(label="Delete Relationship", command=lambda: self.relationshipCommandPrompt('delete'))
        relationship_menu.menu.add_command(label="Edit Relationship", command=lambda: self.relationshipCommandPrompt('edit'))
        relationship_menu.pack(side=tk.LEFT, padx=2, pady=2)

        button_save = tk.Button(self.toolbar, text="Save", command=lambda: self.controller.save()) #command=self.relationshipCommands)
        button_save.pack(side=tk.LEFT, padx=2, pady=2)

        button_save = tk.Button(self.toolbar, text="Load", command=lambda: self.controller.load()) #command=self.relationshipCommands)
        button_save.pack(side=tk.LEFT, padx=2, pady=2)

        button_save = tk.Button(self.toolbar, text="Help", command=lambda: self.showHelp()) #command=self.relationshipCommands)
        button_save.pack(side=tk.LEFT, padx=2, pady=2)

        button_undo = tk.Button(self.toolbar, text="Undo", command=lambda: self.controller.stepCmd(True))
        button_undo.pack(side=tk.LEFT, padx=2, pady=2)

        button_undo = tk.Button(self.toolbar, text="Redo", command=lambda: self.controller.stepCmd(False))
        button_undo.pack(side=tk.LEFT, padx=2, pady=2)


# -------------- CLASS VISUALS START ---------------------------------------------------------------------------------------

    # Creates a new box for a class. Leaves space for fields
    def addClassBox(self, class_name, fields=None, methods=None):
        if fields is None:
            fields = []

        if methods is None:
            methods = []

        # Calculate box dimensions
        box_width = 150
        # Height adjusts based on the number of attributes, each attribute taking 20 pixels of height
        box_height = 50 + (len(fields) + len(methods)) * 20

        # Draw the rectangle (box) for the class and its attributes
        box = self.canvas.create_rectangle(self.next_x, self.next_y,
                                        self.next_x + box_width, self.next_y + box_height,
                                        fill="lightblue")

        # Draw the class name at the top of the box
        text_class = self.canvas.create_text(self.next_x + box_width / 2, self.next_y + 25,
                                            text=class_name, font=('Helvetica', 10, 'bold'))

        # Draw the fields below the class name
        text_fields = []
        for i, field in enumerate(fields):
            text_y = self.next_y + 50 + i * 20  # Starting below the class name
            field_text = self.canvas.create_text(self.next_x + box_width / 2, text_y, text=f"Field: {field.name}")
            text_fields.append(field_text)

        # Draw the methods and parameters below the fields
        text_methods = []
        for i, method in enumerate(methods):
            method_params = ', '.join(method.params)
            text_y = self.next_y + 50 + (len(fields) + i) * 20  # Starting below the fields
            method_text = self.canvas.create_text(self.next_x + box_width / 2, text_y,
                                                text=f"Method: {method.name}({method_params})")
            text_methods.append(method_text)

        # Store the box and texts (class name + attributes) in a dictionary
        self.box_positions[class_name] = (box, text_class, text_fields, text_methods)

        # Bind mouse events for dragging (move box and all texts together)
        self.canvas.tag_bind(box, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))
        self.canvas.tag_bind(text_class, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))  # Link text to the box
        for text_field in text_fields:
            self.canvas.tag_bind(text_field, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))  # Link fields to the box
        for text_method in text_methods:
            self.canvas.tag_bind(text_method, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))  # Link methods to the box

        # Drag event to move box and all related texts
        self.canvas.tag_bind(box, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))
        self.canvas.tag_bind(text_class, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))
        for text_field in text_fields:
            self.canvas.tag_bind(text_field, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))
        for text_method in text_methods:
            self.canvas.tag_bind(text_method, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))

        # Release event (for all elements)
        self.canvas.tag_bind(box, '<ButtonRelease-1>', self.on_box_release)
        self.canvas.tag_bind(text_class, '<ButtonRelease-1>', self.on_box_release)
        for text_field in text_fields:
            self.canvas.tag_bind(text_field, '<ButtonRelease-1>', self.on_box_release)
        for text_method in text_methods:
            self.canvas.tag_bind(text_method, '<ButtonRelease-1>', self.on_box_release)

        # Store the position for the next box
        self.next_x += box_width + 20
        if self.next_x > self.canvas.winfo_width() - box_width:
            self.next_x = 50
            self.next_y += box_height + 20

    def deleteClassBox(self, class_name):
        if class_name in self.box_positions:
            box, text_class, text_fields, text_methods = self.box_positions[class_name]

            # Delete the class box and all associated texts (class name + fields + methods)
            self.canvas.delete(box)  # Delete the box itself
            self.canvas.delete(text_class)  # Delete the class name text
            for text_field in text_fields:  # Delete all the fields text
                self.canvas.delete(text_field)
            for text_method in text_methods:  # Delete all the fields text
                self.canvas.delete(text_method)

            # Remove any relationship lines connected to this class
            to_delete = []
            for (class1, class2) in self.relationship_lines.keys():
                if class1 == class_name or class2 == class_name:
                    self.deleteRelationshipLine(class1, class2)
                    to_delete.append((class1, class2))
            
            for key in to_delete:
                del self.relationship_lines[key]

            # Remove the class from the dictionary
            del self.box_positions[class_name]
            self.uiFeedback(f'Class "{class_name}" deleted.')
        else:
            self.uiError(f'Class "{class_name}" does not exist.')

    # Used in controller's renameClass to change class name
    def renameClassBox(self, name, rename):
        if name in self.box_positions:
            box, text_class, text_attributes, text_methods = self.box_positions[name]
            
            # Update the class name text
            self.canvas.itemconfig(text_class, text=rename)

            # Update the dictionary with the new name (keeping the same box and attributes)
            self.box_positions[rename] = (box, text_class, text_attributes, text_methods)
            del self.box_positions[name]  # Remove the old entry
            
            # Reapply the event bindings to the new name
            self.canvas.tag_bind(box, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))
            self.canvas.tag_bind(text_class, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))
            for text_attr in text_attributes:
                self.canvas.tag_bind(text_attr, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))
            
            self.canvas.tag_bind(box, '<B1-Motion>', lambda event, class_name=rename: self.on_box_drag(event, class_name))
            self.canvas.tag_bind(text_class, '<B1-Motion>', lambda event, class_name=rename: self.on_box_drag(event, class_name))
            for text_attr in text_attributes:
                self.canvas.tag_bind(text_attr, '<B1-Motion>', lambda event, class_name=rename: self.on_box_drag(event, class_name))

            self.canvas.tag_bind(box, '<ButtonRelease-1>', self.on_box_release)
            self.canvas.tag_bind(text_class, '<ButtonRelease-1>', self.on_box_release)
            for text_attr in text_attributes:
                self.canvas.tag_bind(text_attr, '<ButtonRelease-1>', self.on_box_release)

            self.uiFeedback(f'Class "{name}" renamed to "{rename}".')
        else:
            self.uiError(f'Class "{name}" does not exist.')

    # -------------------- ATTRIBUTE VISUALS START ---------------------------------------------------------------------------

    # Redraw the class box and attributes in the canvas after changes.
    def updateAttributesBox(self, class_name):
        if class_name in self.box_positions:
            # Get the current class data (including fields and methods)
            box, text_class, text_fields, text_methods = self.box_positions[class_name]

            # Get the current fields and methods from the editor model
            fields = self.controller.editor.classes[class_name].fields
            methods = self.controller.editor.classes[class_name].methods

            # Clear the old fields and methods text from the canvas
            for text_field in text_fields:
                self.canvas.delete(text_field)
            for text_method in text_methods:
                self.canvas.delete(text_method)

            # Calculate new height based on the number of fields and methods
            box_height = 50 + (len(fields) + len(methods)) * 20
            box_coords = self.canvas.coords(box)
            box_width = box_coords[2] - box_coords[0]

            # Resize the box to accommodate the new number of fields and methods
            self.canvas.coords(box, box_coords[0], box_coords[1], box_coords[0] + box_width, box_coords[1] + box_height)

            # Redraw the fields and methods
            text_fields = []
            for i, field in enumerate(fields):
                text_y = box_coords[1] + 50 + i * 20  # Starting below the class name
                field_text = self.canvas.create_text(box_coords[0] + box_width / 2, text_y, text=f"Field: {field.name}")
                text_fields.append(field_text)

            text_methods = []
            for i, method in enumerate(methods):
                method_params = ', '.join(method.params)
                text_y = box_coords[1] + 50 + (len(fields) + i) * 20  # Starting below the fields
                method_text = self.canvas.create_text(box_coords[0] + box_width / 2, text_y,
                                                    text=f"Method: {method.name}({method_params})")
                text_methods.append(method_text)

            # Update the stored fields and methods in the box_positions dictionary
            self.box_positions[class_name] = (box, text_class, text_fields, text_methods)
        else:
            self.uiError(f'Class "{class_name}" does not exist.')

    # -------------------- Relationship Visuals START ----------------------------------------------------
    
    def drawRelationshipLine(self, class1, class2, relationship_type):
        # Ensure the relationship_type is converted from string to Type if necessary

        if isinstance(relationship_type, str):
            relationship_type = Type.make(relationship_type)
            if not relationship_type:
                self.uiError(f"Invalid relationship type: {relationship_type}")
                return
            
        # Draws a relationship line between two classes.
        if class1 in self.box_positions and class2 in self.box_positions:
            box1, _, _, _ = self.box_positions[class1]
            box2, _, _, _ = self.box_positions[class2]

            # Get the left and right centers of both boxes
            x1_right, y1_right = self.getBoxRightCenter(box1)
            x1_left, y1_left = self.getBoxLeftCenter(box1)
            x2_right, y2_right = self.getBoxRightCenter(box2)
            x2_left, y2_left = self.getBoxLeftCenter(box2)

            # Decide whether to draw from right-to-left or left-to-right based on horizontal positions
            if x1_right < x2_left:
                # class1 is to the left of class2: draw from the right side of class1 to the left side of class2
                x1, y1 = x1_right, y1_right
                x2, y2 = (x2_left - 10), y2_left
                arrow_direction = tk.LAST  # Arrow should point towards class2
            else:
                # class2 is to the left of class1: draw from the right side of class2 to the left side of class1
                x1, y1 = (x2_right + 10), y2_right
                x2, y2 = x1_left, y1_left
                arrow_direction = tk.FIRST  # Arrow should point towards class1

            angle = self.compute_angle(x1, y1, x2, y2)
            extension = 10  # Extend the line into the shape

            # Extend the endpoint of the line to go into the shape
            x2_extended = x2 + extension * math.cos(angle)
            y2_extended = y2 + extension * math.sin(angle)

            # Draw the line with the appropriate style
            if relationship_type == Type.Realization:
                # Dotted line for realization
                line = self.canvas.create_line(x1, y1, x2_extended, y2_extended, dash=(4, 2), arrow=arrow_direction)
            else:
                # Solid line for other types
                line = self.canvas.create_line(x1, y1, x2_extended, y2_extended, arrow=arrow_direction)

            # Draw the shape at the actual endpoint
            if relationship_type == Type.Aggregate:
                shape = self.drawDiamond(x2, y2, angle) if arrow_direction == tk.LAST else self.drawDiamond(x1, y1, angle)
            elif relationship_type == Type.Composition:
                shape = self.drawFilledDiamond(x2, y2, angle) if arrow_direction == tk.LAST else self.drawFilledDiamond(x1, y1, angle)
            elif relationship_type == Type.Inheritance:
                flip = (arrow_direction == tk.LAST and x1 < x2) or (arrow_direction == tk.FIRST and x1 > x2)
                shape = self.drawTriangle(x2, y2, angle, flip) if arrow_direction == tk.LAST else self.drawTriangle(x1, y1, angle, flip)
            elif relationship_type == Type.Realization:
                flip = (arrow_direction == tk.LAST and x1 < x2) or (arrow_direction == tk.FIRST and x1 > x2)
                shape = self.drawTriangle(x2, y2, angle, flip) if arrow_direction == tk.LAST else self.drawTriangle(x1, y1, angle, flip)
            else:
                self.uiError(f"Invalid relationship type: {relationship_type}")
                return

            self.relationship_lines[(class1, class2)] = (line, shape)

    # Removes the relationship line and its shape (diamond, triangle)
    def deleteRelationshipLine(self, class1, class2):
        if (class1, class2) in self.relationship_lines:
            line, shape = self.relationship_lines[(class1, class2)]
            self.canvas.delete(line)
            self.canvas.delete(shape)
            del self.relationship_lines[(class1, class2)]
        elif (class2, class1) in self.relationship_lines:
            line, shape = self.relationship_lines[(class2, class1)]
            self.canvas.delete(line)
            self.canvas.delete(shape)
            del self.relationship_lines[(class2, class1)]

    def drawAggregationLine(self, x1, y1, x2, y2, arrow_direction, angle):
        # Draws a solid directional line with a diamond for aggregation relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow_direction)
        shape = self.drawDiamond(x2, y2, angle) if arrow_direction == tk.LAST else self.drawDiamond(x1, y1, angle)
        return line, shape

    def drawCompositionLine(self, x1, y1, x2, y2, arrow_direction, angle):
        # Draws a solid directional line with a filled diamond for composition relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow_direction)
        shape = self.drawFilledDiamond(x2, y2, angle) if arrow_direction == tk.LAST else self.drawFilledDiamond(x1, y1, angle)
        return line, shape

    def drawInheritanceLine(self, x1, y1, x2, y2, arrow_direction, angle):
        # Draws a solid directional line with a triangle for inheritance relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow_direction)
        # Determine if the triangle needs to be flipped
        flip = (arrow_direction == tk.LAST and x1 < x2) or (arrow_direction == tk.FIRST and x1 > x2)
        shape = self.drawTriangle(x2, y2, angle, flip) if arrow_direction == tk.LAST else self.drawTriangle(x1, y1, angle, flip)
        return line, shape

    def drawRealizationLine(self, x1, y1, x2, y2, arrow_direction, angle):
        # Draws a dashed directional line with a triangle for realization relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, dash=(4, 2), arrow=arrow_direction)
        # Determine if the triangle needs to be flipped
        flip = (arrow_direction == tk.LAST and x1 < x2) or (arrow_direction == tk.FIRST and x1 > x2)
        shape = self.drawTriangle(x2, y2, angle, flip) if arrow_direction == tk.LAST else self.drawTriangle(x1, y1, angle, flip)
        return line, shape

    def compute_angle(self, x1, y1, x2, y2):
        return math.atan2(y2 - y1, x2 - x1)

    def drawDiamond(self, x2, y2, angle):
        # Draws a diamond at the end of a line for aggregation.
        size = 17
        half_size = size / 2

        # Calculate the corners of the diamond based on fixed offsets
        diamond = self.canvas.create_polygon(
            x2 + half_size * math.cos(angle), y2 + half_size * math.sin(angle),         # Right point
            x2 - half_size * math.sin(angle), y2 + half_size * math.cos(angle),         # Top point
            x2 - half_size * math.cos(angle), y2 - half_size * math.sin(angle),         # Left point
            x2 + half_size * math.sin(angle), y2 - half_size * math.cos(angle),         # Bottom point
            fill="white", outline="black"
        )

        return diamond

    def drawFilledDiamond(self, x2, y2, angle):
        # Draws a diamond at the end of a line for composition.
        size = 17
        half_size = size / 2

        # Calculate the corners of the diamond based on fixed offsets
        filled_diamond = self.canvas.create_polygon(
            x2 + half_size * math.cos(angle), y2 + half_size * math.sin(angle),         # Right point
            x2 - half_size * math.sin(angle), y2 + half_size * math.cos(angle),         # Top point
            x2 - half_size * math.cos(angle), y2 - half_size * math.sin(angle),         # Left point
            x2 + half_size * math.sin(angle), y2 - half_size * math.cos(angle),         # Bottom point
            fill="black", outline="black"
        )

        return filled_diamond

    def drawTriangle(self, x2, y2, angle, flip=False):
        # Draws a triangle at the end of a line for inheritance and realization.
        size = 10
        dx, dy = size * math.cos(angle), size * math.sin(angle)
        if not flip:
            # Triangle pointing in the opposite direction
            triangle = self.canvas.create_polygon(
                x2 - dx, y2 - dy,         # Tip of the triangle (flipped direction)
                x2 + dy, y2 - dx,         # Base left
                x2 - dy, y2 + dx,         # Base right
                fill="white", outline="black"
            )
        else:
            # Triangle pointing in the direction of the line
            triangle = self.canvas.create_polygon(
                x2 + dx, y2 + dy,         # Tip of the triangle
                x2 - dy, y2 + dx,         # Base left
                x2 + dy, y2 - dx,         # Base right
                fill="white", outline="black"
            )
        
        return triangle
    
    def updateRelationshipLines(self, class_name):
        # Get the relationships associated with the class
        related_classes = self.controller.findRelationships(class_name)

        # Loop through the related classes
        for related_class, direction, relationship_type in related_classes:
            # Convert the relationship type string back to Type before updating, if needed
            if isinstance(relationship_type, str):
                relationship_type = Type.make(relationship_type)
                if not relationship_type:
                    self.uiError(f"Invalid relationship type: {relationship_type}")
                    continue

            # Delete and redraw the visual lines for each relationship
            if (class_name, related_class) in self.relationship_lines:
                # Delete the existing visual line and shape
                line, shape = self.relationship_lines[(class_name, related_class)]
                self.canvas.delete(line)
                self.canvas.delete(shape)

                # Redraw the relationship line
                self.drawRelationshipLine(class_name, related_class, relationship_type)

            elif (related_class, class_name) in self.relationship_lines:
                # Delete the existing visual line and shape for the inverse direction
                line, shape = self.relationship_lines[(related_class, class_name)]
                self.canvas.delete(line)
                self.canvas.delete(shape)

                # Redraw the relationship line
                self.drawRelationshipLine(related_class, class_name, relationship_type)

    # ------------------- HELP BUTTON FUNCTION ------------------------------------------------------------

    def showHelp(self):
        # Create a new top-level window for help
        help_window = tk.Toplevel(self.root)
        help_window.title("Help")
        
        # Create a scrollable text box for displaying help information
        text = tk.Text(help_window, wrap="word", height=25, width=80)
        text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(help_window, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        
        # Add the help content
        help_content = """
    Class Commands:
        add: Creates a new class
        delete: Deletes an existing class
        rename: Renames an existing class

    Relationship Commands:
        add: Creates a typed relationship between two classes
        delete: Deletes an existing relationship between two classes
        edit: Edits the type of an existing relationship

    Field Commands:
        add: Creates a new field for a class
        delete: Deletes an existing field
        rename: Renames an existing field

    Method Commands:
        add: Creates a new method for a class
        delete: Deletes an existing method
        rename: Renames an existing method

    Parameter Commands:
        remove: Removes a parameter from a method
        clear: Clears all parameters within a method
        rename: Renames a parameter within a method
        change: Specifies a new list of parameters for a method

    Save Command:
        Saves to a JSON format

    Load Command:
        Loads from a JSON format
        """

        # Insert the help content into the text box
        text.insert(tk.END, help_content)

        # Make the text box read-only
        text.config(state=tk.DISABLED)

    # ------------------- BOX VISUALS AND MOVEMENT FUNCTIONS START ----------------------------------------------------

    def getBoxLeftCenter(self, box):
        # Returns the left border center coordinates of a box.
        coords = self.canvas.coords(box)
        x_left = coords[0]  # The x-coordinate of the left border
        y_center = (coords[1] + coords[3]) / 2  # The y-coordinate of the vertical center
        return x_left, y_center
    
    def getBoxRightCenter(self, box):
        # Returns the left border center coordinates of a box.
        coords = self.canvas.coords(box)
        x_left = coords[2]  # The x-coordinate of the left border
        y_center = (coords[1] + coords[3]) / 2  # The y-coordinate of the vertical center
        return x_left, y_center

    def on_box_click(self, event, item):
        # Called when the user clicks on a box. Store the selected item and the offset
        self.selected_item = item
        self.offset_x = event.x - self.canvas.coords(item)[0]
        self.offset_y = event.y - self.canvas.coords(item)[1]

    def on_box_drag(self, event, class_name):
        # Called when the user drags a box. Update the position of the selected item and its text.
        if self.selected_item:
            x = event.x - self.offset_x
            y = event.y - self.offset_y

            # Move the box
            box, text_class, text_fields, text_methods = self.box_positions[class_name]
            box_coords = self.canvas.coords(box)
            box_width = box_coords[2] - box_coords[0]
            box_height = box_coords[3] - box_coords[1]

            # Move the box
            self.canvas.coords(box, x, y, x + box_width, y + box_height)

            # Move the class name text
            self.canvas.coords(text_class, x + box_width / 2, y + 25)

            # Move each field text
            for i, text_field in enumerate(text_fields):
                text_y = y + 50 + i * 20  # Adjust the Y position for each attribute
                self.canvas.coords(text_field, x + box_width / 2, text_y)

            # Move each method text
            for i, text_method in enumerate(text_methods):
                text_y = y + 50 + (len(text_fields) + i) * 20  # Adjust the Y position for each method
                self.canvas.coords(text_method, x + box_width / 2, text_y)

            # Continuously update the relationship lines as the box moves
            if class_name:
                self.updateRelationshipLines(class_name)

    def on_box_release(self, event):
        # Called when the user releases the mouse after dragging a box
        if self.selected_item:
            class_name = None
            # Find the class name associated with the selected item
            for name, (box, _, _, _) in self.box_positions.items():
                if box == self.selected_item:
                    class_name = name
                    break

            # Update the relationship lines connected to the moved box
            if class_name:
                self.updateRelationshipLines(class_name)
            
            self.selected_item = None

    # -------------- DIAGNOSTIC FUNCTIONS START ----------------------------------------------------------------

    def uiChooseSaveLocation(self) -> str:
        filename = tk.filedialog.asksaveasfilename(title="Select a File", filetypes=[("JSON files", "*.JSON")])
        return filename

    def uiChooseLoadLocation(self) -> str:
        filename = tk.filedialog.askopenfilename(title="Select a File", filetypes=[("JSON files", "*.JSON")])
        return filename

    def uiFeedback(self, text: str):
        tk.messagebox.showinfo("Feedback", text)

    def uiError(self, text: str):
        tk.messagebox.showerror("Error", text)
    
    def uiRun(self):
        self.root.mainloop()
    
    def uiQuery(self, prompt: str) -> str:
        return tk.simpledialog.askstring("Input", prompt)
