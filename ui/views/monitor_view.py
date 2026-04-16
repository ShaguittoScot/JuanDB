"""
monitor_view.py — Arquitectura modular para la vista de Monitoreo.

Clases:
    MetricCard     — KPI card reutilizable
    RealTimeChart  — Base para gráficas pyqtgraph estilizadas
    MonitorView    — Vista principal (orquesta layout + timer UI)
"""

import random
import pyqtgraph as pg
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QPushButton, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QCursor, QColor

from ui.components.help_icon import HelpIcon

# ── Importar paleta desde el sistema de diseño ────────────────────────────────
from ui.colors import DARK_THEME as APP_COLORS


# ═════════════════════════════════════════════════════════════════════════════
# MetricCard — KPI card con título, valor y subtítulo
# ═════════════════════════════════════════════════════════════════════════════

class MetricCard(QFrame):
    """Tarjeta de métrica: etiqueta + valor grande + indicador."""

    def __init__(self, title: str, subtitle: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("metricCard")
        self.setProperty("class", "metric-card")
        self.setMinimumHeight(96)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(4)

        # Título (UPPERCASE, pequeño, muted)
        self._title_lbl = QLabel(title.upper())
        self._title_lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self._title_lbl.setProperty("class", "text-muted")

        # Valor principal
        self._value_lbl = QLabel("—")
        self._value_lbl.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        self._value_lbl.setProperty("class", "view-title")

        # Subtítulo / indicador
        self._sub_lbl = QLabel(subtitle)
        self._sub_lbl.setFont(QFont("Segoe UI", 11))
        self._sub_lbl.setProperty("class", "text-hint")

        layout.addWidget(self._title_lbl)
        layout.addWidget(self._value_lbl)
        layout.addWidget(self._sub_lbl)

    # API pública
    def set_value(self, value: str, subtitle: str = ""):
        self._value_lbl.setText(value)
        if subtitle:
            self._sub_lbl.setText(subtitle)

    def set_indicator(self, text: str):
        self._sub_lbl.setText(text)


# ═════════════════════════════════════════════════════════════════════════════
# RealTimeChart — Clase base para gráficas pyqtgraph del monitor
# ═════════════════════════════════════════════════════════════════════════════

class RealTimeChart(QFrame):
    """
    Contenedor base para una gráfica pyqtgraph.
    Aplica el tema oscuro del sistema de diseño y elimina ruido visual.
    """

    def __init__(self, title: str, tooltip: str = "", parent=None):
        super().__init__(parent)
        self.setObjectName("formCard")
        self.setMinimumHeight(200)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Card header ───────────────────────────────────────────────────────
        hdr = QFrame()
        hdr.setFixedHeight(44)
        hdr.setStyleSheet(f"""
            QFrame {{
                background: transparent;
                border: none;
                border-bottom: 1px solid {APP_COLORS['BORDER']};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }}
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(16, 0, 16, 0)

        self._title_lbl = QLabel(title)
        self._title_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self._title_lbl.setProperty("class", "view-subtitle-muted")
        hl.addWidget(self._title_lbl)
        
        if tooltip:
            from ui.components.help_icon import HelpIcon
            icon = HelpIcon(tooltip)
            hl.addWidget(icon)

        hl.addStretch()

        # Slot para widget extras en el header (ej. leyenda)
        self._header_extras = QHBoxLayout()
        self._header_extras.setSpacing(12)
        hl.addLayout(self._header_extras)

        outer.addWidget(hdr)

        # ── Área de la gráfica ────────────────────────────────────────────────
        self.plot = pg.PlotWidget()
        self._style_plot()
        outer.addWidget(self.plot, 1)

    def _style_plot(self):
        """Aplica el tema del sistema de diseño a la gráfica."""
        bg = APP_COLORS["BG_SURFACE"]
        self.plot.setBackground(pg.mkColor(bg))
        self.plot.showGrid(x=False, y=True, alpha=0.08)
        self.plot.getPlotItem().hideButtons()
        self.plot.setMenuEnabled(False)

        # Eliminar bordes internos
        self.plot.getPlotItem().getViewBox().setBorder(None)
        self.plot.setStyleSheet("border: none; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")

        # Ejes con colores del tema
        for axis_name in ("left", "bottom"):
            ax = self.plot.getAxis(axis_name)
            ax.setPen(pg.mkPen(APP_COLORS["SEPARATOR"]))
            ax.setTextPen(pg.mkPen(APP_COLORS["TEXT_HINT"]))

        # Quitar eje derecho y top
        self.plot.getPlotItem().showAxis("right", False)
        self.plot.getPlotItem().showAxis("top",   False)

    def _add_legend_dot(self, label: str, color: str):
        """Agrega un punto de leyenda en el header."""
        lbl = QLabel(f"● {label}")
        lbl.setFont(QFont("Segoe UI", 11))
        lbl.setStyleSheet(f"color: {color}; border: none;")
        self._header_extras.addWidget(lbl)

    def mk_pen(self, color_key: str, width: int = 2, style=Qt.PenStyle.SolidLine) -> pg.mkPen:
        return pg.mkPen(color=APP_COLORS[color_key], width=width, style=style)

    def mk_brush(self, color_key: str, alpha: int = 40) -> pg.mkBrush:
        c = QColor(APP_COLORS[color_key])
        c.setAlpha(alpha)
        return pg.mkBrush(c)


# ═════════════════════════════════════════════════════════════════════════════
# QueryLoadChart — Gráfica 1: Carga de consultas (línea + relleno)
# ═════════════════════════════════════════════════════════════════════════════

class QueryLoadChart(RealTimeChart):
    def __init__(self, history_len: int = 60, parent=None):
        super().__init__("Carga de consultas", "Muestra la cantidad de peticiones o consultas procesadas por el servidor por segundo (QPS).", parent)
        self._n = history_len
        self._data = [0.0] * self._n
        self._x = list(range(-self._n + 1, 1))

        self._add_legend_dot("QPS", APP_COLORS["ACCENT"])

        self.plot.setLabel("left",   "Consultas/seg", color=APP_COLORS["TEXT_HINT"])
        self.plot.setLabel("bottom", "Tiempo (seg)",  color=APP_COLORS["TEXT_HINT"])

        self._curve = self.plot.plot(
            self._x, self._data,
            pen=self.mk_pen("ACCENT", width=2),
            fillLevel=0,
            brush=self.mk_brush("ACCENT", alpha=35),
        )

    def push(self, value: float):
        self._data.pop(0)
        self._data.append(value)
        self._curve.setData(self._x, self._data)
        peak = max(self._data) * 1.15 or 10
        self.plot.setYRange(0, peak, padding=0)


# ═════════════════════════════════════════════════════════════════════════════
# CpuRamChart — Gráfica 2: CPU & RAM (sólida + punteada)
# ═════════════════════════════════════════════════════════════════════════════

class CpuRamChart(RealTimeChart):
    def __init__(self, history_len: int = 60, parent=None):
        super().__init__("CPU & RAM", "Monitorea el porcentaje del procesador y la memoria RAM consumidos en tiempo real.", parent)
        self._n = history_len
        self._cpu = [0.0] * self._n
        self._ram = [0.0] * self._n
        self._x   = list(range(-self._n + 1, 1))

        self._add_legend_dot("CPU",  APP_COLORS["ACCENT"])
        self._add_legend_dot("RAM",  APP_COLORS["WARNING"])

        self.plot.setLabel("left",   "%",            color=APP_COLORS["TEXT_HINT"])
        self.plot.setLabel("bottom", "Tiempo (seg)", color=APP_COLORS["TEXT_HINT"])
        self.plot.setYRange(0, 100, padding=0.02)

        # CPU — línea sólida
        self._curve_cpu = self.plot.plot(
            self._x, self._cpu,
            pen=self.mk_pen("ACCENT", width=2, style=Qt.PenStyle.SolidLine),
            name="CPU"
        )
        # RAM — línea punteada
        self._curve_ram = self.plot.plot(
            self._x, self._ram,
            pen=self.mk_pen("WARNING", width=2, style=Qt.PenStyle.DashLine),
            name="RAM"
        )

    def push(self, cpu: float, ram: float):
        for lst, val in ((self._cpu, cpu), (self._ram, ram)):
            lst.pop(0); lst.append(val)
        self._curve_cpu.setData(self._x, self._cpu)
        self._curve_ram.setData(self._x, self._ram)


# ═════════════════════════════════════════════════════════════════════════════
# NetworkChart — Gráfica 3: Entrada/Salida de Red (barras simétricas)
# ═════════════════════════════════════════════════════════════════════════════

class NetworkChart(RealTimeChart):
    def __init__(self, bars: int = 30, parent=None):
        super().__init__("Tráfico de red", "Visualiza el tráfico de entrada (RX) y salida (TX) en kilobytes por segundo.", parent)
        self._n = bars
        self._rx = [0.0] * self._n    # entrada (arriba)
        self._tx = [0.0] * self._n    # salida (abajo, negativo)
        self._x  = list(range(self._n))

        self._add_legend_dot("RX (↓)", APP_COLORS["SUCCESS"])
        self._add_legend_dot("TX (↑)", APP_COLORS["INFO"])

        self.plot.setLabel("left",   "KB/s",         color=APP_COLORS["TEXT_HINT"])
        self.plot.setLabel("bottom", "Muestras",     color=APP_COLORS["TEXT_HINT"])

        # Barras RX — verde, hacia arriba
        self._bars_rx = pg.BarGraphItem(
            x=self._x, height=self._rx, width=0.7,
            brush=pg.mkBrush(QColor(APP_COLORS["SUCCESS"]))
        )
        # Barras TX — azul, hacia abajo (negativas)
        self._bars_tx = pg.BarGraphItem(
            x=self._x, height=self._tx, width=0.7,
            brush=pg.mkBrush(QColor(APP_COLORS["INFO"]))
        )

        self.plot.addItem(self._bars_rx)
        self.plot.addItem(self._bars_tx)

        # Línea cero
        self.plot.addItem(pg.InfiniteLine(
            pos=0, angle=0,
            pen=pg.mkPen(APP_COLORS["BORDER"], width=1)
        ))

    def push(self, rx_kb: float, tx_kb: float):
        self._rx.pop(0); self._rx.append(rx_kb)
        self._tx.pop(0); self._tx.append(-tx_kb)   # negativo = hacia abajo
        self._bars_rx.setOpts(x=self._x, height=self._rx)
        self._bars_tx.setOpts(x=self._x, height=self._tx)
        peak = max(max(self._rx), max(-v for v in self._tx), 1) * 1.2
        self.plot.setYRange(-peak, peak, padding=0)


# ═════════════════════════════════════════════════════════════════════════════
# MonitorView — Vista principal
# ═════════════════════════════════════════════════════════════════════════════

class MonitorView(QWidget):
    """
    Orquesta el layout de monitoreo.
    Timer centralizado aquí: cada tick emite datos a los sub-componentes.
    El controller externo puede conectarse a btn_toggle y llamar a
    update_display() / update_graph() para inyectar datos reales.
    """

    # Señal que el timer interno dispara para actualizar todos los widgets
    _tick = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(900, 620)
        self._history_len = 60
        self._build_ui()
        self._setup_demo_timer()

    # ── Construcción ──────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._controls_bar())
        root.addWidget(self._kpi_strip())

        # Gráficas — 2/3 del espacio disponible
        charts = QFrame()
        charts.setStyleSheet("background: transparent; border: none;")
        cl = QGridLayout(charts)
        cl.setContentsMargins(16, 12, 16, 16)
        cl.setSpacing(12)

        self.chart_qps     = QueryLoadChart(self._history_len)
        self.chart_cpu_ram = CpuRamChart(self._history_len)
        self.chart_net     = NetworkChart(30)

        # Row 0: QPS (ancho completo)
        cl.addWidget(self.chart_qps,      0, 0, 1, 2)
        # Row 1: CPU/RAM | Red
        cl.addWidget(self.chart_cpu_ram,  1, 0, 1, 1)
        cl.addWidget(self.chart_net,      1, 1, 1, 1)

        cl.setRowStretch(0, 1)
        cl.setRowStretch(1, 1)
        cl.setColumnStretch(0, 1)
        cl.setColumnStretch(1, 1)

        root.addWidget(charts, 1)
        root.addWidget(self._footer())

    # ── Barra de controles ────────────────────────────────────────────────────

    def _controls_bar(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(52)
        bar.setStyleSheet(f"border-bottom: 1px solid {APP_COLORS['SEPARATOR']};")

        lay = QHBoxLayout(bar)
        lay.setContentsMargins(24, 0, 24, 0)
        lay.setSpacing(12)

        self.btn_toggle = QPushButton("▶  Iniciar monitoreo")
        self.btn_toggle.setProperty("class", "btn-primary")
        self.btn_toggle.setFixedHeight(32)
        self.btn_toggle.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.btn_toggle.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_toggle.clicked.connect(self._toggle_demo)

        self.dot_status = QLabel("●")
        self.dot_status.setFont(QFont("Segoe UI", 12))
        self.dot_status.setStyleSheet(f"color: {APP_COLORS['TEXT_HINT']}; border: none;")

        self.status_label = QLabel("Detenido")
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setProperty("class", "text-muted")

        self.error_label = QLabel("")
        self.error_label.setFont(QFont("Segoe UI", 12))
        self.error_label.setStyleSheet(f"color: {APP_COLORS['ERROR']}; border: none;")

        lay.addWidget(self.btn_toggle)
        lay.addSpacing(8)
        lay.addWidget(self.dot_status)
        lay.addWidget(self.status_label)
        lay.addStretch()
        lay.addWidget(self.error_label)
        
        help_icon = HelpIcon("Métricas de rendimiento del servidor MySQL en tiempo real — QPS, conexiones, CPU y red.")
        help_icon.setStyleSheet(help_icon.styleSheet() + " margin-right: 8px;")
        lay.addWidget(help_icon)
        
        return bar

    # ── Franja de KPIs ────────────────────────────────────────────────────────

    def _kpi_strip(self) -> QFrame:
        strip = QFrame()
        strip.setStyleSheet(f"border-bottom: 1px solid {APP_COLORS['SEPARATOR']};")
        lay = QHBoxLayout(strip)
        lay.setContentsMargins(16, 10, 16, 10)
        lay.setSpacing(10)

        self._cards = {}
        kpis = [
            ("uptime",   "Tiempo activo",     "uptime del servidor"),
            ("threads",  "Conexiones",        "simultáneas"),
            ("qps",      "Consultas / seg",   "QPS promedio"),
            ("total_q",  "Total consultas",   "desde inicio"),
        ]
        for key, title, sub in kpis:
            card = MetricCard(title, sub)
            self._cards[key] = card
            lay.addWidget(card, 1)

        return strip

    # ── Footer ────────────────────────────────────────────────────────────────

    def _footer(self) -> QFrame:
        f = QFrame()
        f.setFixedHeight(30)
        f.setStyleSheet(f"border-top: 1px solid {APP_COLORS['SEPARATOR']};")
        lay = QHBoxLayout(f)
        lay.setContentsMargins(24, 0, 24, 0)
        lbl = QLabel("Actualización cada segundo  ·  Ventana de 60 segundos")
        lbl.setFont(QFont("Segoe UI", 10))
        lbl.setProperty("class", "text-hint")
        lay.addWidget(lbl)
        lay.addStretch()
        return f

    # ── Demo timer (datos simulados hasta que el controller inyecte reales) ──

    def _setup_demo_timer(self):
        self._demo_timer = QTimer(self)
        self._demo_timer.setInterval(1000)
        self._demo_timer.timeout.connect(self._tick_demo)
        self._is_active = False
        self._tick_count = 0

    def _toggle_demo(self):
        if self._is_active:
            self._demo_timer.stop()
            self._is_active = False
            self.set_monitoring_state(False)
        else:
            self._demo_timer.start()
            self._is_active = True
            self.set_monitoring_state(True)

    def _tick_demo(self):
        """Genera datos simulados para previsualización. El controller reemplaza esto."""
        self._tick_count += 1
        qps     = max(0, 120 + random.gauss(0, 25))
        threads = max(1, int(5 + random.gauss(0, 2)))
        cpu     = max(0, min(100, 35 + random.gauss(0, 10)))
        ram     = max(0, min(100, 60 + random.gauss(0, 5)))
        rx      = max(0, 800 + random.gauss(0, 200))
        tx      = max(0, 400 + random.gauss(0, 150))

        h, m, s = self._tick_count // 3600, (self._tick_count % 3600) // 60, self._tick_count % 60
        self.update_display(
            uptime=f"{h:02d}:{m:02d}:{s:02d}",
            threads=str(threads),
            qps=f"{qps:.1f}",
            total_queries=str(self._tick_count * int(qps)),
        )
        self.chart_qps.push(qps)
        self.chart_cpu_ram.push(cpu, ram)
        self.chart_net.push(rx, tx)

    # ═════════════════════════════════════════════════════════════════════════
    # API pública — usada por MonitorController
    # ═════════════════════════════════════════════════════════════════════════

    def update_display(self, uptime: str, threads: str, qps: str, total_queries: str):
        self._cards["uptime"].set_value(uptime)
        self._cards["threads"].set_value(threads)
        self._cards["qps"].set_value(qps)
        self._cards["total_q"].set_value(total_queries)

    def update_graph(self, time_data: list, qps_data: list, threads_data: list):
        """Compatibilidad con MonitorController existente — alimenta la gráfica QPS y conexiones."""
        if qps_data:
            self.chart_qps._data = list(qps_data)
            self.chart_qps._curve.setData(self.chart_qps._x, qps_data)
        if threads_data:
            self.chart_cpu_ram._cpu = list(threads_data)
            self.chart_cpu_ram._curve_cpu.setData(self.chart_cpu_ram._x, threads_data)

    def show_error(self, msg: str):
        self.error_label.setText(f"⚠  {msg}")

    def clear_error(self):
        self.error_label.setText("")

    def set_monitoring_state(self, is_active: bool):
        if is_active:
            self.btn_toggle.setText("⏸  Pausar monitoreo")
            self.dot_status.setStyleSheet(f"color: {APP_COLORS['SUCCESS']}; border: none;")
            self.status_label.setText("Monitorizando...")
            self.status_label.setStyleSheet(f"color: {APP_COLORS['SUCCESS']};")
        else:
            self.btn_toggle.setText("▶  Iniciar monitoreo")
            self.dot_status.setStyleSheet(f"color: {APP_COLORS['TEXT_HINT']}; border: none;")
            self.status_label.setText("Detenido")
            self.status_label.setStyleSheet(f"color: {APP_COLORS['TEXT_MUTED']};")