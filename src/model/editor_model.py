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
            return {'classes': list(obj.classes.values()), 'relationships': list(obj.relationships)}
        if isinstance(obj, Class):
            # return {'name': obj.name, 'attributes': list(obj.attributtesSets)}
            # TODO: make classes for fields and methods so that we can check for them here
            return {'name': obj.name, 'fields': list(obj.attributtesSets), 'methods': ['nil']}
        if isinstance(obj, Relationship):
            # TODO: I have yet to check the formatting here
            return {'source': obj.src, 'destination': obj.dst, 'type': obj.typ.display()}
        return json.JSONEncoder.default(self, obj)
