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
    
    # Function renames given attribute in given class if both exist and new name does not
    def renameAttribute(self, class1, attribute1, attribute2):
        if class1 in self.classes:
            item = self.classes[class1]
            if attribute1 in item.attributtesSets:
                if attribute2 not in item.attributtesSets:
                    self.classes[class1].attributtesSets.remove(attribute1)
                    self.classes[class1].attributtesSets.add(attribute2)
                    print(f'Attribute `{attribute1}` renamed to {attribute2}!')
                else:
                    print(f'Attribute `{attribute2}` already exists in the class {class1}')
            else:
                print(f'Attribute `{attribute1}` does not exist in class {class1}')
        else:
            print(f'Class {class1} does not exist')
