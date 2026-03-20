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
        self.view.combo_db_exp.currentTextChanged.connect(self.load_tables_exp)
        self.view.btn_browse_exp.clicked.connect(self.browse_export_path)
        self.view.btn_export.clicked.connect(self.process_export)
        
        # Conectar señales Imp
        self.view.combo_db_imp.currentTextChanged.connect(self.load_tables_imp)
        self.view.btn_browse_imp.clicked.connect(self.browse_import_path)
        self.view.btn_import.clicked.connect(self.process_import)
        
        self.load_dbs()

    def load_dbs(self):
        dbs = get_databases()
        valid_dbs = []
        for db in dbs:
            if isinstance(db, tuple) and len(db) > 0:
                valid_dbs.append(db[0])
                
        self.view.combo_db_exp.clear()
        self.view.combo_db_imp.clear()
        
        if valid_dbs:
            self.view.combo_db_exp.addItems(valid_dbs)
            self.view.combo_db_imp.addItems(valid_dbs)

    def load_tables_exp(self, db_name):
        self.view.combo_table_exp.clear()
        if not db_name: return
        tables = get_tables(db_name)
        for tb in tables:
            if isinstance(tb, tuple) and len(tb) > 0:
                self.view.combo_table_exp.addItem(tb[0])

    def load_tables_imp(self, db_name):
        self.view.combo_table_imp.clear()
        if not db_name: return
        tables = get_tables(db_name)
        for tb in tables:
            if isinstance(tb, tuple) and len(tb) > 0:
                self.view.combo_table_imp.addItem(tb[0])

    def browse_export_path(self):
        fmt = self.view.combo_format_exp.currentText()
        filt = "CSV files (*.csv)" if fmt == "CSV" else "JSON files (*.json)"
        path, _ = QFileDialog.getSaveFileName(self.view, "Guardar Archivo Exportado", "", filt)
        if path:
            self.view.txt_path_exp.setText(path)

    def browse_import_path(self):
        fmt = self.view.combo_format_imp.currentText()
        filt = "CSV files (*.csv)" if fmt == "CSV" else "JSON files (*.json)"
        path, _ = QFileDialog.getOpenFileName(self.view, "Seleccionar Archivo para Importar", "", filt)
        if path:
            self.view.txt_path_imp.setText(path)

    def process_export(self):
        db = self.view.combo_db_exp.currentText()
        tb = self.view.combo_table_exp.currentText()
        fmt = self.view.combo_format_exp.currentText()
        path = self.view.txt_path_exp.text()
        
        if not all([db, tb, fmt, path]):
            self.view.lbl_msg_exp.setText("⚠ Faltan parámetros.")
            self.view.lbl_msg_exp.setStyleSheet("color: #FF4444;")
            return
            
        self.view.btn_export.setEnabled(False)
        self.view.lbl_msg_exp.setText("⏳ Exportando datos...")
        self.view.lbl_msg_exp.setStyleSheet("color: #A78BFA;")
        
        self.exp_worker = ExportWorker(db, tb, fmt, path)
        self.exp_worker.finished.connect(self.on_exp_done)
        self.exp_worker.error.connect(self.on_exp_error)
        self.exp_worker.start()

    def on_exp_done(self, count):
        self.view.btn_export.setEnabled(True)
        self.view.lbl_msg_exp.setText(f"✅ Éxito. {count} fila(s) exportadas.")
        self.view.lbl_msg_exp.setStyleSheet("color: #10B981;")

    def on_exp_error(self, err):
        self.view.btn_export.setEnabled(True)
        self.view.lbl_msg_exp.setText(f"❌ Falló exportación.")
        self.view.lbl_msg_exp.setStyleSheet("color: #FF4444;")
        print("Export error:", err)

    def process_import(self):
        db = self.view.combo_db_imp.currentText()
        tb = self.view.combo_table_imp.currentText()
        fmt = self.view.combo_format_imp.currentText()
        path = self.view.txt_path_imp.text()
        
        if not all([db, tb, fmt, path]):
            self.view.lbl_msg_imp.setText("⚠ Faltan parámetros.")
            self.view.lbl_msg_imp.setStyleSheet("color: #FF4444;")
            return
            
        self.view.btn_import.setEnabled(False)
        self.view.lbl_msg_imp.setText("⏳ Importando datos...")
        self.view.lbl_msg_imp.setStyleSheet("color: #A78BFA;")
        
        self.imp_worker = ImportWorker(db, tb, fmt, path)
        self.imp_worker.finished.connect(self.on_imp_done)
        self.imp_worker.error.connect(self.on_imp_error)
        self.imp_worker.start()

    def on_imp_done(self, count):
        self.view.btn_import.setEnabled(True)
        self.view.lbl_msg_imp.setText(f"✅ Éxito. {count} fila(s) importadas.")
        self.view.lbl_msg_imp.setStyleSheet("color: #10B981;")

    def on_imp_error(self, err):
        self.view.btn_import.setEnabled(True)
        self.view.lbl_msg_imp.setText(f"❌ Falló importación.")
        self.view.lbl_msg_imp.setStyleSheet("color: #FF4444;")
        print("Import error:", err)
