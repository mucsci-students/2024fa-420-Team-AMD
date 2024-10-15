import json
from .class_model import Class
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
            return {'classes': obj.classes, 'relationships': list(obj.relationships)}
        if isinstance(obj, Class):
            return {'name': obj.name, 'attributes': list(obj.attributtesSets)}
        if isinstance(obj, Relationship):
            # TODO: I have yet to check the formatting here
            return {'src': obj.src, 'dst': obj.dst, 'type': obj.typ.display()}
        return json.JSONEncoder.default(self, obj)
