import unittest
import unittest.mock
import prompt_toolkit
import os
from model.editor_model import Editor
from model.class_model import Class, Field, Method
from model.relationship_model import Type, Relationship
from model.command_model import *
from controller.editor_controller import EditorController
from view.ui_cli import CLI, Completions
from view.ui_gui import GUI
from prompt_toolkit.document import Document
from prompt_toolkit.completion import Completion
import view

from unittest.mock import patch, MagicMock

class testCLI(unittest.TestCase):
    def testListClass(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        ctrl.ui.uiError = unittest.mock.Mock()
        
        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'size')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])
        
        ctrl.listClass('Foo')
        ctrl.ui.uiError.assert_not_called, 'An error occurred'

    def testListClassFailure(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        ctrl.ui.uiError = unittest.mock.Mock()
        
        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'size')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])
        ctrl.classAdd('Bar')
        ctrl.editor.relationships[('Foo', 'Bar')] = Relationship('Foo', 'Bar', unittest.mock.Mock())
        
        ctrl.listClass('Foo')
        ctrl.ui.uiError.assert_called, 'An error did not occur'

    def testListRelationships(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        ctrl.ui.uiError = unittest.mock.Mock()
        
        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'size')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])
        ctrl.classAdd('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Inheritance)
        
        ctrl.listRelationships('Foo')
        ctrl.ui.uiError.assert_not_called, 'An error occurred'

    def testListClasses(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        ctrl.ui.uiError = unittest.mock.Mock()
        
        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'size')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])
        ctrl.classAdd('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Inheritance)
        
        ctrl.listClasses()
        ctrl.ui.uiError.assert_not_called, 'An error occurred'
    
    def testCompletions(self):
        Completions.instance().set_tab_completions(['Foo'])
        b2 = len(Completions.instance().get_tab_completions()) == 1
        assert b2, 'Container not working as intended'

    def testCompletionsClasses(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        ctrl.classAdd('Foo')
        ctrl.classAdd('Bar')
        Completions.instance().class_completions(ctrl)
        b1 = len(Completions.instance().get_tab_completions()) == 2

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsFields(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'a')
        ctrl.addField('Foo', 'b')
        ctrl.addField('Foo', 'c')
        Completions.instance().field_completions(ctrl, 'Foo')
        b1 = len(Completions.instance().get_tab_completions()) == 3

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsFieldsEmpty(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        Completions.instance().field_completions(ctrl, 'Foo')
        b1 = len(Completions.instance().get_tab_completions()) == 0

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsMethods(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'a', [])
        ctrl.addMethod('Foo', 'b', [])
        ctrl.addMethod('Foo', 'c', [])
        Completions.instance().method_completions(ctrl, 'Foo')
        b1 = len(Completions.instance().get_tab_completions()) == 3

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsMethodsEmpty(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        Completions.instance().method_completions(ctrl, 'Foo')
        b1 = len(Completions.instance().get_tab_completions()) == 0

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsParams(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'a', ['1', '2', '3'])
        Completions.instance().param_completions(ctrl, 'Foo', 'a')
        b1 = len(Completions.instance().get_tab_completions()) == 3

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsParamsEmpty1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        ctrl.classAdd('Foo')
        Completions.instance().param_completions(ctrl, 'Foo', 'a')
        b1 = len(Completions.instance().get_tab_completions()) == 0

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsParamsEmpty2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        Completions.instance().param_completions(ctrl, 'Foo', 'a')
        b1 = len(Completions.instance().get_tab_completions()) == 0

        assert b1, 'Classes were not correctly gathered'

    def testCompletionsTab(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        
        Completions.instance().set_tab_completions(['start', 'stop', 'foo'])

        document = Document(text='st', cursor_position=2)
        complete_event = None
        completions = list(Completions.instance().get_completions(document, complete_event))

        # Check the expected completions
        expected = ['start', 'stop']
        actual = [completion.text for completion in completions]

        assert expected == actual, 'Expected == actual'
