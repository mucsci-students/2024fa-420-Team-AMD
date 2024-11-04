from model.editor_model import Editor

# Common user interface between CLI and GUI
class UI:
    def uiFeedback(self, text: str):
        pass

    def uiError(self, text: str):
        pass
    
    def uiRun(self, editor: Editor):
        pass
    
    def uiQuery(self, prompt: str) -> str:
        pass
    
    #===== Native File Dialog =====#
    # These functions implement the choosing of a file path,
    # which is a native dialog in the GUI and a string path input in the CLI

    def uiChooseSaveLocation(self) -> str:
        pass

    def uiChooseLoadLocation(self) -> str:
        pass

    #===== GUI Commands =====#
    # These commands are implemented only for the GUI, and do nothing in the CLI

    def updateAccess(self):
        pass
    
    def addClassBox(self, name: str):
        pass

    def deleteClassBox(self, name: str):
        pass

    def renameClassBox(self, name: str, rename: str):
        pass

    def drawRelationshipLine(self, class1: str, class2: str, typename: str):
        pass

    def deleteRelationshipLine(self, class1: str, class2: str):
        pass
    
    def updateAttributesBox(self, class1: str):
        pass
