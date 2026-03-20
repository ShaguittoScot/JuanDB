from PyQt6.QtCore import QObject, QThread, pyqtSignal
from services.backup_service import BackupService
from services.db_service import get_databases
from PyQt6.QtWidgets import QFileDialog

class BackupWorker(QThread):
    finished = pyqtSignal(str)   # Enviará el filepath al terminar
    error = pyqtSignal(str)      # Enviará mensaje de error

    def __init__(self, db_name: str, dest_dir: str):
        super().__init__()
        self.db_name = db_name
        self.dest_dir = dest_dir

    def run(self):
        try:
            filepath = BackupService.create_backup(self.db_name, self.dest_dir)
            self.finished.emit(filepath)
        except Exception as e:
            self.error.emit(str(e))

class BackupController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.worker = None

        # Conectar señales de la vista
        self.view.btn_select_dir.clicked.connect(self.select_directory)
        self.view.btn_backup.clicked.connect(self.start_backup)
        self.view.btn_refresh.clicked.connect(self.load_databases)

        # Cargar datos iniciales
        self.load_databases()

    def load_databases(self):
        self.view.combo_db.clear()
        self.view.log_message("Consultando bases de datos...")
        
        dbs = get_databases()
        
        valid_dbs = []
        for db in dbs:
            # db is usually a tuple like ('information_schema',) o string the error
            if isinstance(db, tuple) and len(db) > 0:
                valid_dbs.append(db[0])
            elif isinstance(db, str):
                self.view.log_message(f"Error o Sistema: {db}")
                
        if valid_dbs:
            self.view.combo_db.addItems(valid_dbs)
            self.view.log_message(f"{len(valid_dbs)} Bases de datos cargadas.")
        else:
            self.view.log_message("⚠ No se encontraron bases de datos o falló la conexión.")

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self.view, "Seleccionar Directorio")
        if dir_path:
            self.view.path_input.setText(dir_path)

    def start_backup(self):
        db_name = self.view.combo_db.currentText()
        dest_dir = self.view.path_input.text().strip()

        if not db_name:
            self.view.log_message("❌ Error: Seleccione una base de datos.")
            return

        if not dest_dir:
            self.view.log_message("❌ Error: Seleccione un directorio destino.")
            return

        self.view.log_message(f"⌛ Iniciando copia de seguridad para '{db_name}'...")
        self.view.log_message("Por favor, espere...")
        self.view.btn_backup.setEnabled(False)
        self.view.btn_refresh.setEnabled(False)

        self.worker = BackupWorker(db_name, dest_dir)
        self.worker.finished.connect(self.on_backup_success)
        self.worker.error.connect(self.on_backup_error)
        self.worker.start()

    def on_backup_success(self, filepath):
        self.view.log_message(f"✅ ¡Copia exitosa!\nGuardada en: {filepath}")
        self.view.btn_backup.setEnabled(True)
        self.view.btn_refresh.setEnabled(True)

    def on_backup_error(self, error_msg):
        self.view.log_message(f"❌ Error al crear la copia:\n{error_msg}")
        self.view.btn_backup.setEnabled(True)
        self.view.btn_refresh.setEnabled(True)
