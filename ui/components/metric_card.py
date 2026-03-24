from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MetricCard(QFrame):
    """Tarjeta de métrica mejorada con animaciones"""
    def __init__(self, title, initial_value="0", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setMinimumHeight(100)
        
        # Estilo base
        self.setProperty("class", "metric-card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(8)
        
        # Título con ícono
        title_layout = QHBoxLayout()
        self.icon_label = QLabel("<img src='assets/icons/bar_chart.svg' width='16' height='16'>")
        self.icon_label.setProperty("class", "icon-16-accent")
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.title_label.setProperty("class", "text-adaptive")
        title_layout.addWidget(self.icon_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        
        # Valor
        self.value_label = QLabel(initial_value)
        self.value_label.setFont(QFont("Courier New", 24, QFont.Weight.Bold))
        self.value_label.setProperty("class", "text-adaptive")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Unidad o indicador
        self.indicator = QLabel("")
        self.indicator.setFont(QFont("Segoe UI", 9))
        self.indicator.setProperty("class", "text-muted")
        
        layout.addLayout(title_layout)
        layout.addWidget(self.value_label)
        layout.addWidget(self.indicator)
        layout.addStretch()
        
        # Animación de valor
        self.anim_value = None
        self._current_value = 0
        
    def set_value(self, value, unit=""):
        """Actualiza el valor con animación"""
        try:
            # Extraer número del texto si es posible
            if isinstance(value, str):
                import re
                numbers = re.findall(r'[\d.]+', value)
                if numbers:
                    new_num = float(numbers[0])
                    self._animate_value(new_num, unit, value)
                else:
                    self.value_label.setText(value)
            else:
                self._animate_value(float(value), unit)
        except:
            self.value_label.setText(str(value))
            
    def _animate_value(self, new_value, unit="", formatted_text=None):
        """Animación suave del cambio de valor"""
        if self.anim_value:
            self.anim_value.stop()
            
        # Si se proporciona texto formateado, usarlo directamente
        if formatted_text:
            self.value_label.setText(formatted_text)
        else:
            self.value_label.setText(f"{new_value}{unit}")
            
    def set_icon(self, icon):
        """Cambia el ícono de la métrica"""
        self.icon_label.setText(icon)
