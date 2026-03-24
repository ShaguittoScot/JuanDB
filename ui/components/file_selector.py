from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

class FileSelector(QWidget):
    """Componente reutilizable para selección de archivos/rutas"""
    def __init__(self, placeholder="Seleccionar archivo...", mode="file", parent=None):
        super().__init__(parent)
        self.mode = mode  # 'file' o 'directory'
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText(placeholder)
        self.path_edit.setProperty("class", "file-selector-input")
        
        self.browse_btn = QPushButton("📂 Examinar")
        self.browse_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.browse_btn.setProperty("class", "btn-secondary-animated")
        
        layout.addWidget(self.path_edit, 1)
        layout.addWidget(self.browse_btn)
        
    def get_path(self):
        return self.path_edit.text()
        
    def set_path(self, path):
        self.path_edit.setText(path)
