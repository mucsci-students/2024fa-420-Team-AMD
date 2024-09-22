from classes import *

class Editor:
    classes = {}
    # Checks if a class of the given name already exists, if not, a new one is created
    def classAdd(self, name):
        if name in self.classes:
            print(f'Class {name} already exists')
        else:
            newclass = Class(name)
            self.classes[name] = newclass
            print(f'Added class {name}!')
        
    def classDelete(self, name):
        pass
    def classRename(self, name, rename):
        pass
