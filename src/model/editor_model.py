import json
from .class_model import Class, Field, Method
from .relationship_model import Relationship

class Editor:
    def __init__(self):
        self.classes = {}
        self.relationships = set()
    
    def hasRelationship(self, src, dst):
        for rel in self.relationships:
            if rel.src == src and rel.dst == dst:
                return True
        return False

class EditorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Editor):
            return {'classes': list(obj.classes.values()), 'relationships': list(obj.relationships)}
        if isinstance(obj, Class):
            # return {'name': obj.name, 'attributes': list(obj.attributtesSets)}
            return {'name': obj.name, 'fields': obj.fields, 'methods': obj.methods}
        if isinstance(obj, Relationship):
            return {'source': obj.src, 'destination': obj.dst, 'type': obj.typ.display()}
        if isinstance(obj, Field):
            return {'name': obj.name}
        if isinstance(obj, Method):
            # Obj.params is a list of strings, so we map them to objects with a string field
            # in order to comply with the JSON specification
            l = list(map(lambda x: {'name': x}, obj.params))
            return {'name': obj.name, 'params': l}
        return json.JSONEncoder.default(self, obj)
