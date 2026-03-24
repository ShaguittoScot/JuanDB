from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtGui import QFont
from datetime import datetime

class LogTextEdit(QTextEdit):
    """Área de log mejorada con colores y formateo"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        
    def append_log(self, message, log_type="info"):
        """Agrega mensajes con diferentes colores según tipo"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Configurar color según tipo
        colors = {
            "info": "#C4B5FD",
            "success": "#4ADE80",
            "error": "#FF4444",
            "warning": "#FFB86C",
            "process": "#FF2E88"
        }
        
        color = colors.get(log_type, "#C4B5FD")
        icon = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "process": "🔄"
        }.get(log_type, "📝")
        
        formatted_msg = f'<span style="color: #6B4E8E;">[{timestamp}]</span> <span style="color: {color};">{icon} {message}</span>'
        self.append(formatted_msg)
        
        # Auto-scroll
        scrollbar = self.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
