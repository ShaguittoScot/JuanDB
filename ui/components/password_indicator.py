import re
from PyQt6.QtWidgets import QLabel


class PasswordStrengthIndicator(QLabel):
    """Barra delgada que indica la fortaleza de la contraseña."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(3)
        self.setStyleSheet("background-color: #30363D; border-radius: 2px;")

    def check_strength(self, password: str):
        score = 0
        if len(password) >= 8:                                    score += 1
        if re.search(r'[A-Z]', password):                        score += 1
        if re.search(r'[a-z]', password):                        score += 1
        if re.search(r'[0-9]', password):                        score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):      score += 1

        colors = {
            0: "#30363D",   # vacía
            1: "#F85149",   # roja (débil)
            2: "#D29922",   # naranja
            3: "#D29922",   # naranja
            4: "#3FB950",   # verde
            5: "#3B82F6",   # azul (excelente)
        }
        self.setStyleSheet(f"background-color: {colors[score]}; border-radius: 2px;")
