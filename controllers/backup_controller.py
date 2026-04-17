from PyQt6.QtCore import QObject, QThread, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from services.backup_service import BackupService
from services.db_service import get_databases, get_tables, get_table_permissions
from utils.database_sanitizer import DatabaseSanitizer
import subprocess
import os

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
        self.last_backup_path = None  # Para guardar la ruta del último backup

        # Conectar señales de la vista
        self.view.btn_select_dir.clicked.connect(self.select_directory)
        self.view.btn_backup.clicked.connect(self.start_backup)
        self.view.btn_refresh.clicked.connect(self.load_databases)
        self.view.combo_db.currentIndexChanged.connect(self.check_selection_permissions)
        
        # Conectar botón de abrir carpeta
        self.view.btn_open_folder.clicked.connect(self.open_folder)
        self.view.btn_open_result.clicked.connect(self.open_result_folder)
        
        # Conectar cambios en la ruta para habilitar/deshabilitar botones
        self.view.path_input.textChanged.connect(self.update_folder_button_state)
        
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
        
        raw_names = []
        for db in dbs:
            if isinstance(db, tuple) and len(db) > 0:
                raw_names.append(db[0])
            elif isinstance(db, str):
                self.view.log_message(f"Error o Sistema: {db}")
                
        # Aplicar saneado (Modo Avanzado lo ignora)
        valid_dbs = DatabaseSanitizer.filter_databases(raw_names)
        
        if valid_dbs:
            self.view.combo_db.addItems(valid_dbs)
            self.view.combo_db_restore.clear()
            self.view.combo_db_restore.addItem("(Ninguna - Restaurar Global)")
            self.view.combo_db_restore.addItems(valid_dbs)
            self.view.log_message(f"{len(valid_dbs)} Bases de datos cargadas.")
            
            # Auto-seleccionar si solo hay una
            if len(valid_dbs) == 1:
                self.view.combo_db.setCurrentIndex(0)
                self.view.combo_db_restore.setCurrentIndex(1)
        else:
            self.view.combo_db.setPlaceholderText("No hay bases de datos de usuario disponibles")
            self.view.log_message("⚠ No se encontraron bases de datos o falló la conexión.")

    def select_directory(self):
        """Selecciona directorio de destino para backup usando diálogo nativo del sistema."""
        dir_path = QFileDialog.getExistingDirectory(
            self.view,
            "Seleccionar Carpeta de Backup",
            "",
            options=QFileDialog.Option.ReadOnly
        )
        if dir_path:
            self.view.path_input.setText(dir_path)

    def check_selection_permissions(self):
        """Verifica si la base de datos seleccionada es de solo lectura."""
        db_name = self.view.combo_db.currentText()
        if not db_name or db_name.startswith("No hay"):
            self.view.lbl_permission_note.setVisible(False)
            return

        try:
            # Obtenemos las tablas para verificar el nivel general
            tables_raw = get_tables(db_name)
            valid_tables = [t[0] for t in tables_raw if isinstance(t, tuple)]
            
            if not valid_tables:
                self.view.lbl_permission_note.setVisible(False)
                return

            perms = get_table_permissions(db_name, valid_tables)
            
            # Si todas las tablas son <= 1 (Amarillo o Rojo), es "Solo lectura" o "Denegado"
            is_readonly = all(level <= 1 for level in perms.values())
            
            if is_readonly:
                self.view.lbl_permission_note.setText("Acceso limitado: Solo lectura")
                self.view.lbl_permission_note.setVisible(True)
            else:
                self.view.lbl_permission_note.setVisible(False)
                
        except Exception as e:
            print(f"[BackupController] Error verificando permisos: {e}")
            self.view.lbl_permission_note.setVisible(False)

    def start_backup(self):
        db_name = self.view.combo_db.currentText()
        dest_dir = self.view.path_input.text().strip()

        if not db_name:
            self.view.log_message("❌ Error: Seleccione una base de datos.")
            return

        # Validación de seguridad del Sanitizer
        if not DatabaseSanitizer.is_safe_database(db_name):
            QMessageBox.critical(self.view, "Acceso Denegado", 
                                f"No se puede realizar backup de la base de datos de sistema '{db_name}' sin Modo Avanzado.")
            self.view.log_message(f"❌ Abortado: '{db_name}' es una base de datos protegida.", "error")
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
        self.view.btn_backup.setEnabled(True)
        self.view.btn_refresh.setEnabled(True)
        self.last_backup_path = filepath  # Guardar la ruta para el botón "Ver archivo"
        self.view.btn_open_result.setEnabled(True)
        self.view.log_message(f"✅ ¡Copia exitosa!\nGuardada en: {filepath}")

    def on_backup_error(self, error_msg):
        self.view.btn_backup.setEnabled(True)
        self.view.btn_refresh.setEnabled(True)
        self.view.log_message(f"❌ Error al crear la copia:\n{error_msg}")

    def select_schema_file(self):
        """Selecciona archivo SQL de esquema usando diálogo nativo del sistema."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Seleccionar Archivo SQL (Esquema)",
            "",
            "SQL Files (*.sql);;All Files (*)",
            options=QFileDialog.Option.ReadOnly
        )
        if file_path:
            self.view.schema_input.setText(file_path)

    def select_data_file(self):
        """Selecciona archivo SQL de datos usando diálogo nativo del sistema."""
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,
            "Seleccionar Archivo de Datos",
            "",
            "SQL Files (*.sql);;All Files (*)",
            options=QFileDialog.Option.ReadOnly
        )
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
        
        if db_name and not DatabaseSanitizer.is_safe_database(db_name):
            QMessageBox.critical(self.view, "Acceso Denegado", 
                                f"No se permite restaurar sobre la base de datos de sistema '{db_name}'.")
            return

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

    def update_folder_button_state(self):
        """Habilita/deshabilita el botón de abrir carpeta según si hay ruta."""
        has_path = bool(self.view.path_input.text().strip())
        self.view.btn_open_folder.setEnabled(has_path)

    def open_folder(self):
        """Abre el Explorador de Archivos en la ruta seleccionada."""
        folder_path = self.view.path_input.text().strip()
        if not folder_path:
            return

        try:
            # Convertir / a \ para Windows
            folder_path = folder_path.replace("/", "\\")
            
            if os.path.exists(folder_path):
                # Usar explorer para abrir la carpeta
                subprocess.Popen(f'explorer "{folder_path}"')
            else:
                self.view.log_message(f"⚠ La carpeta no existe: {folder_path}")
        except Exception as e:
            self.view.log_message(f"❌ Error al abrir carpeta: {str(e)}")

    def open_result_folder(self):
        """Abre el Explorador de Archivos mostrando el archivo generado."""
        if not self.last_backup_path:
            return

        try:
            # Convertir / a \ para Windows
            filepath = self.last_backup_path.replace("/", "\\")
            
            if os.path.exists(filepath):
                # Usar explorer /select para resaltar el archivo
                subprocess.Popen(f'explorer /select, "{filepath}"')
            else:
                self.view.log_message(f"⚠ El archivo no existe: {filepath}")
        except Exception as e:
            self.view.log_message(f"❌ Error al abrir archivo: {str(e)}")
