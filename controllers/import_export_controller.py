from PyQt6.QtCore import QObject, QThread, pyqtSignal
from services.import_export_service import ImportExportService
from services.db_service import get_databases, get_tables
from PyQt6.QtWidgets import QFileDialog

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
        
        # Conectar señales Exp
        self.view.db_exp.currentTextChanged.connect(self.load_tables_exp)
        self.view.file_selector_exp.browse_btn.clicked.connect(self.browse_export_path)
        self.view.btn_export.clicked.connect(self.process_export)
        
        # Conectar señales Imp
        self.view.db_imp.currentTextChanged.connect(self.load_tables_imp)
        self.view.file_selector_imp.browse_btn.clicked.connect(self.browse_import_path)
        self.view.btn_import.clicked.connect(self.process_import)
        
        self.load_dbs()

    def load_dbs(self):
        dbs = get_databases()
        valid_dbs = []
        for db in dbs:
            if isinstance(db, tuple) and len(db) > 0:
                valid_dbs.append(db[0])
                
        self.view.db_exp.clear()
        self.view.db_imp.clear()
        
        if valid_dbs:
            self.view.db_exp.addItems(valid_dbs)
            self.view.db_imp.addItems(valid_dbs)

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

    def browse_export_path(self):
        fmt = self.view.format_exp.currentText()
        filt = "CSV files (*.csv)" if fmt == "CSV" else "JSON files (*.json)"
        
        # Para exportar la carpeta o archivo? En el placeholder dice "Seleccionar carpeta..." pero si el viejo era save_file_name.
        # De igual forma getSaveFileName asume un archivo específico.
        path, _ = QFileDialog.getSaveFileName(self.view, "Guardar Archivo Exportado", "", filt)
        if path:
            self.view.file_selector_exp.set_path(path)

    def browse_import_path(self):
        fmt = self.view.format_imp.currentText()
        filt = "CSV files (*.csv)" if fmt == "CSV" else "JSON files (*.json)"
        path, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar Archivo para Importar", "", filt)
        if path:
            self.view.file_selector_imp.set_path(path)

    def process_export(self):
        db = self.view.db_exp.currentText()
        tb = self.view.table_exp.currentText()
        fmt = self.view.format_exp.currentText()
        path = self.view.file_selector_exp.get_path()
        
        if not all([db, tb, fmt, path]):
            self.view.show_message("export", "⚠ Faltan parámetros.", "error")
            return
            
        self.view.btn_export.setEnabled(False)
        self.view.show_message("export", "⏳ Exportando datos...", "info")
        
        self.exp_worker = ExportWorker(db, tb, fmt, path)
        self.exp_worker.finished.connect(self.on_exp_done)
        self.exp_worker.error.connect(self.on_exp_error)
        self.exp_worker.start()

    def on_exp_done(self, count):
        self.view.btn_export.setEnabled(True)
        self.view.show_message("export", f"✅ Éxito. {count} fila(s) exportadas.", "success")

    def on_exp_error(self, err):
        self.view.btn_export.setEnabled(True)
        self.view.show_message("export", f"❌ Falló exportación.", "error")
        print("Export error:", err)

    def process_import(self):
        db = self.view.db_imp.currentText()
        tb = self.view.table_imp.currentText()
        fmt = self.view.format_imp.currentText()
        path = self.view.file_selector_imp.get_path()
        
        if not all([db, tb, fmt, path]):
            self.view.show_message("import", "⚠ Faltan parámetros.", "error")
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
        self.view.show_message("import", f"❌ Falló importación.", "error")
        print("Import error:", err)
