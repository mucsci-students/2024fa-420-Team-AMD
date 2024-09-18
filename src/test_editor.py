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

if __name__ == '__main__':
    unittest.main()
