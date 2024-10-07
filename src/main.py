import model.editor_model
import view.ui_cli
import controller.editor_controller

if __name__ == '__main__':
    editor = model.editor_model.Editor()
    # TODO: accept command line argument for entering CLI model
    ui = view.ui_cli.CLI()
    controller = controller.editor_controller.EditorController(ui, editor)
    ui.uiRun(controller)
