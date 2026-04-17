from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QFrame, QApplication, QScrollArea
)
from PyQt6.QtCore import Qt
from ui.colors import LIGHT_THEME, DARK_THEME, CYBERPUNK_THEME
from ui.styles import get_stylesheet

from ui.components.sidebar import Sidebar, NAV_ITEMS
from ui.components.topbar import TopBar
from ui.components.module_view import ModuleView
from ui.views.backup_view import BackupView
from controllers.backup_controller import BackupController
from ui.views.monitor_view import MonitorView
from controllers.monitor_controller import MonitorController
from ui.views.transfer_view import TransferView
from controllers.import_export_controller import ImportExportController
from ui.views.security_view import SecurityView
from controllers.security_controller import SecurityController
from ui.views.settings_view import SettingsView

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JuanDB")
        self.setGeometry(100, 100, 1100, 660)
        self.setMinimumSize(800, 500)

        self.theme_mode = 0 # 0: Dark, 1: Cyber, 2: Light

        self._build_ui()
        self._apply_styles()

        # Seleccionar primer módulo
        self.sidebar.set_active_module(0)
        self.change_module(0, NAV_ITEMS[0][1])

    # ── Construcción ────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.module_selected.connect(self.change_module)

        root.addWidget(self.sidebar)
        root.addWidget(self._build_content(), 1)

    # ── Área de contenido ────────────────────────────────────────────────────

    def _build_content(self):
        content = QFrame()
        content.setObjectName("contentArea")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.topbar = TopBar()
        self.topbar.theme_changed.connect(self.change_theme)

        topbar_line = QFrame()
        topbar_line.setObjectName("topBarLine")
        topbar_line.setFixedHeight(1)

        # Área de trabajo con padding
        workspace = QFrame()
        workspace.setObjectName("workspace")
        ws_layout = QVBoxLayout(workspace)
        ws_layout.setContentsMargins(32, 28, 32, 28)
        ws_layout.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.setObjectName("stack")

        self.backup_view = BackupView()
        self.backup_controller = BackupController(self.backup_view)
        
        self.monitor_view = MonitorView()
        self.monitor_controller = MonitorController(self.monitor_view)
        
        self.transfer_view = TransferView()
        self.import_export_controller = ImportExportController(self.transfer_view)
        
        self.security_view = SecurityView()
        self.security_controller = SecurityController(self.security_view)

        self.settings_view = SettingsView()
        self.settings_view.settings_saved.connect(self._on_settings_saved)

        for v in [self.backup_view, self.transfer_view, self.security_view,
                  self.monitor_view, self.settings_view]:
            self.stack.addWidget(v)

        ws_layout.addWidget(self.stack)

        layout.addWidget(self.topbar)
        layout.addWidget(topbar_line)
        layout.addWidget(workspace, 1)

        return content

    # ── Lógica ───────────────────────────────────────────────────────────────

    def change_theme(self, mode: int):
        self.theme_mode = mode
        self._apply_styles()

    def _on_settings_saved(self, cfg: dict):
        """Aplica configuración guardada desde SettingsView."""
        if "theme" in cfg:
            self.theme_mode = cfg["theme"]
            self._apply_styles()

    def change_module(self, index: int, title: str):
        self.stack.setCurrentIndex(index)
        self.topbar.set_module(title)

    # ── Estilos ──────────────────────────────────────────────────────────────

    def _apply_styles(self):
        themes = {
            0: DARK_THEME,
            1: CYBERPUNK_THEME,
            2: LIGHT_THEME
        }
        theme = themes.get(self.theme_mode, DARK_THEME)
        self.setStyleSheet(get_stylesheet(theme))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())