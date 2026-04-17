from PyQt6.QtCore import QObject, QThread, pyqtSignal
from services.import_export_service import ImportExportService
from services.db_service import get_databases, get_tables, get_table_permissions
from utils.database_sanitizer import DatabaseSanitizer
from PyQt6.QtWidgets import QMessageBox
import subprocess
import os

class ExportWorker(QThread):
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, db, table, fmt, path):
        super().__init__()
        self.db = db
        self.table = table
        self.fmt = fmt
        self.path = path

    def run(self):
        try:
            count = ImportExportService.export_data(self.db, self.table, self.fmt, self.path)
            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))

class ImportWorker(QThread):
    finished = pyqtSignal(int)
    error = pyqtSignal(str)

    def __init__(self, db, table, fmt, path):
        super().__init__()
        self.db = db
        self.table = table
        self.fmt = fmt
        self.path = path

    def run(self):
        try:
            count = ImportExportService.import_data(self.db, self.table, self.fmt, self.path)
            self.finished.emit(count)
        except Exception as e:
            self.error.emit(str(e))

class ImportExportController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.last_export_path = None  # Para guardar la ruta del último archivo exportado
        
        # Conectar señales Exp
        self.view.db_exp.currentTextChanged.connect(self.load_tables_exp)
        self.view.btn_export.clicked.connect(self.process_export)
        
        # Conectar señales Imp
        self.view.db_imp.currentTextChanged.connect(self.load_tables_imp)
        self.view.btn_import.clicked.connect(self.process_import)
        self.view.table_imp.currentIndexChanged.connect(self.check_import_permissions)
        
        # Conectar botón de abrir resultado
        self.view.btn_open_result.clicked.connect(self.open_result_file)
        
        self.load_dbs()

    def load_dbs(self):
        dbs = get_databases()
        raw_names = []
        for db in dbs:
            if isinstance(db, tuple) and len(db) > 0:
                raw_names.append(db[0])
                
        # Filtrar vía Sanitizer (Centralizado)
        valid_dbs = DatabaseSanitizer.filter_databases(raw_names)
        
        self.view.db_exp.clear()
        self.view.db_imp.clear()
        
        if valid_dbs:
            self.view.db_exp.addItems(valid_dbs)
            self.view.db_imp.addItems(valid_dbs)
            
            # Auto-seleccionar si solo hay una
            if len(valid_dbs) == 1:
                self.view.db_exp.setCurrentIndex(0)
                self.view.db_imp.setCurrentIndex(0)
        else:
            # Placeholders si está vacío
            self.view.db_exp.setPlaceholderText("No hay bases de datos de usuario disponibles")
            self.view.db_imp.setPlaceholderText("No hay bases de datos de usuario disponibles")

    def load_tables_exp(self, db_name):
        self.view.table_exp.clear()
        if not db_name: return
        tables = get_tables(db_name)
        for tb in tables:
            if isinstance(tb, tuple) and len(tb) > 0:
                self.view.table_exp.addItem(tb[0])

    def load_tables_imp(self, db_name):
        self.view.table_imp.clear()
        if not db_name: return
        tables = get_tables(db_name)
        for tb in tables:
            if isinstance(tb, tuple) and len(tb) > 0:
                self.view.table_imp.addItem(tb[0])

    def process_export(self):
        db = self.view.db_exp.currentText()
        tb = self.view.table_exp.currentText()
        fmt = self.view.format_exp.currentText()
        path = self.view.file_selector_exp.get_path()
        
        if not all([db, tb, fmt, path]):
            self.view.show_message("export", "⚠ Faltan parámetros.", "error")
            return
            
        # Validación de seguridad del Sanitizer
        if not DatabaseSanitizer.is_safe_database(db):
            QMessageBox.critical(self.view, "Acceso Denegado", 
                                f"No se permite exportar la base de datos de sistema '{db}' sin Modo Avanzado.")
            return
            
        self.view.btn_export.setEnabled(False)
        self.view.show_message("export", "⏳ Exportando datos...", "info")
        
        self.exp_worker = ExportWorker(db, tb, fmt, path)
        self.exp_worker.finished.connect(self.on_exp_done)
        self.exp_worker.error.connect(self.on_exp_error)
        self.exp_worker.start()

    def on_exp_done(self, count):
        self.view.btn_export.setEnabled(True)
        export_path = self.view.file_selector_exp.get_path()
        self.last_export_path = export_path  # Guardar la ruta para el botón "Ver archivo"
        self.view.btn_open_result.setEnabled(True)
        self.view.show_message("export", f"✅ Éxito. {count} fila(s) exportadas.", "success")

    def on_exp_error(self, err):
        self.view.btn_export.setEnabled(True)
        error_msg = str(err)
        
        # Mensajes específicos según el tipo de error
        if "Permission denied" in error_msg or "Permiso denegado" in error_msg:
            self.view.show_message("export", f"❌ Acceso denegado. Verifique permisos en el directorio seleccionado.", "error")
        elif "No such file or directory" in error_msg:
            self.view.show_message("export", f"❌ El directorio no existe o no es accesible.", "error")
        else:
            self.view.show_message("export", f"❌ Error: {error_msg}", "error")
        
        print("Export error:", err)

    def process_import(self):
        db = self.view.db_imp.currentText()
        tb = self.view.table_imp.currentText()
        fmt = self.view.format_imp.currentText()
        path = self.view.file_selector_imp.get_path()
        
        if not all([db, tb, fmt, path]):
            self.view.show_message("import", "⚠ Faltan parámetros.", "error")
            return

        if not DatabaseSanitizer.is_safe_database(db):
            QMessageBox.critical(self.view, "Acceso Denegado", 
                                f"No se permite importar sobre la base de datos de sistema '{db}'.")
            return

        # Validación de permisos individuales por tabla antes de procesar
        perms = get_table_permissions(db, [tb])
        if perms.get(tb, 0) < 2:
            QMessageBox.warning(self.view, "Acceso Restringido",
                                f"No tienes permisos de escritura en la tabla '{tb}'. "
                                "La importación ha sido bloqueada.")
            return
            
        self.view.btn_import.setEnabled(False)
        self.view.show_message("import", "⏳ Importando datos...", "info")
        
        self.imp_worker = ImportWorker(db, tb, fmt, path)
        self.imp_worker.finished.connect(self.on_imp_done)
        self.imp_worker.error.connect(self.on_imp_error)
        self.imp_worker.start()

    def on_imp_done(self, count):
        self.view.btn_import.setEnabled(True)
        self.view.show_message("import", f"✅ Éxito. {count} fila(s) importadas.", "success")

    def on_imp_error(self, err):
        self.view.btn_import.setEnabled(True)
        error_msg = str(err)
        
        # Mensajes específicos según el tipo de error
        if "Permission denied" in error_msg or "Permiso denegado" in error_msg:
            self.view.show_message("import", f"❌ Acceso denegado. Verifique permisos en el archivo.", "error")
        elif "FileNotFoundError" in error_msg or "No such file" in error_msg or "no encontrado" in error_msg.lower():
            self.view.show_message("import", f"❌ Archivo no encontrado o acceso denegado.", "error")
        else:
            self.view.show_message("import", f"❌ Error: {error_msg}", "error")
        
        print("Import error:", err)

    def check_import_permissions(self):
        """Bloquea visualmente el botón de importar si no hay permisos."""
        db = self.view.db_imp.currentText()
        tb = self.view.table_imp.currentText()
        if not db or not tb: return
        
        try:
            perms = get_table_permissions(db, [tb])
            level = perms.get(tb, 0)
            
            can_write = (level == 2)
            self.view.btn_import.setEnabled(can_write)
            
            if not can_write:
                self.view.btn_import.setToolTip("No tienes permisos de escritura en esta tabla")
            else:
                self.view.btn_import.setToolTip("Ejecutar importación")
        except:
            pass

    def open_result_file(self):
        """Abre el Explorador de Archivos mostrando el archivo exportado."""
        if not self.last_export_path:
            return

        try:
            # Convertir / a \ para Windows
            filepath = self.last_export_path.replace("/", "\\")
            
            if os.path.exists(filepath):
                # Usar explorer /select para resaltar el archivo
                subprocess.Popen(f'explorer /select, "{filepath}"')
            else:
                self.view.show_message("export", f"⚠ El archivo no existe: {filepath}", "warning")
        except Exception as e:
            self.view.show_message("export", f"❌ Error al abrir archivo: {str(e)}", "error")
