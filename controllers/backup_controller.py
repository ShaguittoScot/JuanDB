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

class RestoreWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(str)

    def __init__(self, db_name, filepaths: list):
        super().__init__()
        self.db_name = db_name
        self.filepaths = filepaths

    def run(self):
        try:
            import os
            from services.backup_service import BackupService
            
            if self.db_name:
                self.progress.emit(f"Preparando BD: {self.db_name}...")
                BackupService.create_database_if_not_exists(self.db_name)
                
            for fp in self.filepaths:
                if fp:
                    self.progress.emit(f"Procesando: {os.path.basename(fp)}")
                    BackupService.restore_backup(self.db_name, fp)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class BackupController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.worker = None
        self.restore_worker = None

        # Conectar señales de la vista
        self.view.btn_select_dir.clicked.connect(self.select_directory)
        self.view.btn_backup.clicked.connect(self.start_backup)
        self.view.btn_refresh.clicked.connect(self.load_databases)
        
        # Conexiones para restauración
        self.view.btn_select_schema.clicked.connect(self.select_schema_file)
        self.view.btn_select_data.clicked.connect(self.select_data_file)
        self.view.btn_restore.clicked.connect(self.start_restore)
        self.view.btn_refresh_restore.clicked.connect(self.load_databases)

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
            self.view.combo_db_restore.clear()
            self.view.combo_db_restore.addItem("(Ninguna - Restaurar Global)")
            self.view.combo_db_restore.addItems(valid_dbs)
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

    def select_schema_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar Archivo SQL (Único/Esquema)", "", "SQL Files (*.sql)")
        if file_path:
            self.view.schema_input.setText(file_path)

    def select_data_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar Archivo de Datos", "", "SQL Files (*.sql)")
        if file_path:
            self.view.data_input.setText(file_path)

    def start_restore(self):
        db_name = self.view.combo_db_restore.currentText()
        schema_path = self.view.schema_input.text().strip()
        data_path = self.view.data_input.text().strip()
        
        is_split = self.view.combo_mode_restore.currentIndex() == 1

        if not db_name:
            self.view.log_message("❌ Error: Escriba o seleccione una BD destino (o elija 'Ninguna').")
            return
            
        if db_name == "(Ninguna - Restaurar Global)":
            db_name = None

        filepaths = []
        if is_split:
            if schema_path: filepaths.append(schema_path)
            if data_path: filepaths.append(data_path)
            if not filepaths:
                self.view.log_message("❌ Error: Seleccione al menos un archivo (Esquema o Datos) para restaurar.")
                return
        else:
            if not schema_path:
                self.view.log_message("❌ Error: Seleccione un archivo .sql para restaurar.")
                return
            filepaths.append(schema_path)

        self.view.log_message(f"⌛ Iniciando restauración en '{db_name or 'Global'}'...")
        self.view.log_message("Por favor, espere...")
        self.view.btn_restore.setEnabled(False)
        self.view.btn_refresh_restore.setEnabled(False)
        self.view.progress_bar_restore.setRange(0, 0)
        self.view.progress_bar_restore.setVisible(True)

        self.restore_worker = RestoreWorker(db_name, filepaths)
        self.restore_worker.progress.connect(lambda msg: self.view.log_message(f"↳ {msg}"))
        self.restore_worker.finished.connect(self.on_restore_success)
        self.restore_worker.error.connect(self.on_restore_error)
        self.restore_worker.start()

    def on_restore_success(self):
        self.view.progress_bar_restore.setVisible(False)
        self.view.log_message("✅ ¡Base de datos restaurada exitosamente!")
        self.view.btn_restore.setEnabled(True)
        self.view.btn_refresh_restore.setEnabled(True)

    def on_restore_error(self, error_msg):
        self.view.progress_bar_restore.setVisible(False)
        self.view.log_message(f"❌ Error al restaurar la copia:\n{error_msg}")
        self.view.btn_restore.setEnabled(True)
        self.view.btn_refresh_restore.setEnabled(True)
