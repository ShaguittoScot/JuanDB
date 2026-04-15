from PyQt6.QtWidgets import QPushButton, QGraphicsColorizeEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QCursor

class AnimatedButton(QPushButton):
    """Botón con animación de opacidad suave al pasar el cursor."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(36)
