class Editor:
    classes = {}
    def classAdd(self, name):
        pass
    def classDelete(self, name):
        pass

    "Function to rename a class called 'name' to a class called 'rename'."
    def classRename(self, name, rename):
        if name in self.classes:
            self.classes[rename] = self.classes.pop(name)
        elif rename in self.classes:
            raise NameError(f"{rename} is an already existing class.")
        else: 
            raise NameError(f"{rename} does not exist.")
