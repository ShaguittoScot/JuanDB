from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class ImportExportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Tarjeta principal
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(16)

        tag = QLabel("IMPORTAR Y EXPORTAR DATOS")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 7, QFont.Weight.Bold))

        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(40, 3)

        desc = QLabel("Transfiere información entre tus tablas y archivos locales fácilmente.\nRecuerda que para la importación las columnas del archivo deben coincidir con la Base de Datos.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Georgia", 11))
        desc.setWordWrap(True)

        # Split: Export | Import
        split_layout = QHBoxLayout()
        split_layout.setSpacing(40)
        
        col_exp = self._build_export_column()
        col_imp = self._build_import_column()
        
        vdiv = QFrame()
        vdiv.setFixedWidth(1)
        vdiv.setStyleSheet("background-color: #2A1E3A;")
        
        split_layout.addLayout(col_exp, 1)
        split_layout.addWidget(vdiv)
        split_layout.addLayout(col_imp, 1)

        card_layout.addWidget(tag)
        card_layout.addWidget(accent_line)
        card_layout.addSpacing(4)
        card_layout.addWidget(desc)
        card_layout.addSpacing(20)
        card_layout.addLayout(split_layout)
        card_layout.addStretch()

        layout.addWidget(card, 1)

    def _build_export_column(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        title = QLabel("1. Exportar Datos")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #FF2E88;")
        
        self.combo_db_exp = self._create_combo()
        self.combo_table_exp = self._create_combo()
        self.combo_format_exp = self._create_combo(["CSV", "JSON"])
        
        path_layout = QHBoxLayout()
        self.txt_path_exp = QLineEdit()
        self.txt_path_exp.setReadOnly(True)
        self.txt_path_exp.setPlaceholderText("Ruta de destino...")
        self.btn_browse_exp = QPushButton("Examinar")
        self.btn_browse_exp.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        path_layout.addWidget(self.txt_path_exp, 1)
        path_layout.addWidget(self.btn_browse_exp)
        
        self.lbl_msg_exp = QLabel("")
        self.lbl_msg_exp.setFont(QFont("Segoe UI", 9))
        
        self.btn_export = QPushButton("Exportar Archivo")
        self.btn_export.setObjectName("btnPrimary")
        self.btn_export.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_export.setFixedHeight(40)
        
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Base de Datos Origen:"))
        layout.addWidget(self.combo_db_exp)
        layout.addWidget(QLabel("Tabla a Exportar:"))
        layout.addWidget(self.combo_table_exp)
        layout.addWidget(QLabel("Formato:"))
        layout.addWidget(self.combo_format_exp)
        layout.addWidget(QLabel("Dónde guardar:"))
        layout.addLayout(path_layout)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_msg_exp)
        layout.addWidget(self.btn_export)
        layout.addStretch()
        
        return layout

    def _build_import_column(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(12)
        
        title = QLabel("2. Importar Datos")
        title.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        title.setStyleSheet("color: #A78BFA;")
        
        self.combo_format_imp = self._create_combo(["CSV", "JSON"])
        
        path_layout = QHBoxLayout()
        self.txt_path_imp = QLineEdit()
        self.txt_path_imp.setReadOnly(True)
        self.txt_path_imp.setPlaceholderText("Seleccionar archivo...")
        self.btn_browse_imp = QPushButton("Examinar")
        self.btn_browse_imp.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        path_layout.addWidget(self.txt_path_imp, 1)
        path_layout.addWidget(self.btn_browse_imp)

        self.combo_db_imp = self._create_combo()
        self.combo_table_imp = self._create_combo()
        
        self.lbl_msg_imp = QLabel("")
        self.lbl_msg_imp.setFont(QFont("Segoe UI", 9))
        
        self.btn_import = QPushButton("Importar Archivo")
        self.btn_import.setObjectName("btnPrimary")
        self.btn_import.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_import.setFixedHeight(40)
        self.btn_import.setStyleSheet("background-color: #8A2BE2;") # purple
        
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Formato Origen:"))
        layout.addWidget(self.combo_format_imp)
        layout.addWidget(QLabel("Archivo Local:"))
        layout.addLayout(path_layout)
        layout.addWidget(QLabel("Base de Datos Destino:"))
        layout.addWidget(self.combo_db_imp)
        layout.addWidget(QLabel("Tabla Destino:"))
        layout.addWidget(self.combo_table_imp)
        layout.addSpacing(10)
        layout.addWidget(self.lbl_msg_imp)
        layout.addWidget(self.btn_import)
        layout.addStretch()
        
        return layout

    def _create_combo(self, items=None) -> QComboBox:
        combo = QComboBox()
        combo.setFixedHeight(34)
        if items:
            combo.addItems(items)
        return combo
