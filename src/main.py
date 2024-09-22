from editor import *
from classes import *

def classCommands(editor):
    command = input('  Enter Class Command: ')
    match command:
        case 'add':
            pass
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
            pass
        case 'delete':
            pass
        case 'rename':
            pass
        case _:
            print('Print an error here')

def listCommands(editor):
    command = input('   Enter List Command: ')
    match command:
        case 'classes':
            pass
        case 'class':
            pass
        case 'relationships':
            name = input("     Class to check relationships: ")
            editor.listRelationships(name)

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
                pass
            case 'load':
                pass
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
