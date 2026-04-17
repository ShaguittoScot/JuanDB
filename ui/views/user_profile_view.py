from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
import qtawesome as qta


def _section(title: str) -> QFrame:
    frame = QFrame()
    frame.setObjectName("formCard")
    # Usamos objectName formCard para heredar estilos de la global
    
    outer = QVBoxLayout(frame)
    outer.setContentsMargins(20, 20, 20, 20)
    outer.setSpacing(16)

    t = QLabel(title)
    t.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
    t.setProperty("class", "text-light")
    outer.addWidget(t)

    body = QVBoxLayout()
    body.setSpacing(12)
    outer.addLayout(body)
    
    frame._body = body # type: ignore
    return frame

def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
    lbl.setProperty("class", "text-muted")
    return lbl

def _input() -> QLineEdit:
    le = QLineEdit()
    le.setFixedHeight(38)
    return le

class UserProfileView(QWidget):
    """
    Vista de Perfil de Usuario unificada con Ajustes de Cuenta.
    """
    save_clicked = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(32)

        # ── Encabezado de Perfil ─────────────────────────────────────────────
        header = QHBoxLayout()
        header.setSpacing(20)

        self._avatar_lbl = QLabel("U")
        self._avatar_lbl.setFixedSize(80, 80)
        self._avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._avatar_lbl.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self._avatar_lbl.setObjectName("profileAvatarLarge")
        self._avatar_lbl.setStyleSheet("""
            QLabel#profileAvatarLarge {
                background-color: #3B82F6;
                color: white;
                border-radius: 40px;
            }
        """)

        header_info = QVBoxLayout()
        header_info.setSpacing(2)
        
        self.name_header = QLabel("Nombre de Usuario")
        self.name_header.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.name_header.setProperty("class", "text-light")

        self.role_header = QLabel("Administrador")
        self.role_header.setFont(QFont("Segoe UI", 12))
        self.role_header.setProperty("class", "text-muted")

        header_info.addWidget(self.name_header)
        header_info.addWidget(self.role_header)
        header_info.addStretch()

        header.addWidget(self._avatar_lbl)
        header.addLayout(header_info)
        header.addStretch()

        main_layout.addLayout(header)

        # ── Área de tarjetas ──────────────────────────────────────────────────
        cards_container = QHBoxLayout()
        cards_container.setSpacing(24)

        # Tarjeta 1: Mi Cuenta
        card_account = _section("Mi Cuenta")
        self.txt_name = _input()
        self.txt_email = _input()

        card_account._body.addWidget(_field_label("Nombre Completo")) # type: ignore
        card_account._body.addWidget(self.txt_name) # type: ignore
        card_account._body.addSpacing(4)
        card_account._body.addWidget(_field_label("Correo Electrónico")) # type: ignore
        card_account._body.addWidget(self.txt_email) # type: ignore
        
        btn_save = QPushButton("Guardar Cambios")
        btn_save.setProperty("class", "btn-primary")
        btn_save.setFixedHeight(40)
        btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_save.clicked.connect(self._on_save_clicked)
        card_account._body.addSpacing(10) # type: ignore
        card_account._body.addWidget(btn_save) # type: ignore

        # Tarjeta 2: Seguridad
        card_security = _section("Seguridad de Cuenta")
        
        btn_pass = QPushButton("  Cambiar Contraseña")
        btn_pass.setIcon(qta.icon('fa5s.key', color='#7D8590'))
        btn_pass.setProperty("class", "btn-secondary-animated")
        btn_pass.setFixedHeight(40)

        btn_sessions = QPushButton("  Gestionar Sesiones Activas")
        btn_sessions.setIcon(qta.icon('fa5s.shield-alt', color='#7D8590'))
        btn_sessions.setProperty("class", "btn-secondary-animated")
        btn_sessions.setFixedHeight(40)

        card_security._body.addWidget(btn_pass) # type: ignore
        card_security._body.addWidget(btn_sessions) # type: ignore
        card_security._body.addStretch() # type: ignore

        cards_container.addWidget(card_account, 1)
        cards_container.addWidget(card_security, 1)

        main_layout.addLayout(cards_container)
        main_layout.addStretch()

    def _on_save_clicked(self):
        data = {
            "name": self.txt_name.text(),
            "email": self.txt_email.text()
        }
        self.save_clicked.emit(data)

    def load_profile(self, config: dict):
        name = config.get("user_name", "Usuario")
        email = config.get("user_email", "admin@juandb.com")
        role = config.get("user_role", "Administrador")

        self.txt_name.setText(name)
        self.txt_email.setText(email)
        
        self.name_header.setText(name)
        self.role_header.setText(role)
        self._avatar_lbl.setText(name[0].upper() if name else "U")
