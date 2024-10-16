import model.editor_model
import view.ui_cli
import view.ui_gui
from controller.editor_controller import EditorController  
import sys

def run_cli(editor):
    ui = view.ui_cli.CLI()  
    controller = EditorController(ui, editor)  
    result = ui.uiRun(controller)  
    return result  

def run_gui(editor):
    ui = view.ui_gui.GUI(None) 
    controller = EditorController(ui, editor)  
    ui.controller = controller 
    ui.uiRun()  

if __name__ == '__main__':
    editor = model.editor_model.Editor()  

    # Default mode is GUI
    ui_mode = 'gui'

    # Check for command-line arguments
    if len(sys.argv) > 2 and sys.argv[1] == '--mode':
        ui_mode = sys.argv[2]

    while True:
        if ui_mode == 'cli':
            # Run CLI and check if we need to switch
            result = run_cli(editor)
            if result == 'switch_to_gui':
                ui_mode = 'gui'  # Switch to GUI
            else:
                break  
        else:
            # Run GUI
            run_gui(editor)
            break
