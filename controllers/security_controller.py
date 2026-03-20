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
        
        self.view.btn_refresh.clicked.connect(self.load_users)
        self.view.btn_create.clicked.connect(self.create_user)
        self.view.btn_delete.clicked.connect(self.delete_user)
        
        self.load_users()

    def load_users(self):
        self.view.table.setRowCount(0)
        
        self.fetch_worker = FetchUsersWorker()
        self.fetch_worker.finished.connect(self.on_users_loaded)
        self.fetch_worker.error.connect(self.on_error)
        self.fetch_worker.start()

    def on_users_loaded(self, users):
        self.view.table.setRowCount(len(users))
        for row, u in enumerate(users):
            user_item = QTableWidgetItem(u.get("User", ""))
            host_item = QTableWidgetItem(u.get("Host", ""))
            self.view.table.setItem(row, 0, user_item)
            self.view.table.setItem(row, 1, host_item)

    def on_error(self, err):
        print(f"Error cargando usuarios: {err}")

    def create_user(self):
        user = self.view.txt_user.text().strip()
        host = self.view.txt_host.text().strip()
        pwd = self.view.txt_pass.text().strip()

        if not user or not pwd:
            self.view.lbl_msg.setText("⚠ Faltan campos usuario/contraseña.")
            self.view.lbl_msg.setStyleSheet("color: #FF4444;")
            return
            
        host = host if host else "%"
        
        self.view.btn_create.setEnabled(False)
        self.view.lbl_msg.setText("⏳ Creando cuenta...")
        self.view.lbl_msg.setStyleSheet("color: #A78BFA;")

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
            self.action_worker = ActionWorker("delete", user, host)
            self.action_worker.finished.connect(self.on_action_done)
            self.action_worker.start()

    def on_action_done(self, success, msg):
        self.view.btn_create.setEnabled(True)
        if success:
            self.view.lbl_msg.setText(f"✅ {msg}")
            self.view.lbl_msg.setStyleSheet("color: #10B981;")
            self.view.txt_user.clear()
            self.view.txt_pass.clear()
            self.load_users()
        else:
            self.view.lbl_msg.setText(f"❌ {msg}")
            self.view.lbl_msg.setStyleSheet("color: #FF4444;")
