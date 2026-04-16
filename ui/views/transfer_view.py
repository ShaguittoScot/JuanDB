from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor
import qtawesome as qta

from ui.components.animated_button import AnimatedButton
from ui.components.file_selector import FileSelector
from ui.components.log_text_edit import LogTextEdit
from ui.colors import DARK_THEME as APP_COLORS
from ui.components.help_icon import HelpIcon



class TransferView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(900, 600)
        self._active_mode = "export"
        self._build_ui()

    def _build_ui(self):
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Columna Izquierda (70%) - Formulario
        left_col = QFrame()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(32, 24, 32, 24)
        left_layout.setSpacing(24)

        # Header con Segmented Control y HelpIcon
        header_lay = QHBoxLayout()
        header_lay.setContentsMargins(0, 0, 0, 0)
        
        spacer_left = QWidget()
        spacer_left.setFixedWidth(28)  # Compensar ancho del HelpIcon
        header_lay.addWidget(spacer_left)
        
        header_lay.addWidget(self._mode_toggle_bar(), 1)
        
        header_lay.addWidget(HelpIcon("Importa y exporta datos de manera rápida mediante archivos CSV, JSON o SQL."))
        left_layout.addLayout(header_lay)

        # Contenedor Card centrado
        center_wrapper = QHBoxLayout()
        center_wrapper.setContentsMargins(0, 0, 0, 0)
        
        self.stack = QStackedWidget()
        self.stack.setMaximumWidth(600)
        self.stack.setObjectName("transferCard")
        self.stack.setStyleSheet(f"""
            QStackedWidget#transferCard {{
                background-color: {APP_COLORS['BG_CARD']};
                border-radius: 12px;
                border: 1px solid {APP_COLORS['BORDER']};
            }}
        """)
        
        self.stack.addWidget(self._form_export())
        self.stack.addWidget(self._form_import())
        
        center_wrapper.addStretch()
        center_wrapper.addWidget(self.stack, 1)
        center_wrapper.addStretch()
        
        left_layout.addStretch()  # Centrado vertical superior
        left_layout.addLayout(center_wrapper)
        left_layout.addStretch()  # Centrado vertical inferior
        
        root.addWidget(left_col, 2)

        # Columna Derecha (33%) - LogPanel
        self.log_panel = self._create_log_panel()
        root.addWidget(self.log_panel, 1)

    def _create_log_panel(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(12, 24, 32, 24)
        outer.setSpacing(0)

        card = QFrame()
        card.setObjectName("terminalCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Header de la terminal
        term_hdr = QFrame()
        term_hdr.setFixedHeight(38)
        term_hdr.setObjectName("terminalHeader")
        th_lay = QHBoxLayout(term_hdr)
        th_lay.setContentsMargins(14, 0, 14, 0)

        # Dots decorativos tipo macOS
        for color in ("#F85149", "#D29922", "#3FB950"):
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 10px;")
            th_lay.addWidget(dot)
        th_lay.addSpacing(10)

        term_title = QLabel("Historial de transferencias")
        term_title.setFont(QFont("Segoe UI", 11))
        term_title.setProperty("class", "text-muted")
        th_lay.addWidget(term_title)
        th_lay.addStretch()

        clr_btn = QPushButton("Limpiar")
        clr_btn.setObjectName("btnSecondary")
        clr_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        clr_btn.clicked.connect(self.clear_messages)
        th_lay.addWidget(clr_btn)

        cl.addWidget(term_hdr)

        # Área de texto
        self.log_area = LogTextEdit()
        self.log_area.setObjectName("logArea")
        self.log_area.setMinimumHeight(300)
        cl.addWidget(self.log_area, 1)

        outer.addWidget(card, 1)
        return page

    def _mode_toggle_bar(self) -> QWidget:
        container = QWidget()
        lay = QHBoxLayout(container)
        lay.setContentsMargins(0, 0, 0, 0)
        
        pill = QFrame()
        pill.setFixedHeight(40)
        pill.setStyleSheet(f"""
            QFrame {{
                background-color: {APP_COLORS['BG_SURFACE']};
                border: 1px solid {APP_COLORS['BORDER']};
                border-radius: 8px;
            }}
        """)
        pill_lay = QHBoxLayout(pill)
        pill_lay.setContentsMargins(4, 4, 4, 4)
        pill_lay.setSpacing(2)

        self.btn_mode_export = QPushButton("Exportar Tabla")
        self.btn_mode_import = QPushButton("Importar Archivo")

        for btn in (self.btn_mode_export, self.btn_mode_import):
            btn.setFixedHeight(30)
            btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setCheckable(True)
            pill_lay.addWidget(btn)

        self.btn_mode_export.setChecked(True)
        self.btn_mode_export.clicked.connect(lambda: self._switch_mode("export"))
        self.btn_mode_import.clicked.connect(lambda: self._switch_mode("import"))

        self._style_toggle_btns()

        lay.addStretch()
        lay.addWidget(pill)
        lay.addStretch()
        
        return container

    def _style_toggle_btns(self):
        active_style = f"""
            QPushButton {{
                background-color: {APP_COLORS['ACCENT']};
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 0 24px;
                font-weight: 600;
            }}
        """
        inactive_style = f"""
            QPushButton {{
                background-color: transparent;
                color: {APP_COLORS['TEXT_MUTED']};
                border: none;
                border-radius: 6px;
                padding: 0 24px;
                font-weight: 500;
            }}
            QPushButton:hover {{ color: {APP_COLORS['TEXT_LIGHT']}; }}
        """
        if self._active_mode == "export":
            self.btn_mode_export.setStyleSheet(active_style)
            self.btn_mode_import.setStyleSheet(inactive_style)
        else:
            self.btn_mode_export.setStyleSheet(inactive_style)
            self.btn_mode_import.setStyleSheet(active_style)

    def _switch_mode(self, mode: str):
        self._active_mode = mode
        self.btn_mode_export.setChecked(mode == "export")
        self.btn_mode_import.setChecked(mode == "import")
        self.stack.setCurrentIndex(0 if mode == "export" else 1)
        self._style_toggle_btns()

    def _field_row(self, icon_name: str, widget: QWidget) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)
        
        icon_lbl = QLabel()
        pm = qta.icon(icon_name, color=APP_COLORS['TEXT_MUTED']).pixmap(18, 18)
        icon_lbl.setPixmap(pm)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFixedWidth(24)
        
        row.addWidget(icon_lbl)
        row.addWidget(widget, 1)
        return row

    def _lbl(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        l.setStyleSheet(f"color: {APP_COLORS['TEXT_MUTED']};")
        return l

    def _form_export(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        cl = QVBoxLayout(page)
        cl.setContentsMargins(32, 32, 32, 32)
        cl.setSpacing(18)

        title = QLabel("Exportar Datos")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {APP_COLORS['TEXT_LIGHT']};")
        cl.addWidget(title)
        
        cl.addSpacing(8)

        cl.addWidget(self._lbl("Base de datos"))
        self.db_exp = QComboBox()
        self.db_exp.setPlaceholderText("Seleccionar base de datos...")
        cl.addLayout(self._field_row('fa5s.database', self.db_exp))

        cl.addWidget(self._lbl("Tabla a exportar"))
        self.table_exp = QComboBox()
        self.table_exp.setPlaceholderText("Seleccionar tabla...")
        cl.addLayout(self._field_row('fa5s.table', self.table_exp))

        cl.addWidget(self._lbl("Formato de salida"))
        self.format_exp = QComboBox()
        self.format_exp.addItems(["CSV", "JSON", "SQL"])
        cl.addLayout(self._field_row('fa5s.file-export', self.format_exp))

        cl.addWidget(self._lbl("Carpeta de destino"))
        self.file_selector_exp = FileSelector("Seleccionar ruta de destino...", mode="directory")
        cl.addLayout(self._field_row('fa5s.folder-open', self.file_selector_exp))

        cl.addSpacing(24)

        self.btn_export = AnimatedButton("Ejecutar Exportación")
        self.btn_export.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_export.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP_COLORS['ACCENT']};
                color: #FFFFFF;
                border-radius: 6px;
                padding: 10px 0;
            }}
            QPushButton:hover {{ background-color: {APP_COLORS['ACCENT_DARK']}; }}
        """)
        cl.addWidget(self.btn_export)

        return page

    def _form_import(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        cl = QVBoxLayout(page)
        cl.setContentsMargins(32, 32, 32, 32)
        cl.setSpacing(18)

        title = QLabel("Importar Datos")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {APP_COLORS['TEXT_LIGHT']};")
        cl.addWidget(title)
        
        cl.addSpacing(8)

        cl.addWidget(self._lbl("Formato del archivo"))
        self.format_imp = QComboBox()
        self.format_imp.addItems(["CSV", "JSON", "SQL"])
        cl.addLayout(self._field_row('fa5s.file-import', self.format_imp))

        cl.addWidget(self._lbl("Archivo de origen"))
        self.file_selector_imp = FileSelector("Seleccionar archivo...", mode="file")
        cl.addLayout(self._field_row('fa5s.file', self.file_selector_imp))

        cl.addWidget(self._lbl("Base de datos destino"))
        self.db_imp = QComboBox()
        self.db_imp.setPlaceholderText("Seleccionar base de datos...")
        cl.addLayout(self._field_row('fa5s.database', self.db_imp))

        cl.addWidget(self._lbl("Tabla destino"))
        self.table_imp = QComboBox()
        self.table_imp.setPlaceholderText("Seleccionar tabla...")
        cl.addLayout(self._field_row('fa5s.table', self.table_imp))

        cl.addSpacing(24)

        self.btn_import = AnimatedButton("Ejecutar Importación")
        self.btn_import.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_import.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP_COLORS['WARNING']};
                color: #FFFFFF;
                border-radius: 6px;
                padding: 10px 0;
            }}
            QPushButton:hover {{ background-color: #B07D15; }}
        """)
        cl.addWidget(self.btn_import)

        return page

    # API Pública para Controller
    def show_message(self, section: str, message: str, msg_type: str = "info"):
        self.log_area.append_log(message, msg_type)

    def clear_messages(self):
        self.log_area.clear()
