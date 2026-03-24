import re
from PyQt6.QtWidgets import QLabel

class PasswordStrengthIndicator(QLabel):
    """Indicador visual de fortaleza de contraseña"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)
        self.setStyleSheet("background-color: #3B2A52; border-radius: 2px;")
        
    def check_strength(self, password):
        """Evalúa la fortaleza de la contraseña"""
        strength = 0
        if len(password) >= 8:
            strength += 1
        if re.search(r'[A-Z]', password):
            strength += 1
        if re.search(r'[a-z]', password):
            strength += 1
        if re.search(r'[0-9]', password):
            strength += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            strength += 1
            
        colors = {
            0: "#3B2A52",
            1: "#FF4444",
            2: "#FFB86C",
            3: "#FFE55C",
            4: "#4ADE80",
            5: "#00FF88"
        }
        
        self.setStyleSheet(f"background-color: {colors.get(strength, '#3B2A52')}; border-radius: 2px;")
