import unittest

from editor import *
from classes import *

class testEditor(unittest.TestCase):
    def testClassDeleteSuccess(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classDelete('Foo')
        assert editor.classes == {}, 'Foo was not deleted'

    def testClassDeleteFailure(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classDelete('Bar')
        assert 'Foo' in editor.classes, 'Foo did not remain after failed deletion'
        
    def testClassRenameSuccess(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classRename('Foo', 'Bar')
        assert 'Bar' in editor.classes and 'Foo' not in editor.classes, 'Foo was not renamed to Bar'
    
    # Failure due to targeted class of renaming not existing
    def testClassRenameFailure1(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classRename('Bar', 'Foo2')
        assert 'Foo2' not in editor.classes and 'Bar' not in editor.classes, 'Bar does not exist, rename failed'
    
    # Failure due to class of new name already existing
    def testClassRenameFailure2(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        editor.classRename('Foo', 'Bar')
        assert 'Foo' in editor.classes and 'Bar' in editor.classes, 'Foo could not be renamed Bar: Bar already exists.'

    def testRelationshipAddSuccess(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        editor.relationshipAdd('Foo', 'Bar')
        # relationshipAdd will always, on success, insert a tuple with the order of the arguments given
        assert ('Foo', 'Bar') in editor.relationships, 'Relationship was not added successfully'

    # Failure due to already existing relationship
    def testRelationshipAddFailure1(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        editor.relationshipAdd('Foo', 'Bar')

        editor.relationshipAdd('Bar', 'Foo')
        assert ('Bar', 'Foo') not in editor.relationships, 'Duplication was not checked for'

    # Failure due to missing class
    def testRelationshipAddFailure2(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.relationshipAdd('Foo', 'Bar')
        assert ('Foo', 'Bar') not in editor.relationships, 'Class was not checked for existence'

    def testRelationshipDeleteSuccess(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        editor.relationships.add(('Foo', 'Bar'))

        editor.relationshipDelete('Foo', 'Bar')
        assert ('Foo', 'Bar') not in editor.relationships, 'Relationship was not deleted'

    # Failure due to no relationship
    def testRelationshipDeleteFailure1(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()

        editor.relationshipDelete('Foo', 'Bar')
        assert ('Foo', 'Bar') not in editor.relationships, 'Relationship should not have been removed'

    # Failure due to missing classes
    def testRelationshipDeleteFailure2(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        editor.relationships.add(('Foo', 'Bar'))

        editor.relationshipDelete('Foo', 'Baz')
        assert ('Foo', 'Bar') in editor.relationships and ('Foo', 'Baz') not in editor.relationships, 'Relationship should not have been removed'

    def testListClasses(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        editor.relationshipAdd('Foo', 'Bar')
        # ADD editor.attributesAdd(class, attribute) HERE
        
        # NEED HELP ASSERTING PRINT OUTPUT, 'Classes and contents not successfully listed.'

if __name__ == '__main__':
    unittest.main()
