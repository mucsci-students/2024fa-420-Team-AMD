class Editor:
    def __init__(self):
        self.classes = {}

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
