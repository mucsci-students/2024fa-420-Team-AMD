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
    def classRename(self, name, rename):
        pass

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
