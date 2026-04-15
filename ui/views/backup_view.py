from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QLineEdit, QProgressBar,
    QCheckBox, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor, QColor
from datetime import datetime

from ui.components.animated_button import AnimatedButton
from ui.components.log_text_edit import LogTextEdit


class BackupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(860, 560)
        self._build_ui()
        self._setup_connections()

    def _setup_connections(self):
        self.btn_refresh.clicked.connect(self._on_refresh_clicked)
        self.btn_select_dir.clicked.connect(self._on_select_directory)
        self.btn_backup.clicked.connect(self._on_backup_clicked)
        self.btn_refresh_restore.clicked.connect(self._on_refresh_restore)
        self.btn_select_schema.clicked.connect(self._on_select_schema)
        self.btn_select_data.clicked.connect(self._on_select_data)
        self.btn_restore.clicked.connect(self._on_restore_clicked)

    # ══════════════════════════════════════════════════════════════════════════
    # Construcción principal
    # ══════════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        # Widgets que el controller necesita (inicialización temprana)
        self.combo_db          = QComboBox()
        self.path_input        = QLineEdit()
        self.btn_refresh       = QPushButton()
        self.btn_select_dir    = QPushButton()
        self.combo_db_restore  = QComboBox()
        self.combo_db_restore.setEditable(True)
        self.combo_mode_restore = QComboBox()
        self.schema_input      = QLineEdit()
        self.data_input        = QLineEdit()
        self.btn_refresh_restore = QPushButton()
        self.btn_select_schema   = QPushButton()
        self.btn_select_data     = QPushButton()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Page header
        root.addWidget(self._page_header())

        # Tab bar + contenido
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)          # quita el borde del panel

        self.tabs.addTab(self._tab_create(),   "  Crear respaldo  ")
        self.tabs.addTab(self._tab_restore(),  "  Restaurar  ")
        self.tabs.addTab(self._tab_log(),      "  Registro  ")

        wrapper = QFrame()
        wl = QVBoxLayout(wrapper)
        wl.setContentsMargins(24, 0, 24, 24)
        wl.setSpacing(0)
        wl.addWidget(self.tabs)

        root.addWidget(wrapper, 1)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — Crear respaldo
    # ══════════════════════════════════════════════════════════════════════════

    def _tab_create(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 20, 0, 0)
        outer.setSpacing(0)

        # Card
        card = QFrame()
        card.setObjectName("formCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 24)
        cl.setSpacing(18)

        # — Base de datos —
        cl.addWidget(self._group_title("Base de datos"))
        db_row = QHBoxLayout(); db_row.setSpacing(8)
        self.combo_db.setPlaceholderText("Seleccionar base de datos...")
        self.btn_refresh.setText("↺")
        self.btn_refresh.setFixedWidth(34)
        self.btn_refresh.setToolTip("Actualizar lista")
        self.btn_refresh.setProperty("class", "btn-secondary-animated")
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        db_row.addWidget(self.combo_db, 1)
        db_row.addWidget(self.btn_refresh)
        cl.addLayout(db_row)

        # — Directorio —
        cl.addWidget(self._group_title("Directorio de destino"))
        dir_row = QHBoxLayout(); dir_row.setSpacing(8)
        self.path_input.setPlaceholderText("Ej.  C:/backups/mysql")
        self.btn_select_dir.setText("Examinar")
        self.btn_select_dir.setProperty("class", "btn-secondary-animated")
        self.btn_select_dir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        dir_row.addWidget(self.path_input, 1)
        dir_row.addWidget(self.btn_select_dir)
        cl.addLayout(dir_row)

        # — Nombre opcional —
        cl.addWidget(self._group_title("Nombre del archivo  \u00b7  opcional"))
        self.custom_name = QLineEdit()
        self.custom_name.setPlaceholderText("Se genera automáticamente si se deja vacío")
        cl.addWidget(self.custom_name)

        # Divisor
        cl.addWidget(self._hdiv())

        # — Opciones —
        cl.addWidget(self._group_title("Opciones"))
        opts = QHBoxLayout(); opts.setSpacing(24)
        self.chk_compress    = QCheckBox("Comprimir (.zip)")
        self.chk_compress.setChecked(True)
        self.chk_drop_tables = QCheckBox("DROP TABLE IF EXISTS")
        self.chk_create_db   = QCheckBox("CREATE DATABASE")
        for chk in (self.chk_compress, self.chk_drop_tables, self.chk_create_db):
            chk.setFont(QFont("Segoe UI", 12))
            opts.addWidget(chk)
        opts.addStretch()
        cl.addLayout(opts)

        # — Progress —
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setVisible(False)
        cl.addWidget(self.progress_bar)

        # — Stats —
        stats = QHBoxLayout()
        self.stats_last_backup  = QLabel("Último backup: —")
        self.stats_backup_count = QLabel("Realizados: 0")
        for lbl in (self.stats_last_backup, self.stats_backup_count):
            lbl.setFont(QFont("Segoe UI", 11))
            lbl.setProperty("class", "text-hint")
        stats.addWidget(self.stats_last_backup)
        stats.addStretch()
        stats.addWidget(self.stats_backup_count)
        cl.addLayout(stats)

        # — Botones — full-width al final de la card
        btn_row = QHBoxLayout(); btn_row.setSpacing(8)
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setProperty("class", "btn-secondary-animated")
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setVisible(False)
        self.btn_cancel.clicked.connect(self._on_cancel_backup)

        self.btn_backup = AnimatedButton("Crear copia de seguridad")
        self.btn_backup.setProperty("class", "btn-primary")

        btn_row.addWidget(self.btn_cancel)
        btn_row.addStretch()
        btn_row.addWidget(self.btn_backup)
        cl.addLayout(btn_row)

        outer.addWidget(card)
        outer.addStretch()
        return page

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — Restaurar
    # ══════════════════════════════════════════════════════════════════════════

    def _tab_restore(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 20, 0, 0)
        outer.setSpacing(0)

        card = QFrame()
        card.setObjectName("formCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(28, 24, 28, 24)
        cl.setSpacing(18)

        # — BD destino —
        cl.addWidget(self._group_title("Base de datos destino"))
        bd_row = QHBoxLayout(); bd_row.setSpacing(8)
        self.combo_db_restore.setPlaceholderText("Nombre de BD nueva o existente...")
        self.btn_refresh_restore.setText("↺")
        self.btn_refresh_restore.setFixedWidth(34)
        self.btn_refresh_restore.setProperty("class", "btn-secondary-animated")
        self.btn_refresh_restore.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        bd_row.addWidget(self.combo_db_restore, 1)
        bd_row.addWidget(self.btn_refresh_restore)
        cl.addLayout(bd_row)

        # — Modalidad —
        cl.addWidget(self._group_title("Modalidad"))
        self.combo_mode_restore.addItems(["Archivo único (.sql)", "Esquema y datos separados"])
        self.combo_mode_restore.currentIndexChanged.connect(self._toggle_restore_mode)
        cl.addWidget(self.combo_mode_restore)

        # — Archivo SQL —
        cl.addWidget(self._group_title("Archivo SQL"))
        sch_row = QHBoxLayout(); sch_row.setSpacing(8)
        self.schema_input.setPlaceholderText("Seleccionar archivo .sql...")
        self.btn_select_schema.setText("Buscar")
        self.btn_select_schema.setProperty("class", "btn-secondary-animated")
        self.btn_select_schema.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        sch_row.addWidget(self.schema_input, 1)
        sch_row.addWidget(self.btn_select_schema)
        cl.addLayout(sch_row)

        # — Datos separados (oculto) —
        self.data_section = QFrame()
        ds = QVBoxLayout(self.data_section)
        ds.setContentsMargins(0, 0, 0, 0); ds.setSpacing(8)
        ds.addWidget(self._group_title("Archivo de datos"))
        data_row = QHBoxLayout(); data_row.setSpacing(8)
        self.data_input.setPlaceholderText("Seleccionar archivo de datos .sql...")
        self.btn_select_data.setText("Buscar")
        self.btn_select_data.setProperty("class", "btn-secondary-animated")
        self.btn_select_data.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        data_row.addWidget(self.data_input, 1)
        data_row.addWidget(self.btn_select_data)
        ds.addLayout(data_row)
        self.data_section.setVisible(False)
        cl.addWidget(self.data_section)

        # Divisor
        cl.addWidget(self._hdiv())

        # — Advertencia —
        warn = QLabel(
            "⚠   Esta operación sobreescribirá todos los datos existentes "
            "en la base de datos destino. Esta acción no se puede deshacer."
        )
        warn.setProperty("class", "warning-box")
        warn.setWordWrap(True)
        warn.setFont(QFont("Segoe UI", 12))
        cl.addWidget(warn)

        # — Progress —
        self.progress_bar_restore = QProgressBar()
        self.progress_bar_restore.setFixedHeight(4)
        self.progress_bar_restore.setVisible(False)
        cl.addWidget(self.progress_bar_restore)

        # — Botón —
        self.btn_restore = AnimatedButton("Restaurar backup")
        self.btn_restore.setProperty("class", "btn-secondary-animated")
        cl.addWidget(self.btn_restore)   # full-width

        outer.addWidget(card)
        outer.addStretch()
        return page

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — Registro / Log
    # ══════════════════════════════════════════════════════════════════════════

    def _tab_log(self) -> QWidget:
        page = QWidget()
        page.setStyleSheet("background: transparent;")
        outer = QVBoxLayout(page)
        outer.setContentsMargins(0, 20, 0, 0)
        outer.setSpacing(0)

        card = QFrame()
        card.setObjectName("terminalCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Header de la terminal
        term_hdr = QFrame()
        term_hdr.setFixedHeight(38)
        term_hdr.setStyleSheet("""
            QFrame {
                background-color: #161B22;
                border-bottom: 1px solid #30363D;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
            }
        """)
        th_lay = QHBoxLayout(term_hdr)
        th_lay.setContentsMargins(14, 0, 14, 0)

        # Dots decorativos tipo macOS
        for color in ("#F85149", "#D29922", "#3FB950"):
            dot = QLabel("●")
            dot.setStyleSheet(f"color: {color}; font-size: 10px;")
            th_lay.addWidget(dot)
        th_lay.addSpacing(10)

        term_title = QLabel("Salida del proceso")
        term_title.setFont(QFont("Segoe UI", 11))
        term_title.setStyleSheet("color: #7D8590;")
        th_lay.addWidget(term_title)
        th_lay.addStretch()

        clr_btn = QPushButton("Limpiar")
        clr_btn.setObjectName("btnSecondary")
        clr_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        clr_btn.clicked.connect(self.clear_log)
        th_lay.addWidget(clr_btn)

        cl.addWidget(term_hdr)

        # Área de texto
        self.log_area = LogTextEdit()
        self.log_area.setObjectName("logArea")
        self.log_area.setMinimumHeight(300)
        cl.addWidget(self.log_area, 1)

        outer.addWidget(card, 1)
        return page

    # ══════════════════════════════════════════════════════════════════════════
    # Helpers visuales
    # ══════════════════════════════════════════════════════════════════════════

    def _page_header(self) -> QFrame:
        h = QFrame()
        h.setStyleSheet("QFrame { border-bottom: 1px solid #21262D; }")
        l = QVBoxLayout(h)
        l.setContentsMargins(24, 18, 24, 0)
        l.setSpacing(3)
        t = QLabel("Backups")
        t.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        t.setProperty("class", "view-title")
        s = QLabel("Crea y restaura copias de seguridad de tus bases de datos MySQL.")
        s.setFont(QFont("Segoe UI", 12))
        s.setProperty("class", "text-muted")
        l.addWidget(t); l.addWidget(s)
        return h

    def _group_title(self, text: str) -> QLabel:
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        lbl.setProperty("class", "text-muted")
        return lbl

    def _hdiv(self) -> QFrame:
        d = QFrame()
        d.setFixedHeight(1)
        d.setStyleSheet("background-color: #21262D; border: none;")
        return d

    # ══════════════════════════════════════════════════════════════════════════
    # Lógica
    # ══════════════════════════════════════════════════════════════════════════

    def _toggle_restore_mode(self, index: int):
        self.data_section.setVisible(index == 1)
        if index == 1:
            self.schema_input.setPlaceholderText("Ej. sakila-schema.sql")
            self.data_input.setPlaceholderText("Ej. sakila-data.sql")
        else:
            self.schema_input.setPlaceholderText("Seleccionar archivo .sql...")
            self.data_input.clear()

    def _on_refresh_clicked(self):
        self._log("Actualizando lista de bases de datos...", "process")
        QTimer.singleShot(900, lambda: self._log("Lista actualizada", "success"))

    def _on_refresh_restore(self):
        self._log("Actualizando bases de datos disponibles...", "process")
        QTimer.singleShot(900, lambda: self._log("Lista actualizada", "success"))

    def _on_select_directory(self):
        from PyQt6.QtWidgets import QFileDialog
        d = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de backup")
        if d:
            self.path_input.setText(d)
            self._log(f"Directorio seleccionado: {d}", "info")

    def _on_select_schema(self):
        from PyQt6.QtWidgets import QFileDialog
        f, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo SQL", "", "SQL Files (*.sql)")
        if f:
            self.schema_input.setText(f)
            self._log(f"Archivo SQL: {f}", "info")

    def _on_select_data(self):
        from PyQt6.QtWidgets import QFileDialog
        f, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de datos", "", "SQL Files (*.sql)")
        if f:
            self.data_input.setText(f)
            self._log(f"Archivo de datos: {f}", "info")

    def _on_backup_clicked(self):
        if not self.path_input.text():
            self._log("Selecciona un directorio de destino", "error"); return
        if not self.combo_db.currentText():
            self._log("Selecciona una base de datos", "error"); return

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.btn_backup.setEnabled(False)
        self.btn_cancel.setVisible(True)
        self._log(f"Iniciando backup de '{self.combo_db.currentText()}'...", "process")
        # Redirigir al tab de log para que el usuario vea el progreso
        self.tabs.setCurrentIndex(2)
        QTimer.singleShot(3000, self._sim_backup_done)

    def _sim_backup_done(self):
        self.progress_bar.setValue(100)
        self._log(f"Backup completado en: {self.path_input.text()}", "success")
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.stats_last_backup.setText(f"Último: {now}")
        count = int(self.stats_backup_count.text().split(": ")[-1])
        self.stats_backup_count.setText(f"Realizados: {count + 1}")
        QTimer.singleShot(800, self._reset_backup_ui)

    def _reset_backup_ui(self):
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.btn_backup.setEnabled(True)
        self.btn_cancel.setVisible(False)

    def _on_cancel_backup(self):
        self._log("Backup cancelado por el usuario", "warning")
        self._reset_backup_ui()

    def _on_restore_clicked(self):
        if not self.combo_db_restore.currentText():
            self._log("Selecciona o escribe el nombre de la BD destino", "error"); return
        if not self.schema_input.text():
            self._log("Selecciona el archivo SQL a restaurar", "error"); return
        self._log(f"Iniciando restauración en '{self.combo_db_restore.currentText()}'...", "process")
        self.tabs.setCurrentIndex(2)
        self.progress_bar_restore.setVisible(True)
        self.progress_bar_restore.setValue(0)
        QTimer.singleShot(3000, lambda: (
            self.progress_bar_restore.setValue(100),
            self._log("Restauración completada exitosamente", "success"),
            QTimer.singleShot(800, lambda: (
                setattr(self.progress_bar_restore, 'visible', False),
                self.progress_bar_restore.setVisible(False)
            ))
        ))

    def _log(self, msg: str, msg_type: str = "info"):
        self.log_area.append_log(msg, msg_type)

    # ══════════════════════════════════════════════════════════════════════════
    # API pública (compatibilidad con BackupController)
    # ══════════════════════════════════════════════════════════════════════════

    def log_message(self, msg: str, msg_type: str = "info"):
        self._log(msg, msg_type)

    def clear_log(self):
        self.log_area.clear()
        self._log("Registro limpiado", "info")

    def set_backup_progress(self, value: int):
        self.progress_bar.setValue(value)

    def update_database_list(self, databases: list):
        self.combo_db.clear()
        self.combo_db.addItems(databases)
        self.combo_db_restore.clear()
        self.combo_db_restore.addItems(databases)