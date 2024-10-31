from . import ui_interface
from model.relationship_model import Type
from model.command_model import *

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
                case 'field':
                    self.fieldCommands(controller)
                case 'method':
                    self.methodCommands(controller)
                case 'parameter':
                    self.parameterCommands(controller)
                case 'save':
                    controller.save()
                case 'load':
                    controller.load()
                case 'undo':
                    controller.stepCmd(True)
                case 'redo':
                    controller.stepCmd(False)
                case 'list':
                    self.listCommands(controller)
                case 'help':
                    print('These are valid commands: class, relationship, field, method, parameter, save, load, undo, redo, list, switch, exit.')
                    controller.editorHelp()
                case 'exit':
                    quit = True
                    break
                case 'switch':
                    print('Switching to GUI...')
                    return 'switch_to_gui'
                case _:
                    print('error! print some help here')

    def uiQuery(self, prompt) -> str:
        text = input(f'  {prompt}')
        return text

    def classCommands(self, controller):
        command = input('  Enter Class Command: ')
        match command:
            # If command is 'add' it will prompt for a name and attempt to create a new class of that name#
            case 'add':
                name = input('  Class Name to Add: ')
                cmd = CommandClassAdd(name)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                name = input('  Class to Delete: ')
                cmd = CommandClassDelete(name)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                name = input('  Class to change: ')
                rename = input('    New name: ')
                cmd = CommandClassRename(name, rename)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')
    
    def relationshipCommands(self, controller):
        command = input('  Enter Relationship Command: ')
        match command:
            case 'add':
                class1 = input('  First Class in Relationship: ')
                class2 = input('  Second Class in Relationship: ')
                print('  Type of Relationship:')
                print(f'    {Type.Aggregate.display()}')
                print(f'    {Type.Composition.display()}')
                print(f'    {Type.Inheritance.display()}')
                print(f'    {Type.Realization.display()}')
                text = input('  Enter: ').lower()
                typ = Type.make(text)
                if typ == None:
                    self.uiError(f'Cannot determine relationship type from `{text}`')
                    return
                cmd = CommandRelationshipAdd(class1, class2, typ)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                class1 = input('  First Class in Relationship to Delete: ')
                class2 = input('  Second Class in Relationship to Delete: ')
                cmd = CommandRelationshipDelete(class1, class2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'edit':
                class1 = input('  First Class in Relationship: ')
                class2 = input('  Second Class in Relationship: ')
                print('  Type of Relationship to change to:')
                print(f'    {Type.Aggregate.display()}')
                print(f'    {Type.Composition.display()}')
                print(f'    {Type.Inheritance.display()}')
                print(f'    {Type.Realization.display()}')
                text = input('  Enter: ').lower()
                typ = Type.make(text)
                if typ == None:
                    self.uiError(f'Cannot determine relationship type from `{text}`')
                    return
                cmd = CommandRelationshipEdit(class1, class2, typ)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')
    
    def fieldCommands(self, controller):
        command = input('  Enter Field Command: ')
        match command:
            case 'add':
                class1 = input('  Class to Add Field To: ')
                field1 = input('  Field Name: ')
                cmd = CommandFieldAdd(class1, field1)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                class1 = input('  Class to delete field from: ')
                field1 = input('  Field to delete: ')
                cmd = CommandFieldDelete(class1, field1)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                class1 = input('  Class who\'s field you would like to rename: ')
                field1 = input('  Field you would like to rename: ')
                field2 = input('  Field name you would like to change to: ')
                controller.renameField(class1, field1, field2)
                cmd = CommandFieldRename(class1, field1, field2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')

    def methodCommands(self, controller):
        command = input('  Enter Method Command: ')
        match command:
            case 'add':
                class1 = input('  Class to Add Method To: ')
                method = input('  Method Name: ')
                param = 'tmp'
                params = []
                print('  Input a list of parameters in order. Enter a blank name to end the list.')
                while True:
                    param = input('    Param name (or empty for termination): ')
                    if param == '':
                        break
                    params.append(param)
                cmd = CommandMethodAdd(class1, method, params)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                class1 = input('  Class to delete method from: ')
                method = input('  Method to delete: ')
                cmd = CommandMethodDelete(class1, method)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                class1 = input('  Class who\'s method you would like to rename: ')
                method1 = input('  Method you would like to rename: ')
                method2 = input('  Method name you would like to change to: ')
                cmd = CommandMethodRename(class1, method1, method2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')

    def parameterCommands(self, controller):
        command = input('  Enter Parameter Command: ')
        match command:
            case 'remove':
                class1 = input('  Class with the desired Method: ')
                method = input('  Method to remove parameter from: ')
                param = input('  Parameter to remove: ')
                cmd = CommandParameterRemove(class1, method, param)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'clear':
                class1 = input('  Class with the desired Method: ')
                method = input('  Method to clear parameters from: ')
                cmd = CommandParameterClear(class1, method)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                class1 = input('  Class with the desired Method: ')
                method = input('  Method to clear parameters from: ')
                param1 = input('  Parameter to rename: ')
                param2 = input('  New parameter name: ')
                cmd = CommandParameterRename(class1, method, param1, param2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'change':
                class1 = input('  Class with the desired Method: ')
                method = input('  Method with parameters to change: ')
                param = 'tmp'
                params = []
                print('  Input a list of parameters in order. Enter a blank name to end the list.')
                while True:
                    param = input('    Param name (or empty for termination): ')
                    if param == '':
                        break
                    params.append(param)
                cmd = CommandParameterChange(class1, method, params)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
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
                    print('     add: Creates a typed relationship between two classes')
                    print('     delete: Deletes an existing relationship between two classes')
                    print('     edit: Edits the type of an existing relationship')
                    print()
                case 'field help':
                    print('Valid subcommands:')
                    print('     add: Creates a new field for a class')
                    print('     delete: Deletes an existing field')
                    print('     rename: Renames an existing field')
                    print()
                case 'method help':
                    print('Valid subcommands:')
                    print('     add: Creates a new method for a class')
                    print('     delete: Deletes an existing method')
                    print('     rename: Renames an existing method')
                    print()
                case 'parameter help':
                    print('Valid subcommands:')
                    print('     remove: Removes a parameter from a method')
                    print('     clear: Clears all parameters within a method')
                    print('     rename: Renames a parameter witin a method')
                    print('     change: Specifies a new list of parameters for a method')
                    print()
                case 'save help':
                    print('Saves to a JSON format')
                    print()
                case 'load help':
                    print('Loads from a JSON format')
                    print()
                case 'undo help':
                    print('Reverts the latest change in the workspace')
                    print()
                case 'redo help':
                    print('Reapplies reverted changes in the workspace')
                    print()
                case 'list help':
                    print('Valid subcommands:')
                    print('     classes: Lists all classes and their contents')
                    print('     class: Lists a specific class and its contents')
                    print('     relationships: Lists all relationships a class has with others')
                    print()
                case 'exit':
                    quit = True
                case 'switch help':
                    print('Switches to the GUI version of this program')
                    print()
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

            # First, print all fields
            if controller.editor.classes[class_name].fields:
                print('Fields:')
                for field in controller.editor.classes[class_name].fields:
                    print(f'  {field.name}')
            else:
                print('Fields: None')   

            # Then, print all methods
            if controller.editor.classes[class_name].methods:
                print('Methods:')
                for method in controller.editor.classes[class_name].methods:
                    print(f'  {method.name}(', end='')
                    for i, param in enumerate(method.params):
                        if i > 0:
                            print(', ', end='')
                        print(param, end='')
                    print(')')
            else:
                print('Methods: None')   

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
