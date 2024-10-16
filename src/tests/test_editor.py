import unittest
from model.editor_model import Editor
from model.class_model import Class, Field, Method
from model.relationship_model import Type, Relationship
from controller.editor_controller import EditorController
from view.ui_cli import CLI

class testEditor(unittest.TestCase):
    
    def testClassDeleteSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.classDelete('Foo')
        assert ctrl.editor.classes == {}, 'Foo was not deleted'

    def testClassDeleteFailure(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.classDelete('Bar')
        assert 'Foo' in ctrl.editor.classes, 'Foo did not remain after failed deletion'

    # This is to monitor a bug where a lambda expression cleared the relationships list
    def testClassDeleteBugfix(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.classAdd('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)
        ctrl.classAdd('Quo')

        before = ctrl.editor.relationships
        ctrl.classDelete('Quo')
        after = ctrl.editor.relationships
        print('Bugfix: ', before, after)

        assert before == after, 'Relationships were modified when an unrelated class was deleted'
        
    def testClassRenameSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.classRename('Foo', 'Bar')
        assert 'Bar' in ctrl.editor.classes and 'Foo' not in ctrl.editor.classes, 'Foo was not renamed to Bar'
    
    # Failure due to targeted class of renaming not existing
    def testClassRenameFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.classRename('Bar', 'Foo2')
        assert 'Foo2' not in ctrl.editor.classes and 'Bar' not in ctrl.editor.classes, 'Bar does not exist, rename failed'
    
    # Failure due to class of new name already existing
    def testClassRenameFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.classRename('Foo', 'Bar')
        assert 'Foo' in ctrl.editor.classes and 'Bar' in ctrl.editor.classes, 'Foo could not be renamed Bar: Bar already exists.'

    def testRelationshipAddSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)
        assert Relationship('Foo', 'Bar', Type.Aggregate) in ctrl.editor.relationships, 'Relationship was not added successfully'

    # Failure due to already existing relationship
    def testRelationshipAddFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        ctrl.relationshipAdd('Bar', 'Foo', Type.Aggregate)
        assert Relationship('Bar', 'Foo', Type.Aggregate) not in ctrl.editor.relationships, 'Duplication was not checked for'

    # Failure due to missing class
    def testRelationshipAddFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)
        assert Relationship('Foo', 'Bar', Type.Aggregate) not in ctrl.editor.relationships, 'Class was not checked for existence'

    def testRelationshipDeleteSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        ctrl.relationshipDelete('Foo', 'Bar')
        assert Relationship('Foo', 'Bar', Type.Aggregate) not in ctrl.editor.relationships, 'Relationship was not deleted'

    # Failure due to no relationship
    def testRelationshipDeleteFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')

        ctrl.relationshipDelete('Foo', 'Bar')
        assert Relationship('Foo', 'Bar', Type.Aggregate) not in ctrl.editor.relationships, 'Relationship should not have been removed'

    # Failure due to missing classes
    def testRelationshipDeleteFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        ctrl.relationshipDelete('Foo', 'Baz')
        assert Relationship('Foo', 'Bar', Type.Aggregate) in ctrl.editor.relationships and Relationship('Foo', 'Baz', Type.Aggregate) not in ctrl.editor.relationships, 'Relationship should not have been removed'

    def testRelationshipEditSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        ctrl.relationshipEdit('Foo', 'Bar', Type.Inheritance)
        
        b1 = Relationship('Foo', 'Bar', Type.Aggregate) not in ctrl.editor.relationships
        b2 = Relationship('Foo', 'Bar', Type.Inheritance) in ctrl.editor.relationships
        assert b1 and b2, 'Relationship was not edited successfully'

    # Failure due to no change
    def testRelationshipEditFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')
        ctrl.relationshipAdd('Foo', 'Bar', Type.Aggregate)

        ctrl.relationshipEdit('Foo', 'Bar', Type.Aggregate)
        
        b1 = Relationship('Foo', 'Bar', Type.Aggregate) in ctrl.editor.relationships
        assert b1, 'Relationship was edited when not supposed to'

    # Failure due to no relationship
    def testRelationshipEditFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')
        ctrl.editor.classes['Bar'] = Class('Bar')

        ctrl.relationshipEdit('Foo', 'Bar', Type.Inheritance)
        
        b1 = Relationship('Foo', 'Bar', Type.Inheritance) not in ctrl.editor.relationships
        assert b1, 'Relationship should not have manifested from nothing'

    # Failure due to no class
    def testRelationshipEditSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.editor.classes['Foo'] = Class('Foo')

        ctrl.relationshipEdit('Foo', 'Bar', Type.Inheritance)
        
        b1 = Relationship('Foo', 'Bar', Type.Inheritance) not in ctrl.editor.relationships
        assert b1, 'Relationship should not have manifested from nothing'

    def testAddFieldSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.addField('Foo', 'at')
        assert Field('at') in ctrl.editor.classes['Foo'].fields, 'Attribute added to class'

    # Failure due to class not existing
    def testAddFieldFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.addField('Foo', 'at')
        assert 'Foo' not in ctrl.editor.classes, 'class was not checked for existence'
    
    # Failure due to attribute already existing in class
    def testAddFieldFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'at')

        ctrl.addField('Foo', 'at')
        assert Field('at') in ctrl.editor.classes['Foo'].fields, 'duplication was not checked for'

    def testRenameFieldSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'at')

        ctrl.renameField('Foo', 'at', 'at2')
        assert Field('at2') in ctrl.editor.classes['Foo'].fields and Field('at') not in ctrl.editor.classes['Foo'].fields, 'Attribute name was not changed'

    # Failure due to class not existing
    def testRenameFieldFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.renameField('Foo', 'at', 'at2')
        assert 'Foo' not in ctrl.editor.classes, 'class not checked for existence'
    
    # Faiure due to original attribute not existing
    def testRenameFieldFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.renameField('Foo', 'at', 'at2')
        assert Field('at2') not in ctrl.editor.classes['Foo'].fields and Field('at') not in ctrl.editor.classes['Foo'].fields, 'Attribute not checked for existence'
    
    # Failure due to new attrubute name already existing
    def testRenameFieldFailure3(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addField('Foo', 'at')
        ctrl.addField('Foo', 'at2')

        ctrl.renameField('Foo', 'at', 'at2')
        assert Field('at2') in ctrl.editor.classes['Foo'].fields and Field('at') in ctrl.editor.classes['Foo'].fields, 'Duplication was not checked for'

    def testAddMethodSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.addMethod('Foo', 'run', ['a, b, c'])
        assert Method('run') in ctrl.editor.classes['Foo'].methods, 'Method was not added to the class'

    # Failure due to no class
    def testAddMethodFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.addMethod('Foo', 'run', ['a, b, c'])
        assert 'Foo' not in ctrl.editor.classes, 'Method was added to a non existant class'

    # Failure due to duplication
    def testAddMethodFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.addMethod('Foo', 'run', ['a, b, c'])
        ctrl.addMethod('Foo', 'run', ['a, b, c'])
        assert Method('run') in ctrl.editor.classes['Foo'].methods, 'Method should still exist'

    def testDeleteMethodSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.addMethod('Foo', 'run', ['a, b, c'])
        ctrl.deleteMethod('Foo', 'run')
        assert Method('run') not in ctrl.editor.classes['Foo'].methods, 'Method still exists'

    # Failure due to no method existing
    def testDeleteMethodFailure(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.deleteMethod('Foo', 'run')
        assert Method('run') not in ctrl.editor.classes['Foo'].methods, 'Method should not exist'

    def testRenameMethodSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'run', ['a, b, c'])

        ctrl.renameMethod('Foo', 'run', 'walk')
        b1 = Method('run') not in ctrl.editor.classes['Foo'].methods
        b2 = Method('walk') in ctrl.editor.classes['Foo'].methods
        assert b1 and b2, 'Method should have been renamed'

    # Failure due to no existing method
    def testRenameMethodFailure1(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')

        ctrl.renameMethod('Foo', 'run', 'walk')
        b1 = Method('run') not in ctrl.editor.classes['Foo'].methods
        b2 = Method('walk') not in ctrl.editor.classes['Foo'].methods
        assert b1 and b2, 'No method should exist'

    # Failure due to duplication
    def testRenameMethodFailure2(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'run', ['a, b, c'])
        ctrl.addMethod('Foo', 'walk', [])

        ctrl.renameMethod('Foo', 'run', 'walk')
        b1 = Method('run') in ctrl.editor.classes['Foo'].methods
        b2 = Method('walk') in ctrl.editor.classes['Foo'].methods
        assert b1 and b2, 'Nothing should have changed'

    def testRenameParameterSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])

        ctrl.renameParameter('Foo', 'run', 'a', 'd')
        b1 = Method('run') in ctrl.editor.classes['Foo'].methods
        idx = ctrl.editor.classes['Foo'].methods.index(Method('run'))
        b2 = ctrl.editor.classes['Foo'].methods[idx].params == ['d', 'b', 'c']
        assert b1 and b2, 'Parameter was not renamed correctly'

    def testRenameParameterFailure(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])

        ctrl.renameParameter('Foo', 'run', 'd', 'e')
        b1 = Method('run') in ctrl.editor.classes['Foo'].methods
        idx = ctrl.editor.classes['Foo'].methods.index(Method('run'))
        b2 = ctrl.editor.classes['Foo'].methods[idx].params == ['a', 'b', 'c']
        assert b1 and b2, 'Parameter was modified when they should not have'

    def testClearParametersSuccess(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])

        ctrl.clearParameters('Foo', 'run')
        b1 = Method('run') in ctrl.editor.classes['Foo'].methods
        idx = ctrl.editor.classes['Foo'].methods.index(Method('run'))
        b2 = ctrl.editor.classes['Foo'].methods[idx].params == []
        assert b1 and b2, 'Parameters were not cleared'

    def testClearParametersFailure(self):
        editor = Editor()
        ui = CLI()
        ctrl = EditorController(ui, editor)

        ctrl.classAdd('Foo')
        ctrl.addMethod('Foo', 'run', ['a', 'b', 'c'])

        ctrl.clearParameters('Foo', 'walk')
        b1 = Method('run') in ctrl.editor.classes['Foo'].methods
        idx = ctrl.editor.classes['Foo'].methods.index(Method('run'))
        b2 = ctrl.editor.classes['Foo'].methods[idx].params == ['a', 'b', 'c']
        assert b1 and b2, 'Parameters were clared when they should not have'
