from editor import *

def classCommands(editor):
    command = input('  Enter Class Command: ')
    match command:
        # If command is 'add' it will promt for a name and attempt to create a new class of that name#
        case 'add':
            name = input('  Enter class name  ')
            classAdd(name)
        case 'delete':
            pass
        case 'rename':
            pass
        case _:
            print('Print an error here')

def relationshipCommands(editor):
    command = input('  Enter Relationship Command: ')
    match command:
        case 'add':
            pass
        case 'delete':
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

if __name__ == '__main__':
    editor = Editor()
    quit = False
    while not quit:
        command = input('Enter UML Command: ')
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
                pass
            case 'help':
                pass
            case 'exit':
                pass
            case _:
                print('error! print some help here')
