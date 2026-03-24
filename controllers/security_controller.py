from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from services.security_service import SecurityService

class FetchUsersWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def run(self):
        try:
            users = SecurityService.get_users()
            self.finished.emit(users)
        except Exception as e:
            self.error.emit(str(e))

class ActionWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, action, *args):
        super().__init__()
        self.action = action
        self.args = args

    def run(self):
        try:
            if self.action == "create":
                res = SecurityService.create_user(*self.args)
                self.finished.emit(True, "Usuario creado exitosamente con permisos básicos.")
            elif self.action == "delete":
                res = SecurityService.delete_user(*self.args)
                self.finished.emit(True, "El usuario ha sido eliminado por completo.")
        except Exception as e:
            self.finished.emit(False, str(e))

class SecurityController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        
        # Desconectar los mocks de prueba que el usuario puso en la vista, si existen
        try:
            self.view.btn_refresh.clicked.disconnect()
            self.view.btn_create.clicked.disconnect()
            self.view.btn_delete.clicked.disconnect()
        except TypeError:
            pass
            
        self.view.btn_refresh.clicked.connect(self.load_users)
        self.view.btn_create.clicked.connect(self.create_user)
        self.view.btn_delete.clicked.connect(self.delete_user)
        
        self.load_users()

    def load_users(self):
        self.view.table.setRowCount(0)
        self.view.show_message("Cargando usuarios desde la base de datos...", "info")
        
        self.fetch_worker = FetchUsersWorker()
        self.fetch_worker.finished.connect(self.on_users_loaded)
        self.fetch_worker.error.connect(self.on_error)
        self.fetch_worker.start()

    def on_users_loaded(self, users):
        self.view.table.setRowCount(len(users))
        for row, u in enumerate(users):
            user_item = QTableWidgetItem(u.get("User", ""))
            host_item = QTableWidgetItem(u.get("Host", ""))
            priv_item = QTableWidgetItem("N/A")  # Placeholder para privilegios
            self.view.table.setItem(row, 0, user_item)
            self.view.table.setItem(row, 1, host_item)
            self.view.table.setItem(row, 2, priv_item)
            
        self.view.user_count_label.setText(f"{len(users)} usuarios")
        self.view.show_message("Lista de usuarios actualizada", "success")

    def on_error(self, err):
        print(f"Error cargando usuarios: {err}")
        self.view.show_message(f"Error cargando usuarios: {err}", "error")

    def create_user(self):
        user = self.view.txt_user.text().strip()
        host = self.view.txt_host.text().strip()
        pwd = self.view.txt_pass.text().strip()
        confirm = self.view.txt_confirm_pass.text().strip()

        # Validaciones
        if not user:
            self.view.show_message("❌ El nombre de usuario es obligatorio", "error")
            return
            
        if not host:
            self.view.show_message("❌ El host es obligatorio", "error")
            return
            
        if not pwd:
            self.view.show_message("❌ La contraseña es obligatoria", "error")
            return
            
        if pwd != confirm:
            self.view.show_message("❌ Las contraseñas no coinciden", "error")
            return
            
        if len(pwd) < 6:
            self.view.show_message("⚠️ La contraseña debe tener al menos 6 caracteres", "warning")
            return
            
        # Verificar si ya existe visualmente para no ir a la DB en vano
        for row in range(self.view.table.rowCount()):
            existing_user = self.view.table.item(row, 0).text()
            existing_host = self.view.table.item(row, 1).text()
            if existing_user == user and existing_host == host:
                self.view.show_message(f"❌ El usuario '{user}'@{host} ya existe", "error")
                return

        host = host if host else "%"
        
        self.view.btn_create.setEnabled(False)
        self.view.show_message("⏳ Creando cuenta en la base de datos...", "info")

        self.action_worker = ActionWorker("create", user, pwd, host)
        self.action_worker.finished.connect(self.on_action_done)
        self.action_worker.start()

    def delete_user(self):
        items = self.view.table.selectedItems()
        if not items: return
        
        row = items[0].row()
        user = self.view.table.item(row, 0).text()
        host = self.view.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self.view, "Confirmar Baja",
            f"¿Estás completamente seguro de revocar el acceso y eliminar a '{user}'@'{host}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.view.btn_delete.setEnabled(False)
            self.view.show_message(f"⏳ Eliminando usuario '{user}'@{host}...", "info")
            self.action_worker = ActionWorker("delete", user, host)
            self.action_worker.finished.connect(self.on_action_done)
            self.action_worker.start()

    def on_action_done(self, success, msg):
        self.view.btn_create.setEnabled(True)
        if success:
            self.view.show_message(f"✅ {msg}", "success")
            self.view.txt_user.clear()
            self.view.txt_pass.clear()
            self.view.txt_confirm_pass.clear()
            self.view.chk_grant_priv.setChecked(False)
            self.view.chk_expire_pass.setChecked(False)
            self.load_users()
        else:
            self.view.show_message(f"❌ {msg}", "error")
