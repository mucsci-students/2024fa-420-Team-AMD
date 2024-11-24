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

class testSingleton(unittest.TestCase):
    def testConstructor(self):
        b = False
        try:
            x = Completions()
        except TypeError:
            b = True
        assert b, 'Singleton should not allow instance creation'
