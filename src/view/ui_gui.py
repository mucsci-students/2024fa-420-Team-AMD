from . import ui_interface
import tkinter as tk
from tkinter import messagebox, simpledialog

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
                    self.controller.classAdd(class_name)

            case 'delete':
                class_name = self.uiQuery("Class to Delete:")
                if class_name:
                    self.controller.classDelete(class_name)

            case 'rename':
                old_name = self.uiQuery("Class to change:")
                if old_name:
                    new_name = self.uiQuery("New name:")
                    if new_name:
                        self.controller.classRename(old_name, new_name)

            case _:
                self.uiError("Invalid action.")

    # prompt the user for any attribute commands
    def attributeCommandPrompt(self, action):
        match action:
            case 'add':
                class_name = self.uiQuery("Enter the class to add an attribute to:")
                if class_name:
                    attribute_name = self.uiQuery("Enter the name of the attribute to add:")
                    if attribute_name:
                        self.controller.addAttribute(class_name, attribute_name)

            case 'delete':
                class_name = self.uiQuery("Enter the class to delete an attribute from:")
                if class_name:
                    attribute_name = self.uiQuery("Enter the name of the attribute to delete:")
                    if attribute_name:
                        self.controller.deleteAttribute(class_name, attribute_name)

            case 'rename':
                class_name = self.uiQuery("Enter the class whose attribute you would like to rename:")
                if class_name:
                    old_attribute_name = self.uiQuery("Enter the current name of the attribute:")
                    if old_attribute_name:
                        new_attribute_name = self.uiQuery("Enter the new name of the attribute:")
                        if new_attribute_name:
                            self.controller.renameAttribute(class_name, old_attribute_name, new_attribute_name)

            case _:
                self.uiError("Invalid action.")
    
    # Prompt the user for relationship commands
    def relationshipCommandPrompt(self, action):
        match action:
            case 'add':
                class1 = self.uiQuery("First Class in Relationship: ")
                class2 = self.uiQuery("Second Class in Relationship: ")
                if class1 and class2:
                    relationship_type = self.uiQuery("Enter the relationship type (aggregation, composition, inheritance, realization):")
                    if relationship_type in ['aggregation', 'composition', 'inheritance', 'realization']:
                        # Add the relationship in the model
                        self.controller.relationshipAdd(class1, class2)
                        # Draw the relationship line on the canvas based on the type
                        self.drawRelationshipLine(class1, class2, relationship_type)
                    else:
                        self.uiError("Invalid relationship type. Valid types are: aggregation, composition, inheritance, realization.")

            case 'delete':
                class1 = self.uiQuery("First Class in Relationship to Delete: ")
                class2 = self.uiQuery("Second Class in Relationship to Delete: ")
                if class1 and class2:
                    self.controller.relationshipDelete(class1, class2)

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

        # Create a dropdown for 'Attributes'
        attribute_menu = tk.Menubutton(self.toolbar, text="Attributes", relief=tk.RAISED)
        attribute_menu.menu = tk.Menu(attribute_menu, tearoff=0)
        attribute_menu["menu"] = attribute_menu.menu
        attribute_menu.menu.add_command(label="Add Attribute", command=lambda: self.attributeCommandPrompt('add'))          #command=self.attributesCommands
        attribute_menu.menu.add_command(label="Delete Attribute", command=lambda: self.attributeCommandPrompt('delete'))
        attribute_menu.menu.add_command(label="Rename Attribute", command=lambda: self.attributeCommandPrompt('rename'))
        attribute_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Relationships'
        relationship_menu = tk.Menubutton(self.toolbar, text="Relationships", relief=tk.RAISED)
        relationship_menu.menu = tk.Menu(relationship_menu, tearoff=0)
        relationship_menu["menu"] = relationship_menu.menu
        relationship_menu.menu.add_command(label="Add Relationship", command=lambda: self.relationshipCommandPrompt('add'))         ##command=self.relationshipCommands
        relationship_menu.menu.add_command(label="Delete Relationship", command=lambda: self.relationshipCommandPrompt('delete'))
        relationship_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'List'
        list_menu = tk.Menubutton(self.toolbar, text="List", relief=tk.RAISED)
        list_menu.menu = tk.Menu(list_menu, tearoff=0)
        list_menu["menu"] = list_menu.menu
        list_menu.menu.add_command(label="List All Classes", command=lambda: print("List All Classes clicked"))
        list_menu.menu.add_command(label="List Class", command=lambda: print("List All Classes clicked"))               # self.list_class_selection function: add a dropdown option to list a specific class
        list_menu.menu.add_command(label="List Relationships", command=lambda: print("List Relationships clicked"))
        list_menu.pack(side=tk.LEFT, padx=2, pady=2)

        button_save = tk.Button(self.toolbar, text="Load", command=lambda: print("Load button clicked")) #command=self.relationshipCommands)
        button_save.pack(side=tk.LEFT, padx=2, pady=2)

        button_save = tk.Button(self.toolbar, text="Save", command=lambda: print("Save button clicked")) #command=self.relationshipCommands)
        button_save.pack(side=tk.LEFT, padx=2, pady=2)


# -------------- CLASS VISUALS START ---------------------------------------------------------------------------------------

    # Creates a new box for a class. Leaves space for attributes
    def addClassBox(self, class_name, attributes=None):
        if attributes is None:
            attributes = []

        # Calculate box dimensions
        box_width = 100
        # Height adjusts based on the number of attributes, each attribute taking 20 pixels of height
        box_height = 50 + len(attributes) * 20

        # Draw the rectangle (box) for the class and its attributes
        box = self.canvas.create_rectangle(self.next_x, self.next_y,
                                        self.next_x + box_width, self.next_y + box_height,
                                        fill="lightblue")

        # Draw the class name at the top of the box
        text_class = self.canvas.create_text(self.next_x + box_width / 2, self.next_y + 25,
                                            text=class_name, font=('Helvetica', 10, 'bold'))

        # Draw the attributes below the class name
        text_attributes = []
        for i, attribute in enumerate(attributes):
            text_y = self.next_y + 50 + i * 20  # Starting below the class name
            attr_text = self.canvas.create_text(self.next_x + box_width / 2, text_y, text=attribute)
            text_attributes.append(attr_text)

        # Store the box and texts (class name + attributes) in a dictionary
        self.box_positions[class_name] = (box, text_class, text_attributes)

        # Bind mouse events for dragging (move box and all texts together)
        self.canvas.tag_bind(box, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))
        self.canvas.tag_bind(text_class, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))  # Link text to the box
        for attr_text in text_attributes:
            self.canvas.tag_bind(attr_text, '<Button-1>', lambda event, item=box: self.on_box_click(event, item))  # Link attributes to the box

        # Drag event to move box and all related texts
        self.canvas.tag_bind(box, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))
        self.canvas.tag_bind(text_class, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))
        for attr_text in text_attributes:
            self.canvas.tag_bind(attr_text, '<B1-Motion>', lambda event, name=class_name: self.on_box_drag(event, name))

        # Release event (for all elements)
        self.canvas.tag_bind(box, '<ButtonRelease-1>', self.on_box_release)
        self.canvas.tag_bind(text_class, '<ButtonRelease-1>', self.on_box_release)
        for attr_text in text_attributes:
            self.canvas.tag_bind(attr_text, '<ButtonRelease-1>', self.on_box_release)

        # Store the position for the next box
        self.next_x += box_width + 20
        if self.next_x > self.canvas.winfo_width() - box_width:
            self.next_x = 50
            self.next_y += box_height + 20

    def deleteClassBox(self, class_name):
        if class_name in self.box_positions:
            box, text_class, text_attributes = self.box_positions[class_name]

            # Delete the class box and all associated texts (class name + attributes)
            self.canvas.delete(box)  # Delete the box itself
            self.canvas.delete(text_class)  # Delete the class name text
            for text_attr in text_attributes:  # Delete all the attribute texts
                self.canvas.delete(text_attr)

            # Remove any relationship lines connected to this class
            to_delete = []
            for (class1, class2) in self.relationship_lines.keys():
                if class1 == class_name or class2 == class_name:
                    self.canvas.delete(self.relationship_lines[(class1, class2)])
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
            box, text_class, text_attributes = self.box_positions[name]
            
            # Update the class name text
            self.canvas.itemconfig(text_class, text=rename)

            # Update the dictionary with the new name (keeping the same box and attributes)
            self.box_positions[rename] = (box, text_class, text_attributes)
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
            # Get the current class data (including attributes)
            box, text_class, text_attributes = self.box_positions[class_name]

            # Get the current attributes from the editor model
            attributes = list(self.controller.editor.classes[class_name].attributtesSets)

            # Clear the old attributes text from the canvas
            for text_attr in text_attributes:
                self.canvas.delete(text_attr)

            # Calculate new height based on the number of attributes
            box_height = 50 + len(attributes) * 20
            box_coords = self.canvas.coords(box)
            box_width = box_coords[2] - box_coords[0]

            # Resize the box to accommodate the new number of attributes
            self.canvas.coords(box, box_coords[0], box_coords[1], box_coords[0] + box_width, box_coords[1] + box_height)

            # Redraw the attributes
            text_attributes = []
            for i, attribute in enumerate(attributes):
                text_y = box_coords[1] + 50 + i * 20  # Starting below the class name
                attr_text = self.canvas.create_text(box_coords[0] + box_width / 2, text_y, text=attribute)
                text_attributes.append(attr_text)

            # Update the stored attributes in the box_positions dictionary
            self.box_positions[class_name] = (box, text_class, text_attributes)
        else:
            self.uiError(f'Class "{class_name}" does not exist.')

    # -------------------- Relationship Visuals START ----------------------------------------------------
    
    def drawRelationshipLine(self, class1, class2, relationship_type):
        # Draw a relationship line between two classes.
        if class1 in self.box_positions and class2 in self.box_positions:
            box1, _, _ = self.box_positions[class1]
            box2, _, _ = self.box_positions[class2]

            # Get the left and right centers of both boxes
            x1_right, y1_right = self.getBoxRightCenter(box1)
            x1_left, y1_left = self.getBoxLeftCenter(box1)
            x2_right, y2_right = self.getBoxRightCenter(box2)
            x2_left, y2_left = self.getBoxLeftCenter(box2)

            # Decide whether to draw from right-to-left or left-to-right based on horizontal positions
            if x1_right < x2_left:
                # class1 is to the left of class2: draw from the right side of class1 to the left side of class2
                x1, y1 = x1_right, y1_right
                x2, y2 = x2_left, y2_left
                arrow_direction = tk.LAST  # Arrow should point towards class2
            else:
                # class2 is to the left of class1: draw from the right side of class2 to the left side of class1
                x1, y1 = x2_right, y2_right
                x2, y2 = x1_left, y1_left
                arrow_direction = tk.FIRST  # Arrow should point towards class1

            # Draw the line based on the relationship type, and place the arrow/shape accordingly
            if relationship_type == 'aggregation':
                line = self.drawAggregationLine(x1, y1, x2, y2, arrow_direction)
            elif relationship_type == 'composition':
                line = self.drawCompositionLine(x1, y1, x2, y2, arrow_direction)
            elif relationship_type == 'inheritance':
                line = self.drawInheritanceLine(x1, y1, x2, y2, arrow_direction)
            elif relationship_type == 'realization':
                line = self.drawRealizationLine(x1, y1, x2, y2, arrow_direction)

            # Store the line in the relationship_lines dictionary
            self.relationship_lines[(class1, class2)] = line

    def drawAggregationLine(self, x1, y1, x2, y2, arrow_direction):
        # Draws a solid directional line with a diamond for aggregation relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow_direction)
        if arrow_direction == tk.LAST:
            self.drawDiamond(x2, y2)
        else:
            self.drawDiamond(x1, y1)
        return line

    def drawCompositionLine(self, x1, y1, x2, y2, arrow_direction):
        # Draws a solid directional line with a filled diamond for composition relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow_direction)
        if arrow_direction == tk.LAST:
            self.drawFilledDiamond(x2, y2)
        else:
            self.drawFilledDiamond(x1, y1)
        return line

    def drawInheritanceLine(self, x1, y1, x2, y2, arrow_direction):
        # Draws a solid directional line with a triangle for inheritance relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, arrow=arrow_direction)
        if arrow_direction == tk.LAST:
            self.drawTriangle(x2, y2)
        else:
            self.drawTriangle(x1, y1)
        return line

    def drawRealizationLine(self, x1, y1, x2, y2, arrow_direction):
        # Draws a dashed directional line with a triangle for realization relationship.
        line = self.canvas.create_line(x1, y1, x2, y2, dash=(4, 2), arrow=arrow_direction)
        if arrow_direction == tk.LAST:
            self.drawTriangle(x2, y2)
        else:
            self.drawTriangle(x1, y1)
        return line

    def drawDiamond(self, x2, y2):
        # Draws a diamond at the end of a line for aggregation.
        size = 10
        self.canvas.create_polygon(
            x2, y2 - size,  # Top
            x2 + size, y2,  # Right
            x2, y2 + size,  # Bottom
            x2 - size, y2,  # Left
            fill="white", outline="black"
        )

    def drawFilledDiamond(self, x2, y2):
        # Draws a diamond at the end of a line for Composition.
        size = 10
        self.canvas.create_polygon(
            x2, y2 - size,  # Top
            x2 + size, y2,  # Right
            x2, y2 + size,  # Bottom
            x2 - size, y2,  # Left
            fill="black", outline="black"
        )

    def drawTriangle(self, x2, y2):
        # Draws a triangle at the end of a line for inheritance and realization.
        size = 10
        self.canvas.create_polygon(
            x2 - size, y2,          # Tip of the triangle (left point)
            x2 + size, y2 - size,   # Top-right point
            x2 + size, y2 + size,   # Bottom-right point
            fill="white", outline="black"
        )
    
    def updateRelationshipLines(self, class_name):
        # Update all lines connected to a specific class when the class box moves.
        related_classes = self.controller.findRelationships(class_name)

        # Update the lines for each related class
        for related_class, direction, relationship_type in related_classes:
            if (class_name, related_class) in self.relationship_lines:
                self.canvas.delete(self.relationship_lines[(class_name, related_class)])
                self.drawRelationshipLine(class_name, related_class, relationship_type)
            elif (related_class, class_name) in self.relationship_lines:
                self.canvas.delete(self.relationship_lines[(related_class, class_name)])
                self.drawRelationshipLine(related_class, class_name, relationship_type)

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
            box, text_class, text_attributes = self.box_positions[class_name]
            box_coords = self.canvas.coords(box)
            box_width = box_coords[2] - box_coords[0]
            box_height = box_coords[3] - box_coords[1]

            # Move the box
            self.canvas.coords(box, x, y, x + box_width, y + box_height)

            # Move the class name text
            self.canvas.coords(text_class, x + box_width / 2, y + 25)

            # Move each attribute text
            for i, text_attr in enumerate(text_attributes):
                text_y = y + 50 + i * 20  # Adjust the Y position for each attribute
                self.canvas.coords(text_attr, x + box_width / 2, text_y)

            # Continuously update the relationship lines as the box moves
            self.updateRelationshipLines(class_name)

    def on_box_release(self, event):
        # Called when the user releases the mouse after dragging a box
        self.selected_item = None

    # -------------- DIAGNOSTIC FUNCTIONS START ----------------------------------------------------------------

    def uiFeedback(self, text: str):
        tk.messagebox.showinfo("Feedback", text)

    def uiError(self, text: str):
        tk.messagebox.showerror("Error", text)
    
    def uiRun(self):
        self.root.mainloop()
    
    def uiQuery(self, prompt: str) -> str:
        return tk.simpledialog.askstring("Input", prompt)