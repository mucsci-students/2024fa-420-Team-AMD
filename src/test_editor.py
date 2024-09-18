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
    
    def testClassRenameFailure1(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        result = editor.classRename('Bar', 'Foo2')
        assert result == False, 'Bar does not exist, rename failed'
    
    def testClassREnameFailure2(self):
        editor = Editor()
        editor.classes['Foo'] = Class()
        editor.classes['Bar'] = Class()
        result = editor.classRename('Foo', 'Bar')
        assert result == False, 'Foo could not be renamed Bar: Bar already exists.'
        
if __name__ == '__main__':
    unittest.main()
