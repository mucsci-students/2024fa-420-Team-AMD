from view.ui_cli import CLI
from view.ui_gui import GUI
from model.editor_model import Editor
from controller.editor_controller import EditorController  

class App:
    def __init__(self):
        self.ui = None

    def run(self):
        if self.ui is None:
            print('ERROR: App created without UI component')
            return
        return self.ui.uiRun()

class AppBuilder:
    def __init__(self):
        self.editor = None
        self.reset()
    
    def reset(self):
        self.app = App()
    
    def getResult(self):
        return self.app
    
    def fail(self, msg):
        print(msg)
        self.app = None
    
    def setUI(self, ui):
        self.app.ui = ui

    def makeEditor(self):
        self.editor = Editor()  
    
    def makeController(self):
        if self.editor is None or self.app.ui is None:
            self.fail('ERROR: Tried to make controller without components')
            return
        self.controller = EditorController(self.app.ui, self.editor)
    
    def linkControllerToUI(self):
        if self.app.ui is None or self.controller is None:
            self.fail('ERROR: Missing UI or Controller element')
            return
        self.app.ui.controller = self.controller

class AppDirector:
    def __init__(self):
        self.builder = AppBuilder()
        
    def makeAppCLI(self):
        self.builder.setUI(CLI())
        self.builder.makeEditor()
        self.builder.makeController()
        self.builder.linkControllerToUI()
        return self.builder.getResult()

    def makeAppGUI(self):
        self.builder.setUI(GUI())
        self.builder.makeEditor()
        self.builder.makeController()
        self.builder.linkControllerToUI()
        app = self.builder.getResult()
        # We need to gray out options on startup
        app.ui.updateAccess()
        return app
