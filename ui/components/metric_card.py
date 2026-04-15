from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class MetricCard(QFrame):
    """Tarjeta de métrica compacta y profesional."""

    def __init__(self, title: str, initial_value: str = "—", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setProperty("class", "metric-card")
        self.setMinimumHeight(90)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 14, 16, 14)
        layout.setSpacing(4)

        # Etiqueta de título (UPPERCASE, pequeña)
        self.title_label = QLabel(title.upper())
        self.title_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.title_label.setProperty("class", "text-muted")

        # Valor principal
        self.value_label = QLabel(initial_value)
        self.value_label.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        self.value_label.setProperty("class", "text-adaptive")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Sub-indicador
        self.indicator = QLabel("")
        self.indicator.setFont(QFont("Segoe UI", 11))
        self.indicator.setProperty("class", "text-hint")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.indicator)

    def set_value(self, value, unit: str = ""):
        """Actualiza el valor mostrado."""
        if isinstance(value, (int, float)):
            self.value_label.setText(f"{value}{unit}")
        else:
            self.value_label.setText(str(value))

    def set_icon(self, icon: str):
        """Compatibilidad — ya no se usa ícono separado."""
        pass
