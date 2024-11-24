import unittest
# We have to import the specific class here so unittest will detect it
from tests.test_editor import testEditor
from tests.test_editor_controller import testEditorController
from tests.test_class_model import testModelClass
from tests.test_singleton import testSingleton
from tests.test_ui_cli import testCLI

if __name__ == '__main__':
    unittest.main()
