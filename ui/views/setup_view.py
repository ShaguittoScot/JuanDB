from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor

class SetupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JuanDB - Configuración Inicial")
        self.setFixedSize(500, 650)
        self.setStyleSheet("background-color: #0B0712; color: #F3E8FF;")
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Cabecera
        header_lbl = QLabel("Bienvenido a JuanDB")
        header_lbl.setFont(QFont("Georgia", 22, QFont.Weight.Bold))
        header_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_lbl.setProperty("class", "text-accent")

        desc_lbl = QLabel("Por favor, ingresa los datos de conexión al servidor y tu información de perfil. Solo te lo pediremos esta vez.")
        desc_lbl.setFont(QFont("Segoe UI", 10))
        desc_lbl.setWordWrap(True)
        desc_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_lbl.setStyleSheet("color: #A78BFA; margin-bottom: 20px;")

        # --- CONTENEDOR DE CAMPOS ---
        form_frame = QFrame()
        form_frame.setStyleSheet("background-color: #120A1C; border-radius: 12px; border: 1px solid #2A1E3A;")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setContentsMargins(24, 24, 24, 24)
        form_layout.setSpacing(16)

        # Sección: Base de Datos
        lbl_db = QLabel("Conexión a Base de Datos")
        lbl_db.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_db.setStyleSheet("border: none;")

        self.txt_host = self._create_input("Host (ej. localhost):", "localhost")
        self.txt_port = self._create_input("Puerto:", "3306")
        self.txt_dbuser = self._create_input("Usuario DB (ej. root):", "root")
        self.txt_dbpass = self._create_input("Contraseña DB:", "", is_password=True)

        form_layout.addWidget(lbl_db)
        form_layout.addWidget(self.txt_host)
        form_layout.addWidget(self.txt_port)
        form_layout.addWidget(self.txt_dbuser)
        form_layout.addWidget(self.txt_dbpass)
        
        # Divisor
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("background-color: #2A1E3A; border: none; margin: 10px 0px;")
        form_layout.addWidget(div)

        # Sección: Usuario App
        lbl_user = QLabel("Perfil de Usuario")
        lbl_user.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        lbl_user.setStyleSheet("border: none;")

        self.txt_appuser = self._create_input("Tu Nombre (ej. Juan):", "")
        self.txt_approle = self._create_input("Cargo/Rol (ej. Administrador):", "Administrador")

        form_layout.addWidget(lbl_user)
        form_layout.addWidget(self.txt_appuser)
        form_layout.addWidget(self.txt_approle)

        # Etiqueta de error
        self.lbl_error = QLabel("")
        self.lbl_error.setStyleSheet("color: #FF4444; border: none;")
        self.lbl_error.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(self.lbl_error)

        # Botón
        self.btn_save = QPushButton("Guardar y Conectar")
        self.btn_save.setFixedSize(200, 42)
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #FF2E88; color: white;
                border-radius: 6px; font-weight: bold; font-size: 14px;
                border: none;
            }
            QPushButton:hover { background-color: #C2185B; }
        """)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch()

        # Ensamblar
        layout.addWidget(header_lbl)
        layout.addWidget(desc_lbl)
        layout.addWidget(form_frame)
        layout.addLayout(btn_layout)
        layout.addStretch()

    def _create_input(self, placeholder: str, default_val: str, is_password: bool = False) -> QLineEdit:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder)
        line_edit.setText(default_val)
        line_edit.setFixedHeight(36)
        line_edit.setStyleSheet("""
            QLineEdit {
                background-color: #0B0712;
                border: 1px solid #3B2A52;
                border-radius: 4px;
                padding: 0px 10px;
                color: #F3E8FF;
            }
            QLineEdit:focus {
                border: 1px solid #FF2E88;
            }
        """)
        if is_password:
            line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        return line_edit

    def show_error(self, message: str):
        self.lbl_error.setText(f"<img src='assets/icons/warning.svg' width='14' height='14'> {message}")

    def clear_error(self):
        self.lbl_error.setText("")
