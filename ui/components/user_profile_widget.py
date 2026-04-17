"""
user_profile_widget.py — Widget de perfil de usuario para el footer del sidebar.

Clase pública:
    UserProfileWidget(QFrame)

Uso:
    from ui.components.user_profile_widget import UserProfileWidget
    widget = UserProfileWidget(name="Juan", role="Administrador", db_user="root")
    sidebar_layout.addWidget(widget)
"""

from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QMenu, QWidgetAction, QWidget
)
from PyQt6.QtCore import Qt, QPoint, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QColor, QAction
import qtawesome as qta


class UserProfileWidget(QFrame):
    """
    Widget compacto de perfil de usuario con:
    - Avatar circular con inicial
    - Nombre (negrita) + rol (gris pequeño)
    - Menú contextual al hacer clic: Perfil / Ajustes / Cerrar sesión

    Señales:
        profile_clicked()   — "Ver perfil" seleccionado
        settings_clicked()  — "Ajustes de cuenta" seleccionado
        logout_clicked()    — "Cerrar sesión" seleccionado
    """

    profile_clicked  = pyqtSignal()
    settings_clicked = pyqtSignal()
    logout_clicked   = pyqtSignal()

    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, name: str = "Usuario", role: str = "Rol",
                 db_user: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("userProfileWidget")
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedHeight(52)

        self._name    = name
        self._role    = role
        self._db_user = db_user

        self._build_ui()

    # ── Construcción ──────────────────────────────────────────────────────────

    def _build_ui(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 8, 12, 8)
        lay.setSpacing(10)

        # ── Avatar circular ──────────────────────────────────────────────────
        self._avatar = QLabel(self._initial())
        self._avatar.setFixedSize(28, 28)
        self._avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._avatar.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self._avatar.setObjectName("userAvatar")

        # ── Columna de texto ─────────────────────────────────────────────────
        col = QVBoxLayout()
        col.setSpacing(1)
        col.setContentsMargins(0, 0, 0, 0)

        self._name_lbl = QLabel(self._name)
        self._name_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self._name_lbl.setProperty("class", "text-light")
        self._name_lbl.setMaximumWidth(130)

        role_text = f"{self._role}  ·  @{self._db_user}" if self._db_user else self._role
        self._role_lbl = QLabel(role_text)
        self._role_lbl.setFont(QFont("Segoe UI", 10))
        self._role_lbl.setProperty("class", "text-hint")
        self._role_lbl.setMaximumWidth(130)

        col.addWidget(self._name_lbl)
        col.addWidget(self._role_lbl)

        # ── Chevron ──────────────────────────────────────────────────────────
        chevron = QLabel()
        chevron.setPixmap(qta.icon('fa5s.ellipsis-h', color='#7D8590').pixmap(14, 14))
        chevron.setProperty("class", "text-hint")
        chevron.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lay.addWidget(self._avatar)
        lay.addLayout(col, 1)
        lay.addWidget(chevron)

    # ── Menú contextual ───────────────────────────────────────────────────────

    def _build_menu(self) -> QMenu:
        menu = QMenu(self)
        menu.setObjectName("userMenu")

        # ── Encabezado informativo (no clickeable) ────────────────────────
        header_widget = QWidget()
        header_lay = QVBoxLayout(header_widget)
        header_lay.setContentsMargins(16, 8, 16, 8)
        header_lay.setSpacing(2)

        lbl_name = QLabel(self._name)
        lbl_name.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        lbl_name.setProperty("class", "text-light")

        lbl_role = QLabel(f"@{self._db_user}  ·  {self._role}" if self._db_user else self._role)
        lbl_role.setFont(QFont("Segoe UI", 11))
        lbl_role.setProperty("class", "text-hint")

        header_lay.addWidget(lbl_name)
        header_lay.addWidget(lbl_role)

        header_action = QWidgetAction(menu)
        header_action.setDefaultWidget(header_widget)
        menu.addAction(header_action)
        menu.addSeparator()

        # ── Perfil ────────────────────────────────────────────────────────
        act_profile = QAction("  Perfil", menu)
        act_profile.setIcon(qta.icon('fa5s.user', color='#7D8590'))
        act_profile.triggered.connect(self.profile_clicked.emit)
        menu.addAction(act_profile)

        # ── Ajustes ───────────────────────────────────────────────────────
        act_settings = QAction("  Ajustes de cuenta", menu)
        act_settings.setIcon(qta.icon('fa5s.cog', color='#7D8590'))
        act_settings.triggered.connect(self.settings_clicked.emit)
        menu.addAction(act_settings)

        menu.addSeparator()

        # ── Cerrar sesión (rojo) ─────────────────────────────────────────
        act_logout = QAction("  Cerrar sesión", menu)
        act_logout.setIcon(qta.icon('fa5s.sign-out-alt', color='#F85149'))
        act_logout.triggered.connect(self.logout_clicked.emit)

        # Widget personalizado para el item de logout (para tener el color rojo y el icono juntos)
        logout_widget = QWidget()
        lw_lay = QHBoxLayout(logout_widget)
        lw_lay.setContentsMargins(12, 6, 16, 6)
        lw_lay.setSpacing(10)
        
        logout_icon = QLabel()
        logout_icon.setPixmap(qta.icon('fa5s.sign-out-alt', color='#F85149').pixmap(14, 14))
        
        logout_text = QLabel("Cerrar sesión")
        logout_text.setFont(QFont("Segoe UI", 13))
        logout_text.setStyleSheet("color: #F85149;") # Rojo
        
        lw_lay.addWidget(logout_icon)
        lw_lay.addWidget(logout_text)
        lw_lay.addStretch()

        logout_widget.setObjectName("userLogoutItem")
        logout_widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_widget.mousePressEvent = lambda _: (menu.close(), self.logout_clicked.emit())

        logout_action = QWidgetAction(menu)
        logout_action.setDefaultWidget(logout_widget)
        menu.addAction(logout_action)

        return menu

    # ── Interactividad ────────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            menu = self._build_menu()
            # El menú flota justo encima del widget
            global_pos = self.mapToGlobal(QPoint(0, 0))
            menu.adjustSize()
            popup_y = global_pos.y() - menu.sizeHint().height() - 6
            menu.exec(QPoint(global_pos.x(), popup_y))
        super().mousePressEvent(event)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _initial(self) -> str:
        return self._name[0].upper() if self._name else "U"

    # ── API pública ───────────────────────────────────────────────────────────

    def set_user(self, name: str, role: str, db_user: str = ""):
        """Actualiza los datos mostrados sin reconstruir el widget."""
        self._name    = name
        self._role    = role
        self._db_user = db_user
        self._avatar.setText(self._initial())
        self._name_lbl.setText(name)
        role_text = f"{role}  ·  @{db_user}" if db_user else role
        self._role_lbl.setText(role_text)
