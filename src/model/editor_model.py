import json
from .class_model import Class

class Editor:
    def __init__(self):
        self.classes = {}
        self.relationships = set()

class EditorEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Editor):
            return {'classes': obj.classes, 'relationships': list(obj.relationships)}
        if isinstance(obj, Class):
            return {'name': obj.name, 'attributes': list(obj.attributtesSets)}
        return json.JSONEncoder.default(self, obj)
