from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QPushButton, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QCursor, QPalette, QColor, QLinearGradient, QIcon
import pyqtgraph as pg

from ui.components.animated_button import AnimatedButton
from ui.components.metric_card import MetricCard


class MonitorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(900, 700)
        self._build_ui()
        

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Tarjeta principal
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 32, 40, 32)
        card_layout.setSpacing(20)

        # Header con tag y título
        header_layout = QHBoxLayout()
        
        tag_container = QVBoxLayout()
        tag = QLabel("<img src='assets/icons/lightning.svg' width='14' height='14'> MONITOREO EN TIEMPO REAL")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 8, QFont.Weight.Bold))
        
        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(60, 3)
        
        tag_container.addWidget(tag)
        tag_container.addWidget(accent_line)
        
        # Título principal
        title = QLabel("Dashboard de Rendimiento")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setProperty("class", "view-title")
        
        header_layout.addLayout(tag_container)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Descripción
        desc = QLabel("Monitoreo avanzado de la base de datos con métricas en tiempo real.\n"
                     "Visualiza el rendimiento, conexiones activas y patrones de consultas.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Segoe UI", 11))
        desc.setWordWrap(True)
        card_layout.addWidget(desc)
        
        card_layout.addSpacing(8)

        # Controles superiores mejorados
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(16)
        
        self.btn_toggle = AnimatedButton("Iniciar Monitoreo")
        self.btn_toggle.setIcon(QIcon("assets/icons/play.svg"))
        self.btn_toggle.setProperty("class", "btn-primary")
        self.btn_toggle.setMinimumSize(200, 44)
        
        # Panel de estado
        status_panel = QFrame()
        status_panel.setProperty("class", "status-panel")
        status_layout = QHBoxLayout(status_panel)
        status_layout.setSpacing(12)
        
        status_indicator = QLabel("●")
        status_indicator.setProperty("class", "status-indicator")
        self.status_label = QLabel("Estado: Pausado")
        self.status_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.status_label.setProperty("status", "paused")
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setProperty("class", "h-separator")
        
        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Segoe UI", 10))
        self.error_label.setWordWrap(True)
        
        status_layout.addWidget(status_indicator)
        status_layout.addWidget(self.status_label)
        status_layout.addWidget(separator)
        status_layout.addWidget(self.error_label)
        
        controls_layout.addWidget(self.btn_toggle)
        controls_layout.addWidget(status_panel, 1)
        controls_layout.addStretch()
        
        card_layout.addLayout(controls_layout)
        card_layout.addSpacing(8)

        # Grid de Métricas con tarjetas mejoradas
        self.metrics = {}
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(20)
        
        # Crear tarjetas de métricas
        self.metrics['uptime'] = MetricCard("Tiempo Activo")
        self.metrics['uptime'].set_icon("<img src='assets/icons/timer.svg' width='16' height='16'>")
        metrics_grid.addWidget(self.metrics['uptime'], 0, 0)
        
        self.metrics['threads'] = MetricCard("Conexiones Activas")
        self.metrics['threads'].set_icon("<img src='assets/icons/plug.svg' width='16' height='16'>")
        self.metrics['threads'].indicator.setText("conexiones simultáneas")
        metrics_grid.addWidget(self.metrics['threads'], 0, 1)
        
        self.metrics['qps'] = MetricCard("Consultas por Segundo")
        self.metrics['qps'].set_icon("<img src='assets/icons/lightning.svg' width='16' height='16'>")
        self.metrics['qps'].indicator.setText("QPS promedio")
        metrics_grid.addWidget(self.metrics['qps'], 1, 0)
        
        self.metrics['total_queries'] = MetricCard("Consultas Totales")
        self.metrics['total_queries'].set_icon("<img src='assets/icons/chart.svg' width='16' height='16'>")
        self.metrics['total_queries'].indicator.setText("desde inicio")
        metrics_grid.addWidget(self.metrics['total_queries'], 1, 1)
        
        card_layout.addLayout(metrics_grid)
        card_layout.addSpacing(16)

        # Sección de gráfica con título mejorado
        graph_header = QHBoxLayout()
        graph_title = QLabel("<img src='assets/icons/bar_chart.svg' width='14' height='14'> Gráfica de Rendimiento en Tiempo Real")
        graph_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        graph_title.setProperty("class", "view-subtitle-muted")
        
        legend_container = QFrame()
        legend_container.setProperty("class", "legend-container")
        legend_layout = QHBoxLayout(legend_container)
        legend_layout.setContentsMargins(12, 4, 12, 4)
        
        qps_legend = QLabel("● QPS")
        qps_legend.setProperty("class", "text-accent")
        threads_legend = QLabel("● Conexiones")
        threads_legend.setProperty("class", "text-muted")
        legend_layout.addWidget(qps_legend)
        legend_layout.addWidget(threads_legend)
        
        graph_header.addWidget(graph_title)
        graph_header.addStretch()
        graph_header.addWidget(legend_container)
        
        card_layout.addLayout(graph_header)
        
        # Gráfica interactiva mejorada
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('#0A0515')
        self.graph_widget.showGrid(x=True, y=True, alpha=0.2)
        self.graph_widget.setLabel('left', 'Valor', color='#C4B5FD')
        self.graph_widget.setLabel('bottom', 'Tiempo (segundos)', color='#C4B5FD')
        self.graph_widget.setMinimumHeight(300)
        
        # Estilo de los ejes
        self.graph_widget.getAxis('left').setPen('#3B2A52')
        self.graph_widget.getAxis('bottom').setPen('#3B2A52')
        self.graph_widget.getAxis('left').setTextPen('#C4B5FD')
        self.graph_widget.getAxis('bottom').setTextPen('#C4B5FD')
        
        # Configurar líneas de la gráfica
        pen_qps = pg.mkPen(color='#FF2E88', width=2.5)
        pen_threads = pg.mkPen(color='#A78BFA', width=2.5)
        
        # Área sombreada para QPS
        self.line_qps = self.graph_widget.plot([0], [0], pen=pen_qps, name="QPS")
        self.line_threads = self.graph_widget.plot([0], [0], pen=pen_threads, name="Conexiones")
        
        # Agregar relleno para las líneas
        self.fill_qps = pg.FillBetweenItem(self.line_qps, self.line_qps, brush=pg.mkBrush(255, 46, 136, 30))
        
        card_layout.addWidget(self.graph_widget, 1)
        
        # Footer con información adicional
        footer = QLabel("<img src='assets/icons/info.svg' width='14' height='14'> Los datos se actualizan cada segundo | Las gráficas muestran los últimos 60 segundos")
        footer.setFont(QFont("Segoe UI", 9))
        footer.setProperty("class", "text-footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(footer)

        layout.addWidget(card)
        layout.addStretch()

    def update_display(self, uptime: str, threads: str, qps: str, total_queries: str):
        """Actualiza las métricas con animaciones suaves"""
        self.metrics['uptime'].set_value(uptime, "")
        self.metrics['threads'].set_value(threads, "")
        self.metrics['qps'].set_value(qps, " QPS")
        self.metrics['total_queries'].set_value(total_queries, "")
        
    def update_graph(self, time_data: list, qps_data: list, threads_data: list):
        """Actualiza la gráfica con manejo de límites automático"""
        if time_data and qps_data and threads_data:
            self.line_qps.setData(time_data, qps_data)
            self.line_threads.setData(time_data, threads_data)
            
            # Ajustar automáticamente los límites del eje Y
            max_qps = max(qps_data) if qps_data else 10
            max_threads = max(threads_data) if threads_data else 10
            max_value = max(max_qps, max_threads) * 1.1  # 10% de margen
            
            if max_value > 0:
                self.graph_widget.setYRange(0, max_value if max_value > 0 else 10)
        
    def show_error(self, msg: str):
        """Muestra mensaje de error con estilo"""
        self.error_label.setText(f"<img src='assets/icons/warning.svg' width='14' height='14'> {msg}")
        self.error_label.setProperty("class", "text-error")
        self.status_label.setProperty("status", "error")
        self.status_label.style().polish(self.status_label)
        
    def clear_error(self):
        """Limpia el mensaje de error"""
        self.error_label.setText("")
        
    def set_monitoring_state(self, is_active: bool):
        """Actualiza la interfaz según el estado del monitoreo"""
        if is_active:
            self.btn_toggle.setText("Pausar Monitoreo")
            self.btn_toggle.setIcon(QIcon("assets/icons/pause.svg"))
            self.status_label.setText("Estado: Activo")
            self.status_label.setProperty("status", "active")
        else:
            self.btn_toggle.setText("Iniciar Monitoreo")
            self.btn_toggle.setIcon(QIcon("assets/icons/play.svg"))
            self.status_label.setText("Estado: Pausado")
            self.status_label.setProperty("status", "paused")
        self.status_label.style().polish(self.status_label)