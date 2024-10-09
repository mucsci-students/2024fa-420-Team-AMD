import model.editor_model
import view.ui_cli
import view.ui_gui
import controller.editor_controller

if __name__ == '__main__':
    editor = model.editor_model.Editor()
    # TODO: accept command line argument for entering CLI model
    ui = view.ui_gui.GUI(None)
    # Bring back CLI in user selection
    #ui = view.ui_cli.CLI()
    controller = controller.editor_controller.EditorController(ui, editor)
    ui.controller = controller
    ui.uiRun()
