import json
from editor import *
from classes import *

def classCommands(editor):
    command = input('  Enter Class Command: ')
    match command:
        # If command is 'add' it will promt for a name and attempt to create a new class of that name#
        case 'add':
            name = input('  Class Name to Add: ')
            editor.classAdd(name)
        case 'delete':
            name = input('  Class to Delete: ')
            editor.classDelete(name)
        case 'rename':
            name = input('  Class to change: ')
            rename = input('    New name: ')
            editor.classRename(name, rename)
        case _:
            print('Print an error here')

def relationshipCommands(editor):
    command = input('  Enter Relationship Command: ')
    match command:
        case 'add':
            class1 = input('  First Class in Relationship: ')
            class2 = input('  Second Class in Relationship: ')
            editor.relationshipAdd(class1, class2)
        case 'delete':
            class1 = input('  First Class in Relationship to Delete: ')
            class2 = input('  Second Class in Relationship to Delete: ')
            editor.relationshipDelete(class1, class2)
            pass
        case _:
            print('Print an error here')

def attributeCommands(editor):
    command = input('  Enter Attribute Command: ')
    match command:
        case 'add':
            class1 = input('  Class to Add Attribute To: ')
            attribute1 = input('  Attribute Name: ')
            editor.addAttribute(class1, attribute1)
        case 'delete':
            class1 = input('  Class to delete attribute from: ')
            attribute1 = input('  Attribute to delete: ')
            editor.deleteAttribute(class1, attribute1)
        case 'rename':
            class1 = input('  Class who\'s attrubte you would like to rename: ')
            attribute1 = input('  Attribute you would like to rename: ')
            attribute2 = input('  Attribute name you would like to change to: ')
            editor.renameAttribute(class1, attribute1, attribute2)
        case _:
            print('Print an error here')

def listCommands(editor):
    command = input('   Enter List Command: ')
    match command:
        case 'classes':
            editor.listClasses()
        case 'class':
            name = input('  Enter class: ')
            editor.listClass(name)
        case 'relationships':
            name = input("     Class to check relationships: ")
            editor.listRelationships(name)

class EditorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Editor):
            return {'classes': editor.classes, 'relationships': list(editor.relationships)}
        if isinstance(obj, Class):
            return {'name': obj.name, 'attributes': list(obj.attributtesSets)}
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    print('Welcome to our Unified Modeling Language (UML) program! Please enter a valid command.')
    editor = Editor()
    quit = False
    while not quit:
        command = input('Enter UML Command: ')
        command = command.strip()
        match command:
            case 'class':
                classCommands(editor)
            case 'relationship':
                relationshipCommands(editor)
            case 'attribute':
                attributeCommands(editor)
            case 'save':
                filename = input('  Save As (.JSON): ')

                output = json.dumps(editor, cls=EditorEncoder, indent=4)
                with open(f'{filename}.JSON', 'w') as f:
                    f.write(output)
                print(f'Saved to {filename}.JSON!')
            case 'load':
                filename = input('  File Name to Open: ')

                with open(filename, 'r') as f:
                    data = f.read()
                    obj = json.loads(data)
                    for name in obj['classes']:
                        editor.classAdd(name)
                        for attr in obj['classes'][name]['attributes']:
                            editor.addAttribute(name, attr)
                    for rel in obj['relationships']:
                        # Relationships should save tuples of a pair of class names
                        editor.relationshipAdd(rel[0], rel[1])
                        
                print(f'=--> Loaded from {filename}!')
            case 'list':
                listCommands(editor)
            case 'help':
                print('These are valid commands: class, relationship, attribute, save, load, list, exit.')
                editor.editorHelp()
            case 'exit':
                quit = True
                break
            case _:
                print('error! print some help here')
