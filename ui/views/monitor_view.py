from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
import pyqtgraph as pg

class MonitorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # Tarjeta principal
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(36, 32, 36, 32)
        card_layout.setSpacing(16)

        tag = QLabel("REDIMIENTO Y MONITOREO")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 7, QFont.Weight.Bold))

        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(40, 3)

        desc = QLabel("Visualiza el rendimiento de la base de datos en tiempo real.\nObtén métricas de uso y estado global del servicio.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Georgia", 11))
        desc.setWordWrap(True)

        # Controles superiores
        controls_layout = QHBoxLayout()
        self.btn_toggle = QPushButton("▶ Iniciar Monitoreo")
        self.btn_toggle.setObjectName("btnPrimary")
        self.btn_toggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle.setFixedSize(180, 36)
        
        self.status_label = QLabel("Estado: Pausado")
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet("color: #A78BFA;")
        
        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Segoe UI", 10))
        self.error_label.setStyleSheet("color: #FF4444;")
        
        controls_layout.addWidget(self.btn_toggle)
        controls_layout.addSpacing(16)
        controls_layout.addWidget(self.status_label)
        controls_layout.addSpacing(16)
        controls_layout.addWidget(self.error_label)
        controls_layout.addStretch()

        # Grid de Métricas
        metrics_grid = QGridLayout()
        metrics_grid.setSpacing(20)
        
        self.val_uptime = self._create_metric_card(metrics_grid, "Tiempo Activo (Uptime)", "0h 0m 0s", 0, 0)
        self.val_threads = self._create_metric_card(metrics_grid, "Conexiones Activas", "0", 0, 1)
        self.val_qps = self._create_metric_card(metrics_grid, "Consultas / Seg (QPS)", "0", 1, 0)
        self.val_total_queries = self._create_metric_card(metrics_grid, "Consultas Totales", "0", 1, 1)

        # Gráfica interactiva de pyqtgraph
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('#120A1C')
        self.graph_widget.showGrid(x=True, y=True, alpha=0.3)
        self.graph_widget.setLabel('left', 'Valor')
        self.graph_widget.setLabel('bottom', 'Tiempo (s)')
        self.graph_widget.setMinimumHeight(200)
        self.graph_widget.addLegend()

        pen_qps = pg.mkPen(color='#FF2E88', width=2)
        pen_threads = pg.mkPen(color='#A78BFA', width=2)
        
        self.line_qps = self.graph_widget.plot([0], [0], pen=pen_qps, name="QPS")
        self.line_threads = self.graph_widget.plot([0], [0], pen=pen_threads, name="Conexiones")

        card_layout.addWidget(tag)
        card_layout.addWidget(accent_line)
        card_layout.addSpacing(4)
        card_layout.addWidget(desc)
        card_layout.addSpacing(24)
        card_layout.addLayout(controls_layout)
        card_layout.addSpacing(24)
        card_layout.addLayout(metrics_grid)
        card_layout.addSpacing(16)
        card_layout.addWidget(QLabel("Gráfica en tiempo real:"))
        card_layout.addWidget(self.graph_widget, 1)
        card_layout.addStretch()

        layout.addWidget(card, 1)

    def _create_metric_card(self, grid: QGridLayout, title: str, initial_value: str, row: int, col: int) -> QLabel:
        frame = QFrame()
        frame.setStyleSheet("background-color: #120A1C; border-radius: 8px; border: 1px solid #3B2A52;")
        flayout = QVBoxLayout(frame)
        flayout.setContentsMargins(24, 24, 24, 24)
        
        lbl_title = QLabel(title)
        lbl_title.setFont(QFont("Segoe UI", 11))
        lbl_title.setStyleSheet("color: #A78BFA; border: none;")
        
        lbl_value = QLabel(initial_value)
        lbl_value.setFont(QFont("Courier New", 26, QFont.Weight.Bold))
        lbl_value.setStyleSheet("color: #F3E8FF; border: none;")
        
        flayout.addWidget(lbl_title)
        flayout.addSpacing(12)
        flayout.addWidget(lbl_value)
        
        grid.addWidget(frame, row, col)
        return lbl_value

    def update_display(self, uptime: str, threads: str, qps: str, total_queries: str):
        self.val_uptime.setText(uptime)
        self.val_threads.setText(threads)
        self.val_qps.setText(qps)
        self.val_total_queries.setText(total_queries)

    def update_graph(self, time_data: list, qps_data: list, threads_data: list):
        self.line_qps.setData(time_data, qps_data)
        self.line_threads.setData(time_data, threads_data)
        
    def show_error(self, msg: str):
        self.error_label.setText(f"⚠ {msg}")
        
    def clear_error(self):
        self.error_label.setText("")
