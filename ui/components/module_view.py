from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ModuleView(QWidget):
    def __init__(self, title: str, description: str, parent=None):
        super().__init__(parent)
        self._build_ui(title, description)

    def _build_ui(self, title: str, description: str):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Tarjeta principal
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(16)

        # Etiqueta de módulo pequeña
        tag = QLabel(title.upper())
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 7, QFont.Weight.Bold))

        # Línea dorada decorativa
        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(40, 3)

        # Descripción
        desc = QLabel(description)
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Georgia", 11))
        desc.setWordWrap(True)

        # Placeholder de contenido
        placeholder = QFrame()
        placeholder.setObjectName("placeholder")
        placeholder.setMinimumHeight(260)
        ph_layout = QVBoxLayout(placeholder)

        ph_label = QLabel("[ Contenido del módulo ]")
        ph_label.setObjectName("phLabel")
        ph_label.setFont(QFont("Courier New", 10))
        ph_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ph_layout.addWidget(ph_label)

        card_layout.addWidget(tag)
        card_layout.addWidget(accent_line)
        card_layout.addSpacing(4)
        card_layout.addWidget(desc)
        card_layout.addSpacing(12)
        card_layout.addWidget(placeholder, 1)

        layout.addWidget(card, 1)
