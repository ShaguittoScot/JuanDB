from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class TopBar(QFrame):
    theme_toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("topBar")
        self.setFixedHeight(64)
        
        self.is_dark_theme = False
        self._build_ui()

    def _build_ui(self):
        tb_layout = QHBoxLayout(self)
        tb_layout.setContentsMargins(32, 0, 32, 0)

        self.current_module_label = QLabel("Backups")
        self.current_module_label.setObjectName("moduleTitle")
        self.current_module_label.setFont(QFont("Georgia", 16, QFont.Weight.Bold))

        self.breadcrumb = QLabel("JuanDB  /  Backups")
        self.breadcrumb.setObjectName("breadcrumb")
        self.breadcrumb.setFont(QFont("Courier New", 8))

        self.btn_theme_toggle = QPushButton("🌙 Oscuro")
        self.btn_theme_toggle.setObjectName("themeToggleBtn")
        self.btn_theme_toggle.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_theme_toggle.clicked.connect(self._on_theme_toggle)

        tb_layout.addWidget(self.current_module_label)
        tb_layout.addStretch()
        tb_layout.addWidget(self.breadcrumb)
        tb_layout.addSpacing(16)
        tb_layout.addWidget(self.btn_theme_toggle)

    def set_module(self, title: str):
        self.current_module_label.setText(title)
        self.breadcrumb.setText(f"JuanDB  /  {title}")

    def _on_theme_toggle(self):
        self.is_dark_theme = not self.is_dark_theme
        self.btn_theme_toggle.setText("☀️ Claro" if self.is_dark_theme else "🌙 Oscuro")
        self.theme_toggled.emit(self.is_dark_theme)
