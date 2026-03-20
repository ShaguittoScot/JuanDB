from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont
from services.config_service import ConfigService

NAV_ITEMS = [
    ("backup",   "Backups",       "B"),
    ("import",   "Import / Export", "I"),
    ("security", "Seguridad",     "S"),
    ("monitor",  "Monitoreo",     "M"),
    ("settings", "Configuración", "C"),
]

class Sidebar(QFrame):
    module_selected = pyqtSignal(int, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        
        self.sidebar_expanded = True
        self.sidebar_width = 220
        self.sidebar_collapsed_width = 64
        self.setFixedWidth(self.sidebar_width)
        
        self.nav_buttons = []
        
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Cabecera ──────────────────────────────────────────────────────
        header = QFrame()
        header.setObjectName("sidebarHeader")
        header.setFixedHeight(64)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(18, 0, 12, 0)
        h_layout.setSpacing(10)

        self.logo_mark = QLabel("JDB")
        self.logo_mark.setObjectName("logoMark")
        self.logo_mark.setFont(QFont("Courier New", 11, QFont.Weight.Bold))

        self.app_title = QLabel("JuanDB")
        self.app_title.setObjectName("appTitle")
        self.app_title.setFont(QFont("Georgia", 13, QFont.Weight.Bold))

        self.btn_toggle = QPushButton("‹")
        self.btn_toggle.setObjectName("toggleBtn")
        self.btn_toggle.setFixedSize(28, 28)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        h_layout.addWidget(self.logo_mark)
        h_layout.addWidget(self.app_title, 1)
        h_layout.addWidget(self.btn_toggle)

        # ── Línea bajo header ─────────────────────────────────────────────
        top_line = QFrame()
        top_line.setObjectName("topLine")
        top_line.setFixedHeight(1)

        # ── Sección de navegación ─────────────────────────────────────────
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(12, 20, 12, 20)
        nav_layout.setSpacing(4)

        self.section_label = QLabel("NAVEGACIÓN")
        self.section_label.setObjectName("sectionLabel")
        self.section_label.setFont(QFont("Courier New", 7, QFont.Weight.Bold))
        nav_layout.addWidget(self.section_label)
        nav_layout.addSpacing(8)

        for i, (key, label, abbr) in enumerate(NAV_ITEMS):
            btn = QPushButton(f"  {label}")
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setFont(QFont("Courier New", 9))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(40)
            btn.setProperty("abbr", abbr)
            btn.setProperty("full_label", label)
            btn.clicked.connect(lambda checked, idx=i, title=label: self._on_nav_clicked(idx, title))
            
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()

        # ── Divisor ───────────────────────────────────────────────────────
        div = QFrame()
        div.setObjectName("divider")
        div.setFixedHeight(1)

        # ── Footer ────────────────────────────────────────────────────────
        footer = QFrame()
        footer.setObjectName("sidebarFooter")
        f_layout = QHBoxLayout(footer)
        f_layout.setContentsMargins(16, 14, 16, 14)
        f_layout.setSpacing(10)

        cfg = ConfigService.load_config()
        app_user = cfg.get("app_user", "Juan")

        from services.db_service import get_current_user_info
        info = get_current_user_info()
        db_user = info["user"]
        db_role = info["role"]

        initial = app_user[0].upper() if app_user else "J"

        avatar = QLabel(initial)
        avatar.setObjectName("avatar")
        avatar.setFixedSize(32, 32)
        avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        avatar.setFont(QFont("Courier New", 11, QFont.Weight.Bold))

        user_col = QVBoxLayout()
        user_col.setSpacing(0)

        self.user_name = QLabel(app_user)
        self.user_name.setObjectName("userName")
        self.user_name.setFont(QFont("Courier New", 9, QFont.Weight.Bold))

        self.user_role = QLabel(f"{db_role} (@{db_user})")
        self.user_role.setObjectName("userRole")
        self.user_role.setFont(QFont("Courier New", 7))
        
        self.btn_logout = QPushButton("Cerrar Sesión")
        self.btn_logout.setObjectName("btnLogout")
        self.btn_logout.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_logout.setStyleSheet("background-color: transparent; color: #FF4444; border: none; font-size: 10px; font-weight: bold; text-align: left; margin-top: 4px;")
        self.btn_logout.clicked.connect(self._on_logout)

        user_col.addWidget(self.user_name)
        user_col.addWidget(self.user_role)
        user_col.addWidget(self.btn_logout)

        f_layout.addWidget(avatar)
        f_layout.addLayout(user_col)
        f_layout.addStretch()

        # ── Ensamblar sidebar ─────────────────────────────────────────────
        layout.addWidget(header)
        layout.addWidget(top_line)
        layout.addWidget(nav_frame, 1)
        layout.addWidget(div)
        layout.addWidget(footer)

    def _on_logout(self):
        import sys
        import os
        from services.config_service import ConfigService
        ConfigService.clear_config()
        # Reinicia limpiamente el proceso desde el Sistema Operativo
        os.execl(sys.executable, sys.executable, *sys.argv)

    def _on_nav_clicked(self, index: int, title: str):
        self.set_active_module(index)
        self.module_selected.emit(index, title)

    def set_active_module(self, index: int):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def toggle_sidebar(self):
        self.sidebar_expanded = not self.sidebar_expanded

        self.anim = QPropertyAnimation(self, b"minimumWidth")
        self.anim.setDuration(250)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim2 = QPropertyAnimation(self, b"maximumWidth")
        anim2.setDuration(250)
        anim2.setEasingCurve(QEasingCurve.Type.InOutCubic)

        if self.sidebar_expanded:
            target = self.sidebar_width
            self.btn_toggle.setText("‹")
            self.app_title.show()
            self.user_name.show()
            self.user_role.show()
            self.section_label.show()
            for btn in self.nav_buttons:
                btn.setText(f"  {btn.property('full_label')}")
        else:
            target = self.sidebar_collapsed_width
            self.btn_toggle.setText("›")
            self.app_title.hide()
            self.user_name.hide()
            self.user_role.hide()
            self.section_label.hide()
            for btn in self.nav_buttons:
                btn.setText(btn.property("abbr"))

        self.anim.setEndValue(target)
        anim2.setEndValue(target)
        self.anim.start()
        anim2.start()
