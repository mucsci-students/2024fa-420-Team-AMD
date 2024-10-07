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
