from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class TopBar(QFrame):
    theme_toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")
        self.setFixedHeight(56)

        self.is_dark_theme = True
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

        sep = QLabel("›")
        sep.setFont(QFont("Segoe UI", 12))
        sep.setStyleSheet("color: #484F58; padding: 0 2px;")

        self.current_module_label = QLabel("Backups")
        self.current_module_label.setObjectName("moduleTitle")
        self.current_module_label.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))

        nav_col_layout.addWidget(self.breadcrumb)
        nav_col_layout.addWidget(sep)
        nav_col_layout.addWidget(self.current_module_label)

        # Botón de tema
        self.btn_theme_toggle = QPushButton("☀  Claro")
        self.btn_theme_toggle.setObjectName("themeToggleBtn")
        self.btn_theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme_toggle.setFixedHeight(30)
        self.btn_theme_toggle.setFont(QFont("Segoe UI", 12))
        self.btn_theme_toggle.clicked.connect(self._on_theme_toggle)

        tb_layout.addWidget(nav_col)
        tb_layout.addStretch()
        tb_layout.addWidget(self.btn_theme_toggle)

    def set_module(self, title: str):
        self.current_module_label.setText(title)

    def _on_theme_toggle(self):
        self.is_dark_theme = not self.is_dark_theme
        self.btn_theme_toggle.setText("☀  Claro" if self.is_dark_theme else "🌙  Oscuro")
        self.theme_toggled.emit(self.is_dark_theme)
