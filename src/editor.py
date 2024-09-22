from classes import *

class Editor:
    def __init__(self):
        self.classes = {}
        self.relationships = set()
/
    def classAdd(self, name):
        if name in self.classes:
            print(f'Class {name} already exists')
        else:
            newclass = Class(name)
            self.classes[name] = newclass
            print(f'Added class {name}!')
        
    def classDelete(self, name):
        if name in self.classes:
            del self.classes[name]
            print(f'Deleted class {name}!')
        else:
            print(f'ERROR: No class exists with the name `{name}`')

    # Function to rename a class called 'name' to a class called 'rename'.
    def classRename(self, name, rename):
        if name in self.classes and rename not in self.classes:
            self.classes[rename] = self.classes.pop(name)
        elif rename in self.classes:
            print(f'ERROR: {rename} is an already existing class. Cannot rename.')
        else: 
            print(f'ERROR: {rename} does not exist. Cannot rename.')

    # Function which adds a relationship between class1 and class2, which are both strings
    def relationshipAdd(self, class1, class2):
        # We use tuples to make it simple to check for relationship existence in both orders
        if (class1, class2) in self.relationships or (class2, class1) in self.relationships:
            print(f'ERROR: There is already a relationship between `{class1}` and `{class2}`')
        elif class1 not in self.classes:
            print(f'ERROR: class `{class1}` does not exist')
        elif class2 not in self.classes:
            print(f'ERROR: class `{class2}` does not exist')
        else:
            # Note the extra parenthesis as we are adding a tuple to the set
            self.relationships.add((class1, class2))
            print(f'Added relationship between {class1} and {class2}!')

    # Function which deletes a relationship between class1 and class2
    def relationshipDelete(self, class1, class2):
        if (class1, class2) in self.relationships:
            self.relationships.remove((class1, class2))
            print(f'Removed relationship between {class1} and {class2}!')
        elif (class2, class1) in self.relationships:
            self.relationships.remove((class2, class1))
            print(f'Removed relationship between {class2} and {class1}!')
        elif class1 not in self.classes:
            print(f'ERROR: class `{class1}` does not exist')
        elif class2 not in self.classes:
            print(f'ERROR: class `{class2}` does not exist')
        else:
            print(f'ERROR: there is no relationship between `{class1}` and `{class2}`')

    # Fuction will check to see if class exists, and whether the given attribute does not already exists. If both parameters pass the attribute will be added to the class #
    def addAttribute(self, class1, attribute1):
        if class1 in self.classes:
            item = self.classes[class1]
            if attribute1 in item.attributtesSets:
                print(f'Attribute `{attribute1}` already exists in the class {class1}')
            else:
                self.classes[class1].attributtesSets.add(attribute1)
                print(f'Attribute `{attribute1}` has been added to class {class1}')
        else:
            print(f'Class {class1} does not exist')


    # Function that lists options and explanations for the basic commands
    def editorHelp(self):
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
                    return
                case _:
                    print('error! print some help here')
                    print()
    
    # Helper function for listClasses and listRelationships
    def findRelationships(self, class_name):
        related_classes = []
        for relationship in self.relationships:
            if relationship[0] == class_name:
                if relationship[1] != class_name:
                    related_classes.append(relationship[1])
            elif relationship[1] == class_name:
                if relationship[0] != class_name:
                    related_classes.append(relationship[0])
        return related_classes

    # Function which lists all other classes a specific class has a relationship with
    def listRelationships(self, class_name):
        # Makes sure class we are checking for exists
        if class_name in self.classes:
            print(f'Class: {class_name}')
            print('Relationships: ')

            # Find relationships that include the current class
            related_classes = self.findRelationships(class_name)

            for relationship in related_classes:
                print(f'{relationship} ---- {class_name}')
        else:
            print(f'{class_name} does not exist.')
