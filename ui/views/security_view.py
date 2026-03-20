from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QPushButton, QAbstractItemView, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class SecurityView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(16)

        tag = QLabel("SEGURIDAD Y CONTROL DE ACCESO")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 7, QFont.Weight.Bold))

        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(40, 3)

        desc = QLabel("Administra las cuentas de usuario de la instancia de base de datos MySQL.\nPuedes añadir usuarios o revocarles el alcance desde esta consola.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Georgia", 11))
        desc.setWordWrap(True)

        split_layout = QHBoxLayout()
        split_layout.setSpacing(40)
        
        # Lado izquierdo (Tabla)
        table_layout = QVBoxLayout()
        table_layout.setSpacing(12)
        lbl_list = QLabel("Usuarios Actuales")
        lbl_list.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_list.setStyleSheet("color: #FF2E88;")
        
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Usuario", "Host (Origen)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0B0712;
                color: #e2e8f0;
                border: 1px solid #3B2A52;
                border-radius: 6px;
                gridline-color: #3B2A52;
            }
            QHeaderView::section {
                background-color: #120A1C;
                color: #A78BFA;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #3B2A52;
            }
            QTableWidget::item:selected {
                background-color: #FF2E88;
                color: white;
            }
        """)
        
        self.btn_delete = QPushButton("Eliminar Seleccionado")
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_delete.setFixedHeight(34)
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid #FF4444;
                color: #FF4444;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF4444;
                color: white;
            }
            QPushButton:disabled {
                border: 1px solid #555;
                color: #555;
            }
        """)
        self.btn_delete.setEnabled(False) # Solo activo si hay algo seleccionado

        self.btn_refresh = QPushButton("Refrescar")
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh.setFixedHeight(34)
        self.btn_refresh.setStyleSheet("""
            QPushButton {
                background-color: #3B2A52;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5D3F7D;
            }
        """)

        btn_box = QHBoxLayout()
        btn_box.addWidget(self.btn_refresh)
        btn_box.addWidget(self.btn_delete)

        table_layout.addWidget(lbl_list)
        table_layout.addWidget(self.table)
        table_layout.addLayout(btn_box)

        # Lado derecho (Formulario Alta)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(16)
        lbl_new = QLabel("Crear Nueva Cuenta")
        lbl_new.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        lbl_new.setStyleSheet("color: #A78BFA;")

        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("Nombre de usuario")
        self.txt_user.setFixedHeight(36)
        self._apply_input_style(self.txt_user)
        
        self.txt_host = QLineEdit()
        self.txt_host.setText("%") # default local/remoto general
        self.txt_host.setPlaceholderText("Host (ej. localhost o %)")
        self.txt_host.setFixedHeight(36)
        self._apply_input_style(self.txt_host)
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Contraseña (secreta)")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass.setFixedHeight(36)
        self._apply_input_style(self.txt_pass)

        self.btn_create = QPushButton("Dar de Alta Usuario")
        self.btn_create.setObjectName("btnPrimary")
        self.btn_create.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_create.setFixedHeight(40)
        
        self.lbl_msg = QLabel("")
        self.lbl_msg.setFont(QFont("Segoe UI", 9))
        self.lbl_msg.setWordWrap(True)

        form_layout.addWidget(lbl_new)
        form_layout.addWidget(QLabel("Usuario:"))
        form_layout.addWidget(self.txt_user)
        form_layout.addWidget(QLabel("Host Autorizado:"))
        form_layout.addWidget(self.txt_host)
        form_layout.addWidget(QLabel("Credencial:"))
        form_layout.addWidget(self.txt_pass)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.lbl_msg)
        form_layout.addWidget(self.btn_create)
        form_layout.addStretch()

        vdiv = QFrame()
        vdiv.setFixedWidth(1)
        vdiv.setStyleSheet("background-color: #2A1E3A;")
        
        split_layout.addLayout(table_layout, 2)
        split_layout.addWidget(vdiv)
        split_layout.addLayout(form_layout, 1)

        card_layout.addWidget(tag)
        card_layout.addWidget(accent_line)
        card_layout.addSpacing(4)
        card_layout.addWidget(desc)
        card_layout.addSpacing(20)
        card_layout.addLayout(split_layout)
        card_layout.addStretch()

        layout.addWidget(card, 1)

        # Conectar selección para habilitar borrar
        self.table.itemSelectionChanged.connect(self._on_table_select)

    def _on_table_select(self):
        items = self.table.selectedItems()
        self.btn_delete.setEnabled(len(items) > 0)

    def _apply_input_style(self, w: QLineEdit):
        w.setStyleSheet("""
            QLineEdit {
                background-color: #0B0712;
                border: 1px solid #3B2A52;
                border-radius: 4px;
                padding: 0px 10px;
                color: #F3E8FF;
            }
            QLineEdit:focus {
                border: 1px solid #A78BFA;
            }
        """)
