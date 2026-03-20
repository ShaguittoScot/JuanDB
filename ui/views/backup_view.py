from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QLineEdit, QTextEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class BackupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Tarjeta principal (Reusando estilos de ModuleView)
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(16)

        tag = QLabel("COPIAS DE SEGURIDAD")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 7, QFont.Weight.Bold))

        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(40, 3)

        desc = QLabel("Exporta y respalda tus bases de datos de forma segura.\nSelecciona una base de datos y un directorio de destino para generar el archivo .sql.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Georgia", 11))
        desc.setWordWrap(True)

        # Contenedor de Formulario
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)
        
        # Fila 1: Seleccionar base de datos
        db_row = QHBoxLayout()
        db_label = QLabel("Base de Datos:")
        db_label.setFont(QFont("Segoe UI", 10))
        db_label.setFixedWidth(120)
        
        self.combo_db = QComboBox()
        self.combo_db.setFont(QFont("Segoe UI", 10))
        self.combo_db.setFixedHeight(32)
        
        self.btn_refresh = QPushButton("↻ Actualizar")
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh.setFixedHeight(32)
        
        db_row.addWidget(db_label)
        db_row.addWidget(self.combo_db, 1)
        db_row.addWidget(self.btn_refresh)
        
        # Fila 2: Seleccionar directorio
        dir_row = QHBoxLayout()
        dir_label = QLabel("Destino:")
        dir_label.setFont(QFont("Segoe UI", 10))
        dir_label.setFixedWidth(120)
        
        self.path_input = QLineEdit()
        self.path_input.setFont(QFont("Segoe UI", 10))
        self.path_input.setFixedHeight(32)
        self.path_input.setPlaceholderText("Directorio para guardar el archivo...")
        self.path_input.setReadOnly(True)
        
        self.btn_select_dir = QPushButton("Examinar...")
        self.btn_select_dir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_select_dir.setFixedHeight(32)
        
        dir_row.addWidget(dir_label)
        dir_row.addWidget(self.path_input, 1)
        dir_row.addWidget(self.btn_select_dir)

        # Fila 3: Botón de respaldo principal
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        self.btn_backup = QPushButton("Crear Copia de Seguridad")
        self.btn_backup.setObjectName("btnPrimary")
        self.btn_backup.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_backup.setFixedSize(220, 42)
        btn_row.addWidget(self.btn_backup)
        
        form_layout.addLayout(db_row)
        form_layout.addLayout(dir_row)
        form_layout.addLayout(btn_row)

        # Consola/Log
        self.log_area = QTextEdit()
        self.log_area.setObjectName("logArea")
        self.log_area.setReadOnly(True)
        self.log_area.setFont(QFont("Courier New", 9))
        self.log_area.setMinimumHeight(150)
        
        card_layout.addWidget(tag)
        card_layout.addWidget(accent_line)
        card_layout.addSpacing(4)
        card_layout.addWidget(desc)
        card_layout.addSpacing(16)
        card_layout.addLayout(form_layout)
        card_layout.addSpacing(16)
        
        log_label = QLabel("Registro del proceso:")
        log_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        log_label.setStyleSheet("color: #A78BFA;")
        
        card_layout.addWidget(log_label)
        card_layout.addWidget(self.log_area, 1)

        layout.addWidget(card, 1)

    def log_message(self, msg: str):
        self.log_area.append(msg)
        # Scroll to bottom
        scrollbar = self.log_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
