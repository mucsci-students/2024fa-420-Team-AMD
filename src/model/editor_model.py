import json
from .class_model import Class, Field, Method
from .relationship_model import Relationship

class Editor:
    def __init__(self):
        self.classes = {}
        self.relationships = {}
        self.action_stack = []
        self.action_idx = 0
    
    def getClasses(self):
        ls = [c for c in self.classes]
        return ls
    
    # Cannot use != as __eq__ can only be called on objects of the same type here
    def hasRelationship(self, src, dst):
        return (src, dst) in self.relationships

    # Helper method to get details about a relationship between a source class and a destination class
    def getRelationship(self, src, dst):
        return self.relationships.get((src, dst))

    #===== State Checkers =====#
    # These functions check what actions can be performed from the state of the editor
    def canAddField(self):
        return len(self.classes) > 0

    def canAddMethod(self):
        return len(self.classes) > 0

    def canDoParams(self):
        for clazz in self.classes:
            item = self.classes[clazz]
            if len(item.methods) > 0:
                return True
        return False

    def canAddRelationship(self):
        return len(self.classes) > 1

    #===== Command Stack =====#
    
    def getRelationshipType(self, class1, class2):
        # Check if a relationship exists between the two classes
        relationship = self.getRelationship(class1, class2)
        return relationship.typ if relationship else None

    def addRelationship(self, src, dst, typ):
        if (src, dst) not in self.relationships:
            self.relationships[(src, dst)] = Relationship(src, dst, typ)
            return True
        return False

    def removeRelationship(self, src, dst):
        return self.relationships.pop((src, dst), None) is not None

    def pushCmd(self, cmd):
        self.action_stack.append(cmd)
        self.action_idx = len(self.action_stack) - 1

    def popCmd(self):
        return self.action_stack.pop()

class EditorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Editor):
            return {
                'classes': list(obj.classes.values()),
                'relationships': list(obj.relationships.values())  # Convert dictionary values to a list
            }

        if isinstance(obj, Class):
           # Create a position dictionary if it exists
            position = {'x': obj.position[0], 'y': obj.position[1]} if hasattr(obj, 'position') else None
            # return {'name': obj.name, 'attributes': list(obj.attributtesSets)}
            return {'name': obj.name, 'fields': obj.fields, 'methods': obj.methods, 'position': position}
        
        if isinstance(obj, Field):
            return {'name': obj.name}
        if isinstance(obj, Method):
            # Obj.params is a list of strings, so we map them to objects with a string field
            # in order to comply with the JSON specification
            l = list(map(lambda x: {'name': x}, obj.params))
            return {'name': obj.name, 'params': l}
        if isinstance(obj, Relationship):
            return {'source': obj.src, 'destination': obj.dst, 'type': obj.typ.display()}
        
        return json.JSONEncoder.default(self, obj)
