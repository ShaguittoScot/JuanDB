import PyQt6.QtWidgets as QtWidgets
from PyQt6.QtWidgets import QPushButton, QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QCursor

class AnimatedButton(QPushButton):
    """Botón con animaciones suaves nativo"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setMinimumHeight(42)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.opacity_anim.setDuration(200)
        self.opacity_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        
    def enterEvent(self, event):
        self.opacity_anim.stop()
        self.opacity_anim.setEndValue(0.85)
        self.opacity_anim.start()
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.opacity_anim.stop()
        self.opacity_anim.setEndValue(1.0)
        self.opacity_anim.start()
        super().leaveEvent(event)
