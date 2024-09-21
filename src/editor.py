import Class
class Editor:
    classes = {}
    # Checks if a class of the given name already exists, if not, a new one is created
    def classAdd(self, name):
        for item in classes:
            if item.name == name:
                return "This class already exists"
        newclass = Class(name)
        classes.add(newclass)
        return "class added"
        
    def classDelete(self, name):
        pass
    def classRename(self, name, rename):
        pass
