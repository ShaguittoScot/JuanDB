"""
help_icon.py — Componente de ícono de ayuda contextual.
Muestra un ícono ⓘ interactivo con un tooltip personalizado.
"""
from PyQt6.QtWidgets import QPushButton, QToolTip
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont, QCursor


class HelpIcon(QPushButton):
    def __init__(self, tooltip_text: str, parent=None):
        super().__init__("ⓘ", parent)
        self.tooltip_text = tooltip_text
        
        self.setFont(QFont("Segoe UI", 16))
        self.setObjectName("helpIconBtn")
        
        self.setToolTip(self.tooltip_text)
        self.setCursor(QCursor(Qt.CursorShape.WhatsThisCursor))
        
        # Al pulsar, forzar la aparición del tooltip directamente debajo del botón
        self.clicked.connect(self._show_tooltip)

    def _show_tooltip(self):
        # Muestra el tooltip manualmente cerca de donde está el mouse
        QToolTip.showText(QCursor.pos(), self.tooltip_text, self)
