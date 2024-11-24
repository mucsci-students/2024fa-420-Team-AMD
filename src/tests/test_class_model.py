import unittest
import unittest.mock
import os
from model.editor_model import Editor
from model.class_model import Class, Field, Method
from model.relationship_model import Type, Relationship
from model.command_model import *
from controller.editor_controller import EditorController
from view.ui_cli import CLI, Completions
from view.ui_gui import GUI

class testModelClass(unittest.TestCase):
    def testHashes(self):
        fields = {}
        fields[Field('Foo')] = True
        b1 = fields[Field('Foo')]
        b2 = Field('Foo').__hash__() == hash(('Foo'))
        
        methods = {}
        methods[Method('run')] = True
        b3 = methods[Method('run')]
        b4 = Method('run').__hash__() == hash(('run'))
        assert b1 and b2 and b3 and b4, 'Hashes not working as intended'
