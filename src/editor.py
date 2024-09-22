class Editor:
    def __init__(self):
        self.classes = {}
        self.relationships = set()

    def classAdd(self, name):
        pass
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

    # Function that lists all contents of a specific class
    def listClass(self, class_name):
        if class_name in self.classes:
            print(f'Class: {class_name}')

            # First, print all relationships
            related_classes = self.findRelationships(class_name)

            if related_classes:
                print('Relationships: ')
                for relationship in related_classes:
                    print(f'{relationship} ---- {class_name}')
            else:
                print('Relationships: None')

            # Then, print all attributes
            if self.classes[class_name].attributes:
                print('Attributes:')
                for attribute in self.classes[class_name].attributtesSets:
                    print(f'  {attribute}')
            else:
                print('Attributes: None')            

            print()

        else:
            print(f'Class "{class_name}" does not exist.')         
