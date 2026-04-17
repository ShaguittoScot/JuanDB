from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal, QSize
from PyQt6.QtGui import QFont
import qtawesome as qta
from services.config_service import ConfigService
from ui.components.user_profile_widget import UserProfileWidget

NAV_ITEMS = [
    ("explorer", "Explorador",      "fa5s.layer-group"),
    ("backup",   "Backups",         "fa5s.hdd"),
    ("import",   "Import / Export", "fa5s.exchange-alt"),
    ("security", "Seguridad",       "fa5s.shield-alt"),
    ("monitor",  "Monitoreo",       "fa5s.chart-line"),
    ("settings", "Configuración",   "fa5s.cog"),
]

class Sidebar(QFrame):
    module_selected = pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")

        self.sidebar_expanded = True
        self.sidebar_width = 210
        self.sidebar_collapsed_width = 56
        self.setFixedWidth(self.sidebar_width)

        self.nav_buttons = []
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Cabecera ───────────────────────────────────────────────────
        header = QFrame()
        header.setObjectName("sidebarHeader")
        header.setFixedHeight(56)
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(16, 0, 12, 0)
        h_layout.setSpacing(10)

        self.logo_mark = QLabel()
        self.logo_mark.setPixmap(qta.icon('fa5s.database', color='#58A6FF').pixmap(20, 20))
        self.logo_mark.setObjectName("logoMark")

        self.app_title = QLabel("JuanDB")
        self.app_title.setObjectName("appTitle")
        self.app_title.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))

        self.btn_toggle = QPushButton()
        self.btn_toggle.setIcon(qta.icon('fa5s.chevron-left', color='#7D8590'))
        self.btn_toggle.setIconSize(QSize(12, 12))
        self.btn_toggle.setObjectName("toggleBtn")
        self.btn_toggle.setFixedSize(26, 26)
        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_toggle.clicked.connect(self.toggle_sidebar)

        h_layout.addWidget(self.logo_mark)
        h_layout.addWidget(self.app_title, 1)
        h_layout.addWidget(self.btn_toggle)

        # ── Separador header ────────────────────────────────────────────
        top_line = QFrame()
        top_line.setObjectName("topLine")
        top_line.setFixedHeight(1)

        # ── Navegación ──────────────────────────────────────────────────
        nav_frame = QFrame()
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 16, 0, 16)
        nav_layout.setSpacing(2)

        self.section_label = QLabel("MENÚ")
        self.section_label.setObjectName("sectionLabel")
        self.section_label.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.section_label.setContentsMargins(16, 0, 0, 8)
        nav_layout.addWidget(self.section_label)

        for i, (key, label, icon_name) in enumerate(NAV_ITEMS):
            btn = QPushButton(f"  {label}")
            btn.setIcon(qta.icon(icon_name, color='#7D8590'))
            btn.setIconSize(QSize(18, 18))
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setFont(QFont("Segoe UI", 12))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(36)
            btn.setProperty("icon_name", icon_name)
            btn.setProperty("label_text", label)
            btn.clicked.connect(lambda checked, idx=i, title=label: self._on_nav_clicked(idx, title))
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)

        nav_layout.addStretch()

        # ── Footer — UserProfileWidget ────────────────────────────────────
        cfg = ConfigService.load_config()
        app_user = cfg.get("app_user", "Juan")

        from services.db_service import get_current_user_info
        info    = get_current_user_info()
        db_user = info["user"]
        db_role = info["role"]

        self.profile_widget = UserProfileWidget(
            name=app_user, role=db_role, db_user=db_user
        )
        self.profile_widget.logout_clicked.connect(self._on_logout)

        # ── Divisor ─────────────────────────────────────────────────────
        div = QFrame()
        div.setObjectName("divider")
        div.setFixedHeight(1)

        # ── Ensamblar ───────────────────────────────────────────────────
        layout.addWidget(header)
        layout.addWidget(top_line)
        layout.addWidget(nav_frame, 1)
        layout.addWidget(div)
        layout.addWidget(self.profile_widget)

    def _on_logout(self):
        import sys, os
        from services.config_service import ConfigService
        ConfigService.clear_config()
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
        self.anim.setDuration(220)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        anim2 = QPropertyAnimation(self, b"maximumWidth")
        anim2.setDuration(220)
        anim2.setEasingCurve(QEasingCurve.Type.InOutCubic)

        if self.sidebar_expanded:
            target = self.sidebar_width
            self.btn_toggle.setIcon(qta.icon('fa5s.chevron-left', color='#7D8590'))
            self.app_title.show()
            self.section_label.show()
            self.profile_widget.show()
            for btn in self.nav_buttons:
                btn.setText(f"  {btn.property('label_text')}")
        else:
            target = self.sidebar_collapsed_width
            self.btn_toggle.setIcon(qta.icon('fa5s.chevron-right', color='#7D8590'))
            self.app_title.hide()
            self.section_label.hide()
            self.profile_widget.hide()
            for btn in self.nav_buttons:
                btn.setText("")

        self.anim.setEndValue(target)
        anim2.setEndValue(target)
        self.anim.start()
        anim2.start()
