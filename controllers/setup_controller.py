from PyQt6.QtCore import QObject, pyqtSignal
from services.config_service import ConfigService
import mysql.connector

class SetupController(QObject):
    setup_completed = pyqtSignal()

    def __init__(self, view):
        super().__init__()
        self.view = view
        self.view.btn_save.clicked.connect(self.process_setup)

    def process_setup(self):
        host = self.view.txt_host.text().strip()
        port = self.view.txt_port.text().strip()
        user = self.view.txt_dbuser.text().strip()
        pwd = self.view.txt_dbpass.text().strip()
        app_name = self.view.txt_appuser.text().strip()
        app_role = self.view.txt_approle.text().strip()

        if not all([host, port, user, app_name, app_role]):
            self.view.show_error("Por favor completa los campos obligatorios.")
            return

        # Probar conexión temporal
        self.view.btn_save.setText("Conectando...")
        self.view.btn_save.setEnabled(False)
        self.view.clear_error()

        try:
            # Probamos conexión a MySQL
            conn = mysql.connector.connect(
                host=host,
                port=int(port),
                user=user,
                password=pwd,
                use_pure=True
            )
            conn.close()

            # Conexión exitosa, guardar JSON
            data = {
                "host": host,
                "port": port,
                "user": user,
                "password": pwd,
                "app_user": app_name,
                "app_role": app_role
            }
            if ConfigService.save_config(data):
                self.setup_completed.emit()
            else:
                self.view.show_error("No se pudo guardar la configuración en disco.")
                self.view.btn_save.setText("Guardar y Conectar")
                self.view.btn_save.setEnabled(True)

        except Exception as e:
            self.view.show_error(f"Fallo conexión BD: {str(e)}")
            self.view.btn_save.setText("Guardar y Conectar")
            self.view.btn_save.setEnabled(True)
