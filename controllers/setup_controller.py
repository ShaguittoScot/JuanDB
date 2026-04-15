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
        host     = self.view.txt_host.text().strip()
        port_str = self.view.txt_port.text().strip()
        user     = self.view.txt_dbuser.text().strip()
        pwd      = self.view.txt_dbpass.text()
        app_name = self.view.txt_appuser.text().strip()
        app_role = self.view.txt_approle.text().strip()

        # ── Validaciones de formulario ————————————————————————————————————————
        if not host:
            self.view.show_error("El campo 'Host' es obligatorio.")
            return

        if not port_str:
            self.view.show_error("El campo 'Puerto' es obligatorio.")
            return

        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                raise ValueError()
        except ValueError:
            self.view.show_error("El puerto debe ser un número válido (1 – 65535).")
            return

        if not user:
            self.view.show_error("El campo 'Usuario' es obligatorio.")
            return

        if not app_name:
            self.view.show_error("El campo 'Tu nombre' es obligatorio.")
            return

        if not app_role:
            self.view.show_error("El campo 'Cargo / Rol' es obligatorio.")
            return

        # ── Intento de conexión ——————————————————————————————————————————————
        self.view.btn_save.setText("Conectando...")
        self.view.btn_save.setEnabled(False)
        self.view.clear_error()

        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=pwd,
                connection_timeout=8,
                use_pure=True,
            )
            conn.close()

            # Éxito — guardar y continuar
            data = {
                "host":     host,
                "port":     str(port),
                "user":     user,
                "password": pwd,
                "app_user": app_name,
                "app_role": app_role,
            }
            if ConfigService.save_config(data):
                self.setup_completed.emit()
            else:
                self._reset_btn()
                self.view.show_error("No se pudo guardar la configuración en disco.")

        except mysql.connector.errors.InterfaceError:
            self._reset_btn()
            self.view.show_error(
                f"No se puede conectar a {host}:{port}. "
                "Verifica que el servidor esté activo y el puerto sea correcto."
            )
        except mysql.connector.errors.ProgrammingError:
            self._reset_btn()
            self.view.show_error(
                "Acceso denegado — verifica el usuario y la contraseña."
            )
        except mysql.connector.errors.DatabaseError as e:
            self._reset_btn()
            self.view.show_error(f"Error del servidor: {e.msg}")
        except Exception as e:
            self._reset_btn()
            msg = str(e)
            if "timed out" in msg.lower() or "timeout" in msg.lower():
                self.view.show_error(
                    f"Tiempo de espera agotado al conectar a {host}:{port}."
                )
            else:
                self.view.show_error(f"No se pudo conectar: {msg[:120]}")

    def _reset_btn(self):
        self.view.btn_save.setText("Guardar y conectar")
        self.view.btn_save.setEnabled(True)
