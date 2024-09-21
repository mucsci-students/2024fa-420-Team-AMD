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
    
    # Fuction will check to see if class exists, and whether the given attribute does not already exists. If both parameters pass the attribute will be added to the class #
    def addAttribute(self, class1, attribute1):
        for item in self.classes:
            if item.name == class1.name:
                if attribute1 in item.attributtesSets:
                    return "Attribute already exists in this class"
                else:
                    temp = item
                    temp.attributtesSets.add(attribute1)
                    self.classes.remove(item)
                    self.classes.add(temp)
                    return "Attribute has been added to this class"
            else:
                return "Class does not exist"