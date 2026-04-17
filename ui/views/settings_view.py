"""
settings_view.py — Vista de Configuración para JuanDB.

Arquitectura:
    SettingsView(QWidget)
        ├── _CategoryList(QListWidget)     ← Panel izquierdo
        ├── _GeneralPage(QWidget)          ← Página General
        ├── _InterfacePage(QWidget)        ← Página Interfaz
        └── _DatabasePage(QWidget)         ← Página Base de Datos
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QLineEdit,
    QPushButton, QCheckBox, QComboBox, QSlider, QSpinBox,
    QListWidget, QListWidgetItem, QStackedWidget, QFileDialog,
    QSizePolicy, QAbstractItemView
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QCursor

from ui.components.server_status_checker import ServerStatusChecker
from ui.components.help_icon import HelpIcon


# ═════════════════════════════════════════════════════════════════════════════
# Helpers compartidos — reutilizados por todas las páginas
# ═════════════════════════════════════════════════════════════════════════════

def _section(title: str) -> QFrame:
    """
    QFrame tipo 'section card' con título y bordes redondeados de 8px.
    Equivale al BG_CARD del sistema de diseño.
    """
    frame = QFrame()
    frame.setProperty("class", "section-card")
    outer = QVBoxLayout(frame)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)

    # Encabezado de sección
    hdr = QFrame()
    hdr.setProperty("class", "section-header")
    hdr.setFixedHeight(40)
    hl = QHBoxLayout(hdr)
    hl.setContentsMargins(16, 0, 16, 0)

    t = QLabel(title)
    t.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
    t.setProperty("class", "text-adaptive")
    hl.addWidget(t)

    # Área de contenido
    body = QFrame()
    body.setObjectName("_sectionBody")
    body.setStyleSheet("QFrame#_sectionBody { background: transparent; border: none; }")
    body_lay = QVBoxLayout(body)
    body_lay.setContentsMargins(16, 16, 16, 16)
    body_lay.setSpacing(16)

    outer.addWidget(hdr)
    outer.addWidget(body)

    # Adjuntamos el layout del body al frame para que las páginas puedan usarlo
    frame._body = body_lay   # type: ignore[attr-defined]
    return frame


def _field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
    lbl.setStyleSheet(f"color: {'#7D8590'}; border: none;")
    return lbl


def _input() -> QLineEdit:
    le = QLineEdit()
    le.setFixedHeight(36)
    return le


def _hint(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setFont(QFont("Segoe UI", 10))
    lbl.setProperty("class", "text-hint")
    lbl.setWordWrap(True)
    return lbl


def _hdiv() -> QFrame:
    d = QFrame()
    d.setFixedHeight(1)
    d.setProperty("class", "h-separator")
    return d


# ═════════════════════════════════════════════════════════════════════════════
# _GeneralPage
# ═════════════════════════════════════════════════════════════════════════════

class _GeneralPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        # ── Sección: Backups ─────────────────────────────────────────────────
        sec_bk = _section("Backups")
        bk = sec_bk._body

        bk.addWidget(_field_label("Ruta por defecto de respaldos"))
        path_row = QHBoxLayout(); path_row.setSpacing(6)
        self.txt_backup_path = _input()
        self.txt_backup_path.setPlaceholderText("Ej.  C:/backups/mysql")
        btn_browse = QPushButton("Examinar")
        btn_browse.setFixedHeight(36)
        btn_browse.setProperty("class", "btn-secondary-animated")
        btn_browse.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_browse.clicked.connect(self._browse_path)
        path_row.addWidget(self.txt_backup_path, 1)
        path_row.addWidget(btn_browse)
        bk.addLayout(path_row)
        bk.addWidget(_hint("Esta ruta se usará como destino por defecto al crear nuevos respaldos."))

        root.addWidget(sec_bk)

        # ── Sección: Inicio ──────────────────────────────────────────────────
        sec_start = _section("Inicio de la aplicación")
        st = sec_start._body

        self.chk_minimized   = QCheckBox("Iniciar la aplicación minimizada")
        self.chk_autoconnect = QCheckBox("Conectar automáticamente al servidor al iniciar")
        self.chk_check_update = QCheckBox("Buscar actualizaciones al iniciar")
        for chk in (self.chk_minimized, self.chk_autoconnect, self.chk_check_update):
            chk.setFont(QFont("Segoe UI", 12))
            chk.setProperty("class", "text-adaptive")
            st.addWidget(chk)
        self.chk_autoconnect.setChecked(True)

        root.addWidget(sec_start)
        root.addStretch()

    def _browse_path(self):
        d = QFileDialog.getExistingDirectory(self, "Seleccionar carpeta de respaldos")
        if d:
            self.txt_backup_path.setText(d)

    def get_values(self) -> dict:
        return {
            "backup_path":   self.txt_backup_path.text(),
            "start_minimized":  self.chk_minimized.isChecked(),
            "autoconnect":   self.chk_autoconnect.isChecked(),
            "check_updates": self.chk_check_update.isChecked(),
        }

    def set_values(self, cfg: dict):
        self.txt_backup_path.setText(cfg.get("backup_path", ""))
        self.chk_minimized.setChecked(cfg.get("start_minimized", False))
        self.chk_autoconnect.setChecked(cfg.get("autoconnect", True))
        self.chk_check_update.setChecked(cfg.get("check_updates", False))


# ═════════════════════════════════════════════════════════════════════════════
# _InterfacePage
# ═════════════════════════════════════════════════════════════════════════════

class _InterfacePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        # ── Sección: Apariencia ──────────────────────────────────────────────
        sec_ap = _section("Apariencia")
        ap = sec_ap._body

        ap.addWidget(_field_label("Tema de la interfaz"))
        fmt_row = QHBoxLayout(); fmt_row.setSpacing(0)
        self.cmb_theme = QComboBox()
        self.cmb_theme.addItems(["Oscuro (Dark Pro)", "Claro (Light)"])
        self.cmb_theme.setFixedHeight(36)
        self.cmb_theme.setFixedWidth(240)
        fmt_row.addWidget(self.cmb_theme); fmt_row.addStretch()
        ap.addLayout(fmt_row)

        ap.addWidget(_hdiv())

        ap.addWidget(_field_label("Idioma"))
        lang_row = QHBoxLayout(); lang_row.setSpacing(0)
        self.cmb_lang = QComboBox()
        self.cmb_lang.addItems(["Español", "English"])
        self.cmb_lang.setFixedHeight(36)
        self.cmb_lang.setFixedWidth(180)
        lang_row.addWidget(self.cmb_lang); lang_row.addStretch()
        ap.addLayout(lang_row)

        root.addWidget(sec_ap)

        # ── Sección: Consola / Log ───────────────────────────────────────────
        sec_con = _section("Consola / Registro")
        cn = sec_con._body

        cn.addWidget(_field_label("Tamaño de fuente de la consola"))
        slider_row = QHBoxLayout(); slider_row.setSpacing(12)
        self.sld_font = QSlider(Qt.Orientation.Horizontal)
        self.sld_font.setRange(9, 18)
        self.sld_font.setValue(12)
        self.sld_font.setFixedHeight(20)

        self.lbl_font_size = QLabel("12 px")
        self.lbl_font_size.setFont(QFont("Segoe UI", 11, QFont.Weight.DemiBold))
        self.lbl_font_size.setProperty("class", "text-accent")
        self.lbl_font_size.setFixedWidth(44)
        self.sld_font.valueChanged.connect(
            lambda v: self.lbl_font_size.setText(f"{v} px")
        )
        slider_row.addWidget(self.sld_font, 1)
        slider_row.addWidget(self.lbl_font_size)
        cn.addLayout(slider_row)
        cn.addWidget(_hint("Afecta al área de registro (log) en la vista de Backups."))

        cn.addWidget(_hdiv())

        self.chk_timestamps = QCheckBox("Mostrar marca de tiempo en el registro")
        self.chk_timestamps.setFont(QFont("Segoe UI", 12))
        self.chk_timestamps.setChecked(True)
        self.chk_timestamps.setProperty("class", "text-adaptive")
        cn.addWidget(self.chk_timestamps)

        root.addWidget(sec_con)
        root.addStretch()

    def get_values(self) -> dict:
        return {
            "theme":           self.cmb_theme.currentIndex(),
            "language":        self.cmb_lang.currentIndex(),
            "console_font_sz": self.sld_font.value(),
            "log_timestamps":  self.chk_timestamps.isChecked(),
        }

    def set_values(self, cfg: dict):
        self.cmb_theme.setCurrentIndex(cfg.get("theme", 0))
        self.cmb_lang.setCurrentIndex(cfg.get("language", 0))
        self.sld_font.setValue(cfg.get("console_font_sz", 12))
        self.chk_timestamps.setChecked(cfg.get("log_timestamps", True))


# ═════════════════════════════════════════════════════════════════════════════
# _DatabasePage
# ═════════════════════════════════════════════════════════════════════════════

class _DatabasePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(16)

        # ── Sección: Conexión ────────────────────────────────────────────────
        sec_conn = _section("Conexión")
        co = sec_conn._body

        co.addWidget(_field_label("Timeout de conexión (segundos)"))
        to_row = QHBoxLayout(); to_row.setSpacing(0)
        self.spin_timeout = QSpinBox()
        self.spin_timeout.setRange(5, 120)
        self.spin_timeout.setValue(30)
        self.spin_timeout.setFixedHeight(36)
        self.spin_timeout.setFixedWidth(100)
        self.spin_timeout.setSuffix("  seg")

        to_row.addWidget(self.spin_timeout); to_row.addStretch()
        co.addLayout(to_row)
        co.addWidget(_hint("Tiempo máximo de espera antes de cancelar una operación de conexión."))

        co.addWidget(_hdiv())

        co.addWidget(_field_label("Máximo de reintentos al perder la conexión"))
        rt_row = QHBoxLayout(); rt_row.setSpacing(0)
        self.spin_retries = QSpinBox()
        self.spin_retries.setRange(0, 10)
        self.spin_retries.setValue(3)
        self.spin_retries.setFixedHeight(36)
        self.spin_retries.setFixedWidth(100)
        self.spin_retries.setSuffix("  intentos")
        rt_row.addWidget(self.spin_retries); rt_row.addStretch()
        co.addLayout(rt_row)

        root.addWidget(sec_conn)

        # ── Sección: Logs ────────────────────────────────────────────────────
        sec_logs = _section("Registro de errores")
        lo = sec_logs._body

        self.chk_autosave_logs = QCheckBox("Auto-guardar logs de errores automáticamente")
        self.chk_autosave_logs.setFont(QFont("Segoe UI", 12))
        self.chk_autosave_logs.setChecked(True)
        self.chk_autosave_logs.setProperty("class", "text-adaptive")
        lo.addWidget(self.chk_autosave_logs)
        lo.addWidget(_hint("Los errores se guardarán en logs/errors.log dentro de la carpeta de la aplicación."))

        lo.addWidget(_hdiv())

        lo.addWidget(_field_label("Retención de logs (días)"))
        ret_row = QHBoxLayout(); ret_row.setSpacing(0)
        self.spin_log_days = QSpinBox()
        self.spin_log_days.setRange(1, 365)
        self.spin_log_days.setValue(30)
        self.spin_log_days.setFixedHeight(36)
        self.spin_log_days.setFixedWidth(100)
        self.spin_log_days.setSuffix("  días")
        ret_row.addWidget(self.spin_log_days); ret_row.addStretch()
        lo.addLayout(ret_row)
        lo.addWidget(_hint("Los registros más antiguos serán eliminados automáticamente."))

        root.addWidget(sec_logs)

        # ── Sección: Estado del servidor ────────────────────────────────────
        sec_status = _section("Estado del servidor")
        ss = sec_status._body

        ss.addWidget(_hint(
            "Verifica si el servidor MySQL / MariaDB responde correctamente "
            "usando las credenciales almacenadas en la configuración actual."
        ))
        self.server_checker = ServerStatusChecker()
        ss.addWidget(self.server_checker)

        root.addWidget(sec_status)
        root.addStretch()

    def get_values(self) -> dict:
        return {
            "connection_timeout": self.spin_timeout.value(),
            "max_retries":        self.spin_retries.value(),
            "autosave_logs":      self.chk_autosave_logs.isChecked(),
            "log_retention_days": self.spin_log_days.value(),
        }

    def set_values(self, cfg: dict):
        self.spin_timeout.setValue(cfg.get("connection_timeout", 30))
        self.spin_retries.setValue(cfg.get("max_retries", 3))
        self.chk_autosave_logs.setChecked(cfg.get("autosave_logs", True))
        self.spin_log_days.setValue(cfg.get("log_retention_days", 30))


# ═════════════════════════════════════════════════════════════════════════════
# SettingsView — Vista principal
# ═════════════════════════════════════════════════════════════════════════════

class SettingsView(QWidget):
    """
    Vista de Configuración: selector lateral de categorías + contenido apilado.
    """

    settings_saved = pyqtSignal(dict)   # Emite el diccionario de configuración

    _CATEGORIES = [
        ("⊛", "General"),
        ("◈", "Interfaz"),
        ("⊚", "Base de Datos"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(860, 520)
        self._build_ui()

    # ── Construcción ──────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        top_bar = QHBoxLayout()
        top_bar.setContentsMargins(24, 18, 24, 0)
        top_bar.addStretch()
        top_bar.addWidget(HelpIcon("Personaliza el comportamiento, la apariencia y la conexión de JuanDB."))
        root.addLayout(top_bar)

        # Cuerpo: lista izquierda + stack derecho
        body = QFrame()
        body.setStyleSheet("background: transparent; border: none;")
        bl = QHBoxLayout(body)
        bl.setContentsMargins(24, 20, 24, 0)
        bl.setSpacing(16)

        bl.addWidget(self._category_list(), 0)
        bl.addWidget(self._content_stack(), 1)

        root.addWidget(body, 1)
        root.addWidget(self._action_bar())

    # ── Lista de categorías (izquierda) ───────────────────────────────────────

    def _category_list(self) -> QListWidget:
        self.cat_list = QListWidget()
        self.cat_list.setFixedWidth(180)
        self.cat_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.cat_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        for icon, label in self._CATEGORIES:
            item = QListWidgetItem(f"  {icon}   {label}")
            item.setFont(QFont("Segoe UI", 12))
            self.cat_list.addItem(item)

        self.cat_list.setCurrentRow(0)
        self.cat_list.currentRowChanged.connect(self._on_category_changed)
        return self.cat_list

    # ── Stack de contenido (derecha) ──────────────────────────────────────────

    def _content_stack(self) -> QStackedWidget:
        self.stack = QStackedWidget()

        self.page_general   = _GeneralPage()
        self.page_interface = _InterfacePage()
        self.page_database  = _DatabasePage()

        for page in (self.page_general, self.page_interface, self.page_database):
            self.stack.addWidget(page)

        return self.stack

    # ── Barra de acciones ─────────────────────────────────────────────────────

    def _action_bar(self) -> QFrame:
        bar = QFrame()
        bar.setFixedHeight(64)
        bar.setObjectName("pageHeader")
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(24, 0, 24, 0)
        lay.setSpacing(10)

        # Feedback de guardado
        self._lbl_saved = QLabel("")
        self._lbl_saved.setFont(QFont("Segoe UI", 12))
        self._lbl_saved.setProperty("class", "text-SUCCESS".lower())

        # Botón restablecer
        btn_reset = QPushButton("Restablecer valores")
        btn_reset.setProperty("class", "btn-secondary-animated")
        btn_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_reset.setFixedHeight(38)
        btn_reset.clicked.connect(self._on_reset)

        # Botón guardar — color acento
        self.btn_save = QPushButton("Guardar cambios")
        self.btn_save.setProperty("class", "btn-primary")
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.setFixedHeight(38)
        self.btn_save.setFont(QFont("Segoe UI", 12, QFont.Weight.DemiBold))
        self.btn_save.clicked.connect(self._on_save)

        lay.addWidget(self._lbl_saved)
        lay.addStretch()
        lay.addWidget(btn_reset)
        lay.addWidget(self.btn_save)
        return bar

    # ── Lógica ────────────────────────────────────────────────────────────────

    def _on_category_changed(self, index: int):
        self.stack.setCurrentIndex(index)

    def _on_save(self):
        cfg = self.get_all_values()
        self.settings_saved.emit(cfg)
        self._lbl_saved.setText("✓  Cambios guardados")
        QTimer.singleShot(3000, lambda: self._lbl_saved.setText(""))

    def _on_reset(self):
        self.page_general.set_values({})
        self.page_interface.set_values({})
        self.page_database.set_values({})
        self._lbl_saved.setProperty("class", "text-INFO".lower())
        self._lbl_saved.setText("↺  Valores restablecidos")
        QTimer.singleShot(3000, lambda: (
            self._lbl_saved.setText(""),
            self._lbl_saved.setProperty("class", "text-SUCCESS".lower())
        ))

    # ── API pública ───────────────────────────────────────────────────────────

    def get_all_values(self) -> dict:
        """Retorna un diccionario plano con la configuración completa."""
        return {
            **self.page_general.get_values(),
            **self.page_interface.get_values(),
            **self.page_database.get_values(),
        }

    def load_config(self, cfg: dict):
        """Carga un diccionario de configuración en todos los paneles."""
        self.page_general.set_values(cfg)
        self.page_interface.set_values(cfg)
        self.page_database.set_values(cfg)
