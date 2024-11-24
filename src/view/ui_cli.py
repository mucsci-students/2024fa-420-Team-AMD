import prompt_toolkit

from . import ui_interface
from model.relationship_model import Type
from model.command_model import *
from .singleton import Singleton

# Class that will hold the list of words that the command line
# can auto complete to. This is only relevant to the CLI so
# the code lives here for now.
@Singleton
class Completions(prompt_toolkit.completion.Completer):
    def __init__(self):
        self.tab_completions = []

    def get_tab_completions(self):
        return self.tab_completions

    def set_tab_completions(self, lst):
        self.tab_completions = lst
    
    def class_completions(self, controller):
        self.set_tab_completions(controller.editor.getClasses())

    def field_completions(self, controller, class_name):
        if class_name in controller.editor.classes:
            class1 = controller.editor.classes[class_name]
            fields = [f.name for f in class1.fields]
            self.set_tab_completions(fields)
        else:
            self.set_tab_completions([])

    def method_completions(self, controller, class_name):
        if class_name in controller.editor.classes:
            class1 = controller.editor.classes[class_name]
            methods = [m.name for m in class1.methods]
            self.set_tab_completions(methods)
        else:
            self.set_tab_completions([])

    def param_completions(self, controller, class_name, method_name):
        if class_name in controller.editor.classes:
            class1 = controller.editor.classes[class_name]
            if Method(method_name) in class1.methods:
                idx = class1.methods.index(Method(method_name))
                method = class1.methods[idx]
                self.set_tab_completions(method.params)
            else:
                self.set_tab_completions([])
        else:
            self.set_tab_completions([])
    
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor
        matches = [option for option in self.tab_completions if option.startswith(text)]
        for m in matches:
            yield prompt_toolkit.completion.Completion(m, -len(text))
    
    # Similar to python's `input()` except it automatically manages tab completions
    def tab_input(self, prompt) -> str:
        session = prompt_toolkit.PromptSession(prompt, completer=self, complete_while_typing=False)
        text = session.prompt()
        return text

class CLI(ui_interface.UI):
    def uiFeedback(self, text: str):
        print(text)

    def uiError(self, text: str):
        print(f'ERROR: {text}')

    def uiChooseSaveLocation(self) -> str:
        filename = self.uiQuery('Save As (Saves to JSON format): ')
        return filename

    def uiChooseLoadLocation(self) -> str:
        filename = self.uiQuery('File Name to Open: ')
        return filename
        
    def uiRun(self, controller):
        print('Welcome to our Unified Modeling Language (UML) program! Please enter a valid command.')
        
        # This is not an amazing solution, have to repeat changes
        tab_commands = ['class', 'relationship', 'field', 'method', 'parameter', 'save', 'load', 'undo', 'redo', 'list', 'help', 'exit', 'switch']
        quit = False
        while not quit:
            Completions.instance().set_tab_completions(tab_commands)

            command = Completions.instance().tab_input('Enter UML Command: ')

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
                    controller.undo()
                case 'redo':
                    controller.redo()
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
        Completions.instance().set_tab_completions(['add', 'delete', 'rename'])

        command = Completions.instance().tab_input('  Enter Class Command: ')
        match command:
            # If command is 'add' it will prompt for a name and attempt to create a new class of that name#
            case 'add':
                name = input('  Class Name to Add: ')
                cmd = CommandClassAdd(name)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                Completions.instance().class_completions(controller)
                name = Completions.instance().tab_input('  Class to Delete: ')
                cmd = CommandClassDelete(name)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                Completions.instance().class_completions(controller)
                name = Completions.instance().tab_input('  Class to change: ')
                rename = input('    New name: ')
                cmd = CommandClassRename(name, rename)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')
    
    def relationshipCommands(self, controller):
        Completions.instance().set_tab_completions(['add', 'delete', 'edit'])

        command = Completions.instance().tab_input('  Enter Relationship Command: ')
        match command:
            case 'add':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  First Class in Relationship: ')
                class2 = Completions.instance().tab_input('  Second Class in Relationship: ')
                print('  Type of Relationship:')
                print(f'    {Type.Aggregate.display()}')
                print(f'    {Type.Composition.display()}')
                print(f'    {Type.Inheritance.display()}')
                print(f'    {Type.Realization.display()}')

                Completions.instance().set_tab_completions(Type.tab_completions())
                text = Completions.instance().tab_input('  Enter: ').lower()
                typ = Type.make(text)
                if typ == None:
                    self.uiError(f'Cannot determine relationship type from `{text}`')
                    return
                cmd = CommandRelationshipAdd(class1, class2, typ)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  First Class in Relationship to Delete: ')
                class2 = Completions.instance().tab_input('  Second Class in Relationship to Delete: ')
                cmd = CommandRelationshipDelete(class1, class2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'edit':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  First Class in Relationship: ')
                class2 = Completions.instance().tab_input('  Second Class in Relationship: ')
                print('  Type of Relationship to change to:')
                print(f'    {Type.Aggregate.display()}')
                print(f'    {Type.Composition.display()}')
                print(f'    {Type.Inheritance.display()}')
                print(f'    {Type.Realization.display()}')
                Completions.instance().set_tab_completions(Type.tab_completions())
                text = Completions.instance().tab_input('  Enter: ').lower()
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
        Completions.instance().set_tab_completions(['add', 'delete', 'rename'])

        command = Completions.instance().tab_input('  Enter Field Command: ')
        match command:
            case 'add':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class to Add Field To: ')
                field1 = input('  Field Name: ')
                cmd = CommandFieldAdd(class1, field1)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'delete':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class to delete field from: ')

                Completions.instance().field_completions(controller, class1)
                field1 = Completions.instance().tab_input('  Field to delete: ')

                cmd = CommandFieldDelete(class1, field1)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class who\'s field you would like to rename: ')

                Completions.instance().field_completions(controller, class1)
                field1 = Completions.instance().tab_input('  Field you would like to rename: ')
                field2 = input('  Field name you would like to change to: ')

                cmd = CommandFieldRename(class1, field1, field2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')

    def methodCommands(self, controller):
        Completions.instance().set_tab_completions(['add', 'delete', 'rename'])

        command = Completions.instance().tab_input('  Enter Method Command: ')
        match command:
            case 'add':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class to Add Method To: ')
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
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class to delete method from: ')

                Completions.instance().method_completions(controller, class1)
                method = Completions.instance().tab_input('  Method to delete: ')

                cmd = CommandMethodDelete(class1, method)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class who\'s method you would like to rename: ')

                Completions.instance().method_completions(controller, class1)
                method1 = Completions.instance().tab_input('  Method you would like to rename: ')
                method2 = input('  Method name you would like to change to: ')
                cmd = CommandMethodRename(class1, method1, method2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case _:
                print('Print an error here')

    def parameterCommands(self, controller):
        Completions.instance().set_tab_completions(['remove', 'clear', 'rename', 'change'])

        command = Completions.instance().tab_input('  Enter Parameter Command: ')
        match command:
            case 'remove':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class with the desired Method: ')

                Completions.instance().method_completions(controller, class1)
                method = Completions.instance().tab_input('  Method to remove parameter from: ')

                Completions.instance().param_completions(controller, class1, method)
                param = Completions.instance().tab_input('  Parameter to remove: ')

                cmd = CommandParameterRemove(class1, method, param)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'clear':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class with the desired Method: ')

                Completions.instance().method_completions(controller, class1)
                method = Completions.instance().tab_input('  Method to clear parameters from: ')

                cmd = CommandParameterClear(class1, method)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'rename':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class with the desired Method: ')

                Completions.instance().method_completions(controller, class1)
                method = Completions.instance().tab_input('  Method to clear parameters from: ')

                Completions.instance().param_completions(controller, class1, method)
                param1 = Completions.instance().tab_input('  Parameter to rename: ')

                param2 = input('  New parameter name: ')
                cmd = CommandParameterRename(class1, method, param1, param2)
                cmd.execute(controller)
                controller.editor.pushCmd(cmd)
            case 'change':
                Completions.instance().class_completions(controller)
                class1 = Completions.instance().tab_input('  Class with the desired Method: ')

                Completions.instance().method_completions(controller, class1)
                method = Completions.instance().tab_input('  Method with parameters to change: ')
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
        Completions.instance().set_tab_completions(['classes', 'class', 'relationships'])

        command = Completions.instance().tab_input('  Enter List Command: ')
        match command:
            case 'classes':
                controller.listClasses()
            case 'class':
                Completions.instance().class_completions(controller)
                name = Completions.instance().tab_input('  Enter class: ')
                controller.listClass(name)
            case 'relationships':
                Completions.instance().class_completions(controller)
                name = Completions.instance().tab_input("     Class to check relationships: ")
                controller.listRelationships(name)

    # Function that lists options and explanations for the basic commands
    # Must be implemented per UI interface
    def displayHelp(self) -> bool:
        quit = False
        while not quit:
            Completions.instance().set_tab_completions(
                [
                    'class help',
                    'relationship help',
                    'field help',
                    'method help',
                    'parameter help',
                    'save help',
                    'load help',
                    'undo help',
                    'redo help',
                    'list help',
                    'exit',
                    'switch',
                ]
            )

            command = Completions.instance().tab_input('Enter "exit" to exit help menu or "<command> help" to get details on what actions can be done with each command: ')
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
