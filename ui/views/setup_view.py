from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QLineEdit, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor


class SetupView(QWidget):
    """Pantalla de configuración inicial — se muestra solo la primera vez."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JuanDB — Configuración inicial")
        self.setFixedSize(460, 800)
        self._apply_base_style()
        self._build_ui()

    def _apply_base_style(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0D1117;
                color: #F0F6FC;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 6px;
                padding: 9px 12px;
                color: #F0F6FC;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #3B82F6;
                background-color: #1C2333;
            }
            QLineEdit::placeholder {
                color: #484F58;
            }
        """)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setSpacing(0)

        # ── Logo/Brand ───────────────────────────────────────────────────────
        brand = QHBoxLayout()
        dot = QLabel("●")
        dot.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        dot.setStyleSheet("color: #3B82F6;")
        name = QLabel("JuanDB")
        name.setFont(QFont("Segoe UI", 16, QFont.Weight.DemiBold))
        name.setStyleSheet("color: #F0F6FC;")
        brand.addStretch()
        brand.addWidget(dot)
        brand.addSpacing(6)
        brand.addWidget(name)
        brand.addStretch()
        root.addLayout(brand)
        root.addSpacing(32)

        # ── Título ───────────────────────────────────────────────────────────
        title = QLabel("Bienvenido")
        title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #F0F6FC; border: none;")

        subtitle = QLabel("Configura la conexión a tu servidor MySQL para comenzar.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #7D8590; border: none;")

        root.addWidget(title)
        root.addSpacing(6)
        root.addWidget(subtitle)
        root.addSpacing(32)

        # ── Formulario ───────────────────────────────────────────────────────
        form = QFrame()
        form.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 10px;
            }
        """)
        form_lay = QVBoxLayout(form)
        form_lay.setContentsMargins(24, 24, 24, 24)
        form_lay.setSpacing(0)

        # Sección: Conexión
        form_lay.addWidget(self._section_label("Servidor MySQL"))
        form_lay.addSpacing(12)

        form_lay.addWidget(self._field_label("Host"))
        self.txt_host = self._input("localhost")
        form_lay.addWidget(self.txt_host)
        form_lay.addSpacing(12)

        row = QHBoxLayout(); row.setSpacing(10)
        col_port = QVBoxLayout()
        col_port.addWidget(self._field_label("Puerto"))
        self.txt_port = self._input("3306")
        col_port.addWidget(self.txt_port)
        col_user = QVBoxLayout()
        col_user.addWidget(self._field_label("Usuario"))
        self.txt_dbuser = self._input("root")
        col_user.addWidget(self.txt_dbuser)
        row.addLayout(col_port); row.addLayout(col_user)
        form_lay.addLayout(row)
        form_lay.addSpacing(12)

        form_lay.addWidget(self._field_label("Contraseña"))
        self.txt_dbpass = self._input("", is_password=True)
        form_lay.addWidget(self.txt_dbpass)

        # Divisor
        form_lay.addSpacing(20)
        div = QFrame()
        div.setFixedHeight(1)
        div.setStyleSheet("background-color: #21262D; border: none;")
        form_lay.addWidget(div)
        form_lay.addSpacing(20)

        # Sección: Perfil
        form_lay.addWidget(self._section_label("Tu perfil"))
        form_lay.addSpacing(12)

        row2 = QHBoxLayout(); row2.setSpacing(10)
        col_n = QVBoxLayout()
        col_n.addWidget(self._field_label("Tu nombre"))
        self.txt_appuser = self._input("Juan")
        col_n.addWidget(self.txt_appuser)
        col_r = QVBoxLayout()
        col_r.addWidget(self._field_label("Cargo / Rol"))
        self.txt_approle = self._input("Administrador")
        col_r.addWidget(self.txt_approle)
        row2.addLayout(col_n); row2.addLayout(col_r)
        form_lay.addLayout(row2)

        root.addWidget(form)
        root.addSpacing(16)

        # ── Error label ──────────────────────────────────────────────────────
        self.lbl_error = QLabel("")
        self.lbl_error.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_error.setFont(QFont("Segoe UI", 12))
        self.lbl_error.setStyleSheet("color: #F85149; border: none;")
        self.lbl_error.setWordWrap(True)
        self.lbl_error.setFixedHeight(20)
        root.addWidget(self.lbl_error)
        root.addSpacing(12)

        # ── Botón ────────────────────────────────────────────────────────────
        self.btn_save = QPushButton("Guardar y conectar")
        self.btn_save.setFixedHeight(42)
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        self.btn_save.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            QPushButton:pressed {
                background-color: #1D4ED8;
            }
        """)
        root.addWidget(self.btn_save)
        root.addStretch()

        # ── Nota ─────────────────────────────────────────────────────────────
        note = QLabel("Solo se te pedirá esta configuración una vez.")
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        note.setFont(QFont("Segoe UI", 11))
        note.setStyleSheet("color: #484F58; border: none;")
        root.addWidget(note)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _section_label(self, text: str) -> QLabel:
        lbl = QLabel(text.upper())
        lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        lbl.setStyleSheet("color: #484F58; letter-spacing: 1px; border: none;")
        return lbl

    def _field_label(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        lbl.setStyleSheet("color: #7D8590; margin-bottom: 4px; border: none;")
        return lbl

    def _input(self, default: str = "", is_password: bool = False) -> QLineEdit:
        le = QLineEdit()
        le.setText(default)
        le.setFixedHeight(38)
        if is_password:
            le.setEchoMode(QLineEdit.EchoMode.Password)
            le.setPlaceholderText("••••••••")
        return le

    # ── API pública ───────────────────────────────────────────────────────────

    def show_error(self, message: str):
        self.lbl_error.setText(f"⚠  {message}")

    def clear_error(self):
        self.lbl_error.setText("")
