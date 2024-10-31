from model.class_model import Method

# Common interface for commands
# All command objects track the changes in the program state 
#
# Commands CAN fail, since their respective controller functions
# can fail also. Failed commands will not be added to the action stack.
class Command:
    def execute(self, controller) -> bool:
        pass

    def undo(self, controller) -> bool:
        pass

class CommandClassAdd(Command):
    def __init__(self, name):
        self.name = name

    def execute(self, controller):
        return controller.classAdd(self.name)

    def undo(self):
        return controller.classDelete(self.name)

class CommandClassDelete(Command):
    def __init__(self, name):
        self.name = name

    def execute(self, controller):
        return controller.classDelete(self.name)

    def undo(self, controller):
        return controller.classAdd(self.name)

class CommandClassRename(Command):
    def __init__(self, name, rename):
        self.name = name
        self.rename = rename

    def execute(self, controller):
        return controller.classRename(self.name, self.rename)

    def undo(self, controller):
        return controller.classRename(self.rename, self.name)

class CommandRelationshipAdd(Command):
    def __init__(self, class1, class2, typ):
        self.class1 = class1
        self.class2 = class2
        self.typ = typ

    def execute(self, controller):
        return controller.relationshipAdd(self.class1, self.class2, self.typ)

    def undo(self, controller):
        return controller.relationshipDelete(self.class1, self.class2)
    
class CommandRelationshipDelete(Command):
    def __init__(self, class1, class2):
        self.class1 = class1
        self.class2 = class2
        self.typ = None

    def execute(self, controller):
        # Saving the type for undo
        # Controller can fail if this relationship is non-existant
        if controller.editor.hasRelationship(self.class1, self.class2):
            self.typ = controller.editor.getRelationship(self.class1, self.class2).typ
        return controller.relationshipDelete(self.class1, self.class2)

    def undo(self, controller):
        return controller.relationshipAdd(self.class1, self.class2, self.typ)

class CommandRelationshipEdit(Command):
    def __init__(self, class1, class2, new_typ):
        self.class1 = class1
        self.class2 = class2
        self.new_typ = new_typ
        self.old_typ = None

    def execute(self, controller):
        # Saving the old type for undo
        # Controller can fail if this relationship is non-existant
        if controller.editor.hasRelationship(self.class1, self.class2):
            self.old_typ = controller.editor.getRelationship(self.class1, self.class2).typ
        return controller.relationshipEdit(self.class1, self.class2, self.new_typ)

    def undo(self, controller):
        return controller.relationshipEdit(self.class1, self.class2, self.old_typ)

class CommandFieldAdd(Command):
    def __init__(self, class1, field1):
        self.class1 = class1
        self.field1 = field1

    def execute(self, controller):
        return controller.addField(self.class1, self.field1)

    def undo(self, controller):
        return controller.deleteField(self.class1, self.field1)

class CommandFieldDelete(Command):
    def __init__(self, class1, field1):
        self.class1 = class1
        self.field1 = field1

    def execute(self, controller):
        return controller.deleteField(self.class1, self.field1)

    def undo(self, controller):
        return controller.addField(self.class1, self.field1)

class CommandFieldRename(Command):
    def __init__(self, class1, field1, field2):
        self.class1 = class1
        self.field1 = field1
        self.field2 = field2

    def execute(self, controller):
        return controller.renameField(self.class1, self.field1, self.field2)

    def undo(self, controller):
        return controller.renameField(self.class1, self.field2, self.field1)

class CommandMethodAdd(Command):
    def __init__(self, class1, method, params):
        self.class1 = class1
        self.method = method
        self.params = params

    def execute(self, controller):
        return controller.addMethod(self.class1, self.method, self.params)

    def undo(self, controller):
        return controller.deleteMethod(self.class1, self.method)

class CommandMethodDelete(Command):
    def __init__(self, class1, method):
        self.class1 = class1
        self.method = method
        self.params = []

    def execute(self, controller):
        # Saving the parameters for undo
        try:
            if self.class1 in controller.editor.classes:
                item = controller.editor.classes[self.class1]
            method = next(m for m in item.methods if m.name == self.method)
            self.params = method.params
        except:
            return False
        return controller.deleteMethod(self.class1, self.method)

    def undo(self, controller):
        return controller.addMethod(self.class1, self.method, self.params)

class CommandMethodRename(Command):
    def __init__(self, class1, method1, method2):
        self.class1 = class1
        self.method1 = method1
        self.method2 = method2

    def execute(self, controller):
        return controller.renameMethod(self.class1, self.method1, self.method2)

    def undo(self, controller):
        return controller.renameMethod(self.class1, self.method2, self.method1)

class CommandParameterRemove(Command):
    def __init__(self, class1, method, param):
        self.class1 = class1
        self.method = method
        self.param = param
        self.old_params = []

    def execute(self, controller):
        # Saving the parameters for undo
        try:
            if self.class1 in controller.editor.classes:
                item = controller.editor.classes[self.class1]
            method = next(m for m in item.methods if m.name == self.method)
            self.old_params = method.params
        except:
            return False
        return controller.removeParameter(self.class1, self.method, self.param)

    def undo(self, controller):
        return controller.replaceParameters(self.class1, self.method, self.old_params)

class CommandParameterClear(Command):
    def __init__(self, class1, method):
        self.class1 = class1
        self.method = method
        self.old_params = []

    def execute(self, controller):
        # Saving the parameters for undo
        try:
            if self.class1 in controller.editor.classes:
                item = controller.editor.classes[self.class1]
            method = next(m for m in item.methods if m.name == self.method)
            self.old_params = method.params
        except:
            return False
        return controller.clearParameters(self.class1, self.method)

    def undo(self, controller):
        return controller.replaceParameters(self.class1, self.method, self.old_params)

class CommandParameterRename(Command):
    def __init__(self, class1, method, param1, param2):
        self.class1 = class1
        self.method = method
        self.param1 = param1
        self.param2 = param2

    def execute(self, controller):
        return controller.renameParameter(self.class1, self.method, self.param1, self.param2)

    def undo(self, controller):
        return controller.renameParameter(self.class1, self.method, self.param2, self.param1)

class CommandParameterChange(Command):
    def __init__(self, class1, method, params):
        self.class1 = class1
        self.method = method
        self.params = params
        self.old_params = []

    def execute(self, controller):
        # Saving the parameters for undo
        try:
            if self.class1 in controller.editor.classes:
                item = controller.editor.classes[self.class1]
            method = next(m for m in item.methods if m.name == self.method)
            self.old_params = method.params
        except:
            return False
        return controller.replaceParameters(self.class1, self.method, self.params)

    def undo(self, controller):
        return controller.replaceParameters(self.class1, self.method, self.old_params)
