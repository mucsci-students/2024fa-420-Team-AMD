from model.app_model import AppDirector  
import sys

if __name__ == '__main__':
    director = AppDirector()

    # Default mode is GUI
    ui_mode = 'gui'

    # Check for command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        ui_mode = 'cli'

    while True:
        if ui_mode == 'cli':
            # Run CLI and check if we need to switch
            app = director.makeAppCLI()
            result = app.run()
            if result == 'switch_to_gui':
                ui_mode = 'gui'  # Switch to GUI
            else:
                break  
        else:
            # Run GUI
            app = director.makeAppGUI()
            app.run()
            break
