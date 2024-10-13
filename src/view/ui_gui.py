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

    def create_toolbar(self):
        # Create a dropdown for 'Classes'
        class_menu = tk.Menubutton(self.toolbar, text="Classes", relief=tk.RAISED)                          #command=self.classesCommands
        class_menu.menu = tk.Menu(class_menu, tearoff=0)
        class_menu["menu"] = class_menu.menu
        class_menu.menu.add_command(label="Add Class", command=lambda: self.controller.classCommandPrompt('add'))    #LAMBDA IS NECESSARY: button should call a user prompt. Prompt is piped into classAdd to add class
        class_menu.menu.add_command(label="Delete Class", command=lambda: self.controller.classCommandPrompt('delete'))
        class_menu.menu.add_command(label="Rename Class", command=lambda: self.controller.classCommandPrompt('rename'))
        class_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Attributes'
        attribute_menu = tk.Menubutton(self.toolbar, text="Attributes", relief=tk.RAISED)
        attribute_menu.menu = tk.Menu(attribute_menu, tearoff=0)
        attribute_menu["menu"] = attribute_menu.menu
        attribute_menu.menu.add_command(label="Add Attribute", command=lambda: self.controller.attributeCommandPrompt('add'))          #command=self.attributesCommands
        attribute_menu.menu.add_command(label="Delete Attribute", command=lambda: self.controller.attributeCommandPrompt('delete'))
        attribute_menu.menu.add_command(label="Rename Attribute", command=lambda: self.controller.attributeCommandPrompt('rename'))
        attribute_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Relationships'
        relationship_menu = tk.Menubutton(self.toolbar, text="Relationships", relief=tk.RAISED)
        relationship_menu.menu = tk.Menu(relationship_menu, tearoff=0)
        relationship_menu["menu"] = relationship_menu.menu
        relationship_menu.menu.add_command(label="Add Relationship", command=lambda: print("Add Relationship clicked"))         ##command=self.relationshipCommands
        relationship_menu.menu.add_command(label="Delete Relationship", command=lambda: print("Delete Relationship clicked"))
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

        button_save = tk.Button(self.toolbar, text="Quit", command=self.root.destroy) 
        button_save.pack(side=tk.LEFT, padx=2, pady=2)
    
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

    # Used in controller's deleteClass to visually delete class and it's attributes
    def deleteClassBox(self, class_name):
        if class_name in self.box_positions:
            box, text_class, text_attributes = self.box_positions[class_name]
            
            # Delete the class box and all associated texts (class name + attributes)
            self.canvas.delete(box)  # Delete the box itself
            self.canvas.delete(text_class)  # Delete the class name text
            for text_attr in text_attributes:  # Delete all the attribute texts
                self.canvas.delete(text_attr)
            
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


    def on_box_click(self, event, item):
        """ Called when the user clicks on a box. Store the selected item and the offset. """
        self.selected_item = item
        # Calculate offset of the mouse from the box's origin
        self.offset_x = event.x - self.canvas.coords(item)[0]
        self.offset_y = event.y - self.canvas.coords(item)[1]

    def on_box_drag(self, event, class_name):
        """ Called when the user drags a box. Update the position of the selected item and its text. """
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

    def on_box_release(self, event):
        """ Called when the user releases the mouse after dragging a box. """
        self.selected_item = None

    def uiFeedback(self, text: str):
        tk.messagebox.showinfo("Feedback", text)

    def uiError(self, text: str):
        tk.messagebox.showerror("Error", text)
    
    def uiRun(self):
        self.root.mainloop()
    
    def uiQuery(self, prompt: str) -> str:
        return tk.simpledialog.askstring("Input", prompt)
