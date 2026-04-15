from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QCheckBox, QStackedWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QCursor

from ui.components.animated_button import AnimatedButton
from ui.components.file_selector import FileSelector


class ImportExportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(860, 520)
        self._active_mode = "export"   # "export" | "import"
        self._build_ui()

    # ══════════════════════════════════════════════════════════════════════════
    # Construcción
    # ══════════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._page_header())
        root.addWidget(self._mode_toggle_bar())

        # Área central con ancho máximo para evitar inputs kilométricos
        center_wrapper = QFrame()
        cw_layout = QHBoxLayout(center_wrapper)
        cw_layout.setContentsMargins(0, 24, 0, 24)

        self.stack = QStackedWidget()
        self.stack.setMaximumWidth(600)
        self.stack.setMinimumWidth(400)
        self.stack.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        self.stack.addWidget(self._form_export())   # index 0
        self.stack.addWidget(self._form_import())   # index 1

        cw_layout.addStretch()
        cw_layout.addWidget(self.stack, 0)
        cw_layout.addStretch()

        root.addWidget(center_wrapper, 1)

    # ── Page header ───────────────────────────────────────────────────────────

    def _page_header(self) -> QFrame:
        h = QFrame()
        h.setStyleSheet("QFrame { border-bottom: 1px solid #21262D; }")
        l = QVBoxLayout(h)
        l.setContentsMargins(24, 18, 24, 14)
        l.setSpacing(3)

        t = QLabel("Importar / Exportar")
        t.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        t.setProperty("class", "view-title")

        s = QLabel("Transfiere datos entre tus tablas y archivos locales en formato CSV o JSON.")
        s.setFont(QFont("Segoe UI", 12))
        s.setProperty("class", "text-muted")

        l.addWidget(t); l.addWidget(s)
        return h

    # ── Toggle de modo (Exportar / Importar) ──────────────────────────────────

    def _mode_toggle_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet("QFrame { border-bottom: 1px solid #21262D; background: transparent; }")
        bar.setFixedHeight(52)

        lay = QHBoxLayout(bar)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addStretch()

        # Pill container
        pill = QFrame()
        pill.setFixedHeight(36)
        pill.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border: 1px solid #30363D;
                border-radius: 8px;
            }
        """)
        pill_lay = QHBoxLayout(pill)
        pill_lay.setContentsMargins(4, 4, 4, 4)
        pill_lay.setSpacing(2)

        self.btn_mode_export = QPushButton("↑  Exportar")
        self.btn_mode_import = QPushButton("↓  Importar")

        for btn in (self.btn_mode_export, self.btn_mode_import):
            btn.setFixedHeight(28)
            btn.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setCheckable(True)
            pill_lay.addWidget(btn)

        self.btn_mode_export.setChecked(True)
        self.btn_mode_export.clicked.connect(lambda: self._switch_mode("export"))
        self.btn_mode_import.clicked.connect(lambda: self._switch_mode("import"))

        self._style_toggle_btns()

        lay.addWidget(pill)
        lay.addStretch()
        return bar

    def _style_toggle_btns(self):
        active_style = """
            QPushButton {
                background-color: #3B82F6;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-weight: 600;
            }
        """
        inactive_style = """
            QPushButton {
                background-color: transparent;
                color: #7D8590;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-weight: 500;
            }
            QPushButton:hover { color: #F0F6FC; }
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
        # Limpiar mensajes del form que queda visible
        if mode == "export":
            self.lbl_msg_exp.hide()
        else:
            self.lbl_msg_imp.hide()

    # ══════════════════════════════════════════════════════════════════════════
    # Formulario EXPORTAR
    # ══════════════════════════════════════════════════════════════════════════

    def _form_export(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        card = QFrame()
        card.setObjectName("formCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 28)
        cl.setSpacing(20)

        # Icono + título mini
        hdr = QHBoxLayout()
        ic = QLabel("↑")
        ic.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        ic.setStyleSheet("color: #3B82F6;")
        t = QLabel("Exportar datos")
        t.setFont(QFont("Segoe UI", 15, QFont.Weight.DemiBold))
        t.setProperty("class", "view-subtitle-muted")
        hdr.addWidget(ic); hdr.addSpacing(8); hdr.addWidget(t); hdr.addStretch()
        cl.addLayout(hdr)

        sub = QLabel("Descarga el contenido de una tabla a un archivo CSV o JSON en tu equipo.")
        sub.setFont(QFont("Segoe UI", 12))
        sub.setProperty("class", "text-muted")
        sub.setWordWrap(True)
        cl.addWidget(sub)

        cl.addWidget(self._hdiv())

        # Campos
        cl.addWidget(self._lbl("Base de datos"))
        self.db_exp = QComboBox()
        self.db_exp.setPlaceholderText("Seleccionar base de datos...")
        cl.addWidget(self.db_exp)

        cl.addWidget(self._lbl("Tabla a exportar"))
        self.table_exp = QComboBox()
        self.table_exp.setPlaceholderText("Seleccionar tabla...")
        cl.addWidget(self.table_exp)

        # Formato — más estrecho, no necesita todo el ancho
        cl.addWidget(self._lbl("Formato de exportación"))
        fmt_row = QHBoxLayout(); fmt_row.setSpacing(8)
        self.format_exp = QComboBox()
        self.format_exp.addItems(["CSV  —  separado por comas", "JSON  —  objetos anidados"])
        self.format_exp.setFixedWidth(260)
        fmt_row.addWidget(self.format_exp)
        fmt_row.addStretch()
        cl.addLayout(fmt_row)

        # Carpeta destino (input-group)
        cl.addWidget(self._lbl("Carpeta de destino"))
        self.file_selector_exp = FileSelector(
            "Seleccionar carpeta donde se guardará el archivo...",
            mode="directory"
        )
        cl.addWidget(self.file_selector_exp)

        # Helper text justo bajo el field
        helper = QLabel("ℹ  El archivo se nombrará automáticamente: tabla_AAAA-MM-DD.formato")
        helper.setFont(QFont("Segoe UI", 11))
        helper.setStyleSheet("color: #484F58;")
        cl.addWidget(helper)

        # Estado
        self.lbl_msg_exp = QLabel("")
        self.lbl_msg_exp.setWordWrap(True)
        self.lbl_msg_exp.setFont(QFont("Segoe UI", 12))
        self.lbl_msg_exp.hide()
        cl.addWidget(self.lbl_msg_exp)

        cl.addStretch()

        # Botón — full width, primario (verde/azul)
        self.btn_export = AnimatedButton("↑   Exportar datos")
        self.btn_export.setProperty("class", "btn-primary")
        self.btn_export.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        cl.addWidget(self.btn_export)

        outer.addWidget(card)
        return page

    # ══════════════════════════════════════════════════════════════════════════
    # Formulario IMPORTAR
    # ══════════════════════════════════════════════════════════════════════════

    def _form_import(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        card = QFrame()
        card.setObjectName("formCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 28)
        cl.setSpacing(20)

        # Icono + título
        hdr = QHBoxLayout()
        ic = QLabel("↓")
        ic.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        ic.setStyleSheet("color: #D29922;")   # ámbar = acción que modifica datos
        t = QLabel("Importar datos")
        t.setFont(QFont("Segoe UI", 15, QFont.Weight.DemiBold))
        t.setProperty("class", "view-subtitle-muted")
        hdr.addWidget(ic); hdr.addSpacing(8); hdr.addWidget(t); hdr.addStretch()
        cl.addLayout(hdr)

        sub = QLabel("Carga un archivo CSV o JSON a una tabla de tu base de datos.")
        sub.setFont(QFont("Segoe UI", 12))
        sub.setProperty("class", "text-muted")
        sub.setWordWrap(True)
        cl.addWidget(sub)

        cl.addWidget(self._hdiv())

        # Formato
        cl.addWidget(self._lbl("Formato del archivo"))
        fmt_row = QHBoxLayout(); fmt_row.setSpacing(8)
        self.format_imp = QComboBox()
        self.format_imp.addItems(["CSV  —  separado por comas", "JSON  —  objetos anidados"])
        self.format_imp.setFixedWidth(260)
        fmt_row.addWidget(self.format_imp); fmt_row.addStretch()
        cl.addLayout(fmt_row)

        # Archivo local
        cl.addWidget(self._lbl("Archivo local"))
        self.file_selector_imp = FileSelector(
            "Seleccionar archivo CSV o JSON...",
            mode="file",
            filter="Data Files (*.csv *.json);;All Files (*)"
        )
        cl.addWidget(self.file_selector_imp)

        # BD destino
        cl.addWidget(self._lbl("Base de datos destino"))
        self.db_imp = QComboBox()
        self.db_imp.setPlaceholderText("Seleccionar base de datos...")
        cl.addWidget(self.db_imp)

        # Tabla destino
        cl.addWidget(self._lbl("Tabla destino"))
        self.table_imp = QComboBox()
        self.table_imp.setPlaceholderText("Seleccionar tabla...")
        cl.addWidget(self.table_imp)

        # Checkbox sobrescribir
        self.chk_overwrite = QCheckBox("Sobrescribir registros existentes (TRUNCATE antes de insertar)")
        self.chk_overwrite.setFont(QFont("Segoe UI", 12))
        cl.addWidget(self.chk_overwrite)

        # Advertencia con ícono + fondo semitransparente
        warn_frame = QFrame()
        warn_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(210, 153, 34, 0.08);
                border: 1px solid rgba(210, 153, 34, 0.30);
                border-radius: 8px;
            }
        """)
        wl = QHBoxLayout(warn_frame)
        wl.setContentsMargins(14, 12, 14, 12)
        wl.setSpacing(12)

        warn_icon = QLabel("⚠")
        warn_icon.setFont(QFont("Segoe UI", 16))
        warn_icon.setStyleSheet("color: #D29922; border: none;")
        warn_icon.setFixedWidth(20)
        warn_icon.setAlignment(Qt.AlignmentFlag.AlignTop)

        warn_text = QLabel(
            "Las columnas del archivo deben coincidir con la estructura "
            "de la tabla destino. Registros incompatibles serán ignorados."
        )
        warn_text.setFont(QFont("Segoe UI", 12))
        warn_text.setStyleSheet("color: #D29922; border: none;")
        warn_text.setWordWrap(True)

        wl.addWidget(warn_icon); wl.addWidget(warn_text, 1)
        cl.addWidget(warn_frame)

        # Estado
        self.lbl_msg_imp = QLabel("")
        self.lbl_msg_imp.setWordWrap(True)
        self.lbl_msg_imp.setFont(QFont("Segoe UI", 12))
        self.lbl_msg_imp.hide()
        cl.addWidget(self.lbl_msg_imp)

        cl.addStretch()

        # Botón — full width, acento ámbar (acción más "peligrosa")
        self.btn_import = AnimatedButton("↓   Importar datos")
        self.btn_import.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        self.btn_import.setStyleSheet("""
            QPushButton {
                background-color: #D29922;
                border: none;
                border-radius: 6px;
                color: #FFFFFF;
                font-weight: 600;
                font-size: 13px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #B07D15; }
            QPushButton:disabled { background-color: #30363D; color: #484F58; }
        """)
        cl.addWidget(self.btn_import)

        outer.addWidget(card)
        return page

    # ══════════════════════════════════════════════════════════════════════════
    # Helpers
    # ══════════════════════════════════════════════════════════════════════════

    def _lbl(self, text: str) -> QLabel:
        l = QLabel(text)
        l.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        l.setProperty("class", "text-muted")
        return l

    def _hdiv(self) -> QFrame:
        d = QFrame()
        d.setFixedHeight(1)
        d.setStyleSheet("background-color: #21262D; border: none;")
        return d

    # ══════════════════════════════════════════════════════════════════════════
    # API pública (compatibilidad con controller)
    # ══════════════════════════════════════════════════════════════════════════

    def show_message(self, section: str, message: str, msg_type: str = "info"):
        color_map = {
            "success": "#3FB950",
            "error":   "#F85149",
            "warning": "#D29922",
            "info":    "#58A6FF",
        }
        c = color_map.get(msg_type, "#7D8590")
        lbl = self.lbl_msg_exp if section == "export" else self.lbl_msg_imp
        lbl.setText(message)
        lbl.setStyleSheet(
            f"color: {c}; border-left: 2px solid {c}; "
            f"padding: 7px 10px; border-radius: 4px; background: transparent;"
        )
        lbl.show()
        if msg_type != "error":
            QTimer.singleShot(5000, lbl.hide)

    def clear_messages(self):
        self.lbl_msg_exp.hide()
        self.lbl_msg_imp.hide()