from . import ui_interface
from model.relationship_model import Type

class CLI(ui_interface.UI):
    def uiFeedback(self, text: str):
        print(text)

    def uiError(self, text: str):
        print(f'ERROR: {text}')
        
    def uiRun(self, controller):
        print('Welcome to our Unified Modeling Language (UML) program! Please enter a valid command.')
        quit = False
        while not quit:
            command = input('Enter UML Command: ')
            command = command.strip()
            match command:
                case 'class':
                    self.classCommands(controller)
                case 'relationship':
                    self.relationshipCommands(controller)
                case 'attribute':
                    self.attributeCommands(controller)
                case 'save':
                    controller.save()
                case 'load':
                    controller.load()
                case 'list':
                    self.listCommands(controller)
                case 'help':
                    print('These are valid commands: class, relationship, attribute, save, load, list, exit.')
                    controller.editorHelp()
                case 'exit':
                    quit = True
                    break
                case _:
                    print('error! print some help here')

    def uiQuery(self, prompt) -> str:
        text = input(f'  {prompt}')
        return text

    def classCommands(self, controller):
        command = input('  Enter Class Command: ')
        match command:
            # If command is 'add' it will promt for a name and attempt to create a new class of that name#
            case 'add':
                name = input('  Class Name to Add: ')
                controller.classAdd(name)
            case 'delete':
                name = input('  Class to Delete: ')
                controller.classDelete(name)
            case 'rename':
                name = input('  Class to change: ')
                rename = input('    New name: ')
                controller.classRename(name, rename)
            case _:
                print('Print an error here')
    
    def relationshipCommands(self, controller):
        command = input('  Enter Relationship Command: ')
        match command:
            case 'add':
                class1 = input('  First Class in Relationship: ')
                class2 = input('  Second Class in Relationship: ')
                print('  Type of Relationship:')
                print('    Aggregate')
                text = input('  Enter: ').lower()
                typ = Type.make(text)
                if typ == None:
                    self.uiError(f'Cannot determine relationship type from `{text}`')
                    return
                controller.relationshipAdd(class1, class2, typ)
            case 'delete':
                class1 = input('  First Class in Relationship to Delete: ')
                class2 = input('  Second Class in Relationship to Delete: ')
                controller.relationshipDelete(class1, class2)
            case _:
                print('Print an error here')
    
    def attributeCommands(self, controller):
        command = input('  Enter Attribute Command: ')
        match command:
            case 'add':
                class1 = input('  Class to Add Attribute To: ')
                attribute1 = input('  Attribute Name: ')
                controller.addAttribute(class1, attribute1)
            case 'delete':
                class1 = input('  Class to delete attribute from: ')
                attribute1 = input('  Attribute to delete: ')
                controller.deleteAttribute(class1, attribute1)
            case 'rename':
                class1 = input('  Class who\'s attrubte you would like to rename: ')
                attribute1 = input('  Attribute you would like to rename: ')
                attribute2 = input('  Attribute name you would like to change to: ')
                controller.renameAttribute(class1, attribute1, attribute2)
            case _:
                print('Print an error here')
    
    def listCommands(self, controller):
        command = input('   Enter List Command: ')
        match command:
            case 'classes':
                controller.listClasses()
            case 'class':
                name = input('  Enter class: ')
                controller.listClass(name)
            case 'relationships':
                name = input("     Class to check relationships: ")
                controller.listRelationships(name)

    # Function that lists options and explanations for the basic commands
    # Must be implemented per UI interface
    def displayHelp(self) -> bool:
        quit = False
        while not quit:
            command = input('Enter "exit" to exit help menu or "<command> help" to get details on what actions can be done with each command: ')
            command = command.strip()
            match command:
                case 'class help':
                    print('Valid subcommands:')
                    print('     add: Creates a new class')
                    print('     delete: Deletes an existing class')
                    print('     rename: Renames an existing class')
                    print()
                case 'relationship help':
                    print('Valid subcommands:')
                    print('     add: Creates a relationship between two classes')
                    print('     delete: Deletes an existing relationship between two classes')
                    print()
                case 'attribute help':
                    print('Valid subcommands:')
                    print('     add: Creates a new attribute for a class')
                    print('     delete: Deletes an existing class attribute')
                    print('     rename: Renames an existing class attribute')
                    print()
                case 'save help':
                    print('Saves to a JSON format')
                    print()
                case 'load help':
                    print('Loads from a JSON format')
                    print()
                case 'list help':
                    print('Valid subcommands:')
                    print('     classes: Lists all classes and their contents')
                    print('     class: Lists a specific class and its contents')
                    print('     relationships: Lists all relationships a class has with others')
                    print()
                case 'exit':
                    quit = True
                case _:
                    print('error! print some help here')
                    print()
    
    # Function which lists all other classes a specific class has a relationship with
    def listRelationships(self, controller, class_name):
        # Makes sure class we are checking for exists
        if class_name in controller.editor.classes:
            print(f'Class: {class_name}')
            print('Relationships: ')

            # Find relationships that include the current class
            related_classes = controller.findRelationships(class_name)

            for relationship, direction, typ in related_classes:
                if direction == 'outgoing':
                    print(f'{class_name} ----> {relationship} ({typ.name})')
                else: 
                    print(f'{relationship} ----> {class_name} ({typ.name})')
        else:
            print(f'{class_name} does not exist.')

    # Function that lists all contents of a specific class
    def listClass(self, controller, class_name):
        if class_name in controller.editor.classes:
            print(f'Class: {class_name}')

            # First, print all attributes
            if controller.editor.classes[class_name].attributtesSets:
                print('Attributes:')
                for attribute in controller.editor.classes[class_name].attributtesSets:
                    print(f'  {attribute}')
            else:
                print('Attributes: None')   

            # Then, print all relationships
            related_classes = controller.findRelationships(class_name)

            if related_classes:
                print('Relationships: ')
                for relationship, direction, typ in related_classes:
                    if direction == 'outgoing':
                        print(f'{class_name} ----> {relationship} ({typ.name})')
                    else: 
                        print(f'{relationship} ----> {class_name} ({typ.name})')
            else:
                print('Relationships: None')

            print()

        else:
            print(f'Class "{class_name}" does not exist.')    

    # Function which lists all classes and contents of each class
    def listClasses(self, controller):
        if controller.editor.classes:
            for class_name in controller.editor.classes:
                self.listClass(controller, class_name)
        else:
            print("There are no classes yet")
