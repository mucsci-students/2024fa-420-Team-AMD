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

class testEditorController(unittest.TestCase):
    def testSave(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        path = 'out.JSON'

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseSaveLocation', lambda: path):
            ctrl.save()
        b = os.path.exists(path)
        if b:
           try:
               os.remove(path)
           except Exception as e:
               pass
        assert b, 'File was not saved properly'

    def testSaveEmpty(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        path = ''

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseSaveLocation', lambda: path):
            ctrl.save()
        b = os.path.exists(path)
        assert not b, 'File was not saved properly'

    def testSaveGui(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        path = 'out.JSON'

        ctrl.classAdd('Foo')
        ctrl.classAdd('Bar')
        ctrl.addField('Foo', 'size')
        ctrl.addMethod('Bar', 'run', ['energy', 'speed'])
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseSaveLocation', lambda: path):
            ctrl.saveGUI()
        b = os.path.exists(path)
        if b:
           try:
               os.remove(path)
           except Exception as e:
               pass
        assert b, 'File was not saved properly'

    def testSaveGuiRelLineMismatch(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        ctrl.editor.getRelationshipType = unittest.mock.Mock()
        ctrl.editor.getRelationshipType.return_value = None
        path = 'out.JSON'

        ctrl.classAdd('Foo')
        ctrl.classAdd('Bar')
        ctrl.addField('Foo', 'size')
        ctrl.addMethod('Bar', 'run', ['energy', 'speed'])
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseSaveLocation', lambda: path):
            ctrl.saveGUI()
        b1 = os.path.exists(path)
        b2 = False
        if b1:
           try:
               f = open(path, 'r')
               s = f.read()
               # print(f'FILE LEN`{len(s)}`')
               # This is just to see that the relationships are not saved
               b2 = len(s) == 847
               f.close()
               os.remove(path)
           except Exception as e:
               pass
        assert b1, 'File was not saved properly'

    def testSaveGuiEmpty(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        path = ''

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseSaveLocation', lambda: path):
            ctrl.saveGUI()
        b = os.path.exists(path)
        assert not b, 'File was not saved properly'

    def testLoad(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        path = 'test.JSON'

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseLoadLocation', lambda: path):
            ctrl.load()
        b1 = len(editor.classes) == 2
        b2 = len(editor.relationships) == 1
        assert b1 and b2, 'File was not loaded properly'

    def testLoadEmpty(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        path = ''

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseLoadLocation', lambda: path):
            ctrl.load()
        b1 = len(editor.classes) == 0
        b2 = len(editor.relationships) == 0
        assert b1 and b2, 'File was loaded when it shouldnt have'

    def testLoadGui(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        path = 'test.JSON'

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseLoadLocation', lambda: path):
            ctrl.loadGUI()
        b1 = len(editor.classes) == 2
        b2 = len(editor.relationships) == 1
        assert b1 and b2, 'File was not loaded properly'

    def testLoadGuiEmpty(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        path = ''

        with unittest.mock.patch.object(ctrl.ui, 'uiChooseLoadLocation', lambda: path):
            ctrl.loadGUI()
        b1 = len(editor.classes) == 0
        b2 = len(editor.relationships) == 0
        assert b1 and b2, 'File was loaded when it shouldnt have'

    def testPushCmd1(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        
        cmd1 = CommandClassAdd('Foo')
        cmd1.execute(ctrl)
        ctrl.pushCmd(cmd1)
        
        b1 = len(ctrl.editor.action_stack) == 1
        b2 = ctrl.editor.canAddField()
        b3 = ctrl.editor.canAddMethod()

        assert b1 and b2 and b3, 'Stack was not updated or grayed out options miscalculated'

    def testHelpCLI(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)
        Completions.instance().tab_input = unittest.mock.Mock()
        Completions.instance().tab_input.return_value = 'exit'
        
        b = ctrl.editorHelp()

        assert b is None, 'An error occured'

    def testHelpGUI(self):
        editor = Editor()
        ui = GUI(None)
        ctrl = EditorController(ui, editor)
        ui.controller = ctrl
        ctrl.ui.uiFeedback = unittest.mock.Mock()
        ctrl.ui.uiError = unittest.mock.Mock()
        
        b = ctrl.ui.showHelp()

        assert b is None, 'An error occured'
