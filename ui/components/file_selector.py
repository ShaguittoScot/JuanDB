from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton, QFileDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor, QFont


class FileSelector(QWidget):
    """
    Input group integrado: campo + botón visualmente fusionados.
    El botón está pegado al lado derecho del input, compartiendo el mismo borde.
    """
    path_changed = pyqtSignal(str)

    def __init__(self, placeholder: str = "Seleccionar...", mode: str = "file",
                 filter: str = "All Files (*)", parent=None):
        super().__init__(parent)
        self.mode   = mode     # 'file' | 'directory'
        self.filter = filter

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Input ──────────────────────────────────────────────────────────
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText(placeholder)
        self.path_edit.setFixedHeight(36)
        self.path_edit.setStyleSheet("""
            QLineEdit {
                background-color: #1C2333;
                border: 1px solid #30363D;
                border-right: none;
                border-radius: 6px 0 0 6px;
                padding: 0 10px;
                color: #F0F6FC;
                font-size: 13px;
                font-family: 'Segoe UI', sans-serif;
            }
            QLineEdit:hover { border-color: #484F58; }
        """)

        # ── Botón integrado ────────────────────────────────────────────────
        self.browse_btn = QPushButton("Examinar")
        self.browse_btn.setFixedHeight(36)
        self.browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_btn.setFont(QFont("Segoe UI", 12))
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #1C2333;
                border: 1px solid #30363D;
                border-left: 1px solid #484F58;
                border-radius: 0 6px 6px 0;
                color: #7D8590;
                padding: 0 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #242e42;
                color: #F0F6FC;
                border-color: #3B82F6;
                border-left-color: #3B82F6;
            }
        """)
        self.browse_btn.clicked.connect(self._browse)

        layout.addWidget(self.path_edit, 1)
        layout.addWidget(self.browse_btn)

    def _browse(self):
        if self.mode == "directory":
            path = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta")
        else:
            path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", self.filter)

        if path:
            self.path_edit.setText(path)
            self.path_changed.emit(path)

    def get_path(self) -> str:
        return self.path_edit.text()

    def set_path(self, path: str):
        self.path_edit.setText(path)

    def clear(self):
        self.path_edit.clear()
