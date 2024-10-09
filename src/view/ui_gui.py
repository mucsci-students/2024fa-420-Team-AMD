from . import ui_interface
import tkinter as tk

class GUI(ui_interface.UI):
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("UML Program")

        # Create a toolbar
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Add buttons to the toolbar
        self.create_toolbar()

    def create_toolbar(self):
        # Create a dropdown for 'Classes'
        class_menu = tk.Menubutton(self.toolbar, text="Classes", relief=tk.RAISED)
        class_menu.menu = tk.Menu(class_menu, tearoff=0)
        class_menu["menu"] = class_menu.menu
        class_menu.menu.add_command(label="Add Class", command=lambda: print("Add Class clicked"))              #command=self.classesCommands
        class_menu.menu.add_command(label="Delete Class", command=lambda: print("Delete Class clicked"))
        class_menu.menu.add_command(label="Rename Class", command=lambda: print("Rename Class clicked"))
        class_menu.pack(side=tk.LEFT, padx=2, pady=2)

        # Create a dropdown for 'Attributes'
        attribute_menu = tk.Menubutton(self.toolbar, text="Attributes", relief=tk.RAISED)
        attribute_menu.menu = tk.Menu(attribute_menu, tearoff=0)
        attribute_menu["menu"] = attribute_menu.menu
        attribute_menu.menu.add_command(label="Add Attribute", command=lambda: print("Add Attribute clicked"))          #command=self.attributesCommands
        attribute_menu.menu.add_command(label="Delete Attribute", command=lambda: print("Delete Attribute clicked"))
        attribute_menu.menu.add_command(label="Rename Attribute", command=lambda: print("Rename Attribute clicked"))
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

    def uiFeedback(self, text: str):
        tk.messagebox.showinfo("Feedback", text)

    def uiError(self, text: str):
        tk.messagebox.showerror("Error", text)
    
    def uiRun(self):
        self.root.mainloop()
    
    def uiQuery(self, prompt: str) -> str:
        return tk.simpledialog.askstring("Input", prompt)
