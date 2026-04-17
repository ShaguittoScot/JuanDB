from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont
import qtawesome as qta

class TopBar(QFrame):
    theme_changed = pyqtSignal(int) # 0: Dark, 1: Cyber, 2: Light

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")
        self.setFixedHeight(56)

        self.theme_mode = 0 # 0: Dark, 1: Cyber, 2: Light
        self._build_ui()

    def _build_ui(self):
        tb_layout = QHBoxLayout(self)
        tb_layout.setContentsMargins(24, 0, 20, 0)
        tb_layout.setSpacing(0)

        # Breadcrumb + título vertical
        nav_col = QFrame()
        nav_col_layout = QHBoxLayout(nav_col)
        nav_col_layout.setContentsMargins(0, 0, 0, 0)
        nav_col_layout.setSpacing(6)

        self.breadcrumb = QLabel("JuanDB")
        self.breadcrumb.setObjectName("breadcrumb")
        self.breadcrumb.setFont(QFont("Segoe UI", 12))

        sep = QLabel()
        sep.setPixmap(qta.icon('fa5s.chevron-right', color='#484F58').pixmap(10, 10))
        sep.setStyleSheet("padding: 0 4px;")

        self.current_module_label = QLabel("Backups")
        self.current_module_label.setObjectName("moduleTitle")
        self.current_module_label.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))

        nav_col_layout.addWidget(self.breadcrumb)
        nav_col_layout.addWidget(sep)
        nav_col_layout.addWidget(self.current_module_label)

        # Botón de tema
        self.btn_theme_toggle = QPushButton("Claro")
        self.btn_theme_toggle.setObjectName("themeToggleBtn")
        self.btn_theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme_toggle.setFixedHeight(30)
        self.btn_theme_toggle.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.btn_theme_toggle.setIcon(qta.icon('fa5s.sun', color='#D29922'))
        self.btn_theme_toggle.setIconSize(QSize(16, 16))
        self.btn_theme_toggle.clicked.connect(self._on_theme_toggle)

        tb_layout.addWidget(nav_col)
        tb_layout.addStretch()
        tb_layout.addWidget(self.btn_theme_toggle)

    def set_module(self, title: str):
        self.current_module_label.setText(title)

    def _on_theme_toggle(self):
        self.theme_mode = (self.theme_mode + 1) % 3
        
        modes = {
            0: ("fa5s.moon", "#7D8590", "Oscuro"),
            1: ("fa5s.bolt", "#FF00FF", "Cyberpunk"),
            2: ("fa5s.sun",  "#D29922", "Claro")
        }
        
        icon_name, color, btn_text = modes[self.theme_mode]
        self.btn_theme_toggle.setText(btn_text)
        self.btn_theme_toggle.setIcon(qta.icon(icon_name, color=color))
        self.theme_changed.emit(self.theme_mode)
