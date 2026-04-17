import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.views.setup_view import SetupView
from controllers.setup_controller import SetupController
from services.config_service import ConfigService


def main():
    try:
        app = QApplication(sys.argv)
        app._windows = [] # Para evitar que las ventanas sean recolectadas por el GC

        if not ConfigService.is_setup_completed():
            setup_view = SetupView()
            setup_controller = SetupController(setup_view)
            
            def on_setup_done():
                setup_view.close()
                main_win = MainWindow()
                app._windows.append(main_win)
                main_win.showMaximized()

            setup_controller.setup_completed.connect(on_setup_done)
            setup_view.show()
            app._windows.append(setup_view)
            app._windows.append(setup_controller)
        else:
            window = MainWindow()
            app._windows.append(window)
            window.showMaximized()

        sys.exit(app.exec())

    except Exception as e:
        import traceback
        traceback.print_exc()
        print("ERROR:", e)
        input("Presiona Enter para salir...")


if __name__ == "__main__":
    main()