from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QLineEdit, QProgressBar,
    QCheckBox, QTabWidget, QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor
from datetime import datetime
import qtawesome as qta

from ui.components.animated_button import AnimatedButton
from ui.components.log_text_edit import LogTextEdit
from ui.components.backup_form_card import BackupFormCard
from ui.components.help_icon import HelpIcon


class BackupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(860, 560)
        self._active_mode = "backup"
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
        self.btn_cancel.clicked.connect(self._on_cancel_backup)

    # ══════════════════════════════════════════════════════════════════════════
    # Construcción principal
    # ══════════════════════════════════════════════════════════════════════════

    def _build_ui(self):
        # Widgets de restauración (inicialización temprana para el controller)
        self.combo_db_restore   = QComboBox()
        self.combo_db_restore.setEditable(True)
        self.combo_mode_restore = QComboBox()
        self.schema_input       = QLineEdit()
        self.data_input         = QLineEdit()
        self.btn_refresh_restore = QPushButton()
        self.btn_select_schema   = QPushButton()
        self.btn_select_data     = QPushButton()

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Segmented Control / Header Layout
        header_lay = QHBoxLayout()
        header_lay.setContentsMargins(0, 0, 0, 0)
        
        spacer_left = QWidget()
        spacer_left.setFixedWidth(28)  # Compensar ancho del HelpIcon + margenes
        header_lay.addWidget(spacer_left)
        
        header_lay.addWidget(self._mode_toggle_bar(), 1)
        
        header_lay.addWidget(HelpIcon("Crea y restaura copias de seguridad de tus bases de datos MySQL."))

        self.stack = QStackedWidget()
        self.stack.addWidget(self._tab_create())
        self.stack.addWidget(self._tab_restore())

        left_col = QFrame()
        wl = QVBoxLayout(left_col)
        wl.setContentsMargins(32, 24, 24, 24)
        wl.setSpacing(24)
        wl.addLayout(header_lay)
        wl.addWidget(self.stack)

        root.addWidget(left_col, 2)
        
        # Columna de Registro
        log_panel = self._create_log_panel()
        root.addWidget(log_panel, 1)

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — Crear respaldo  (delegado a BackupFormCard)
    # ══════════════════════════════════════════════════════════════════════════

    def _tab_create(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(32, 32, 32, 32)
        outer.setSpacing(18)

        # Layout centrado para la card
        center = QHBoxLayout()
        center.setContentsMargins(0, 0, 0, 0)
        center.addStretch()

        self._form_card = BackupFormCard()
        center.addWidget(self._form_card)

        center.addStretch()
        outer.addStretch()  # Centrado vertical superior
        outer.addLayout(center)
        outer.addStretch()  # Centrado vertical inferior

        # ── Proxy de widgets para compatibilidad con BackupController ──
        self.combo_db          = self._form_card.combo_db
        self.path_input        = self._form_card.path_input
        self.custom_name       = self._form_card.custom_name
        self.btn_refresh       = self._form_card.btn_refresh
        self.btn_select_dir    = self._form_card.btn_select_dir
        self.chk_compress      = self._form_card.chk_compress
        self.chk_drop_tables   = self._form_card.chk_drop_tables
        self.chk_create_db     = self._form_card.chk_create_db
        self.progress_bar      = self._form_card.progress_bar
        self.stats_last_backup = self._form_card.stats_last_backup
        self.stats_backup_count = self._form_card.stats_backup_count
        self.btn_cancel        = self._form_card.btn_cancel
        self.btn_backup        = self._form_card.btn_backup

        return page

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — Restaurar
    # ══════════════════════════════════════════════════════════════════════════

    def _tab_restore(self) -> QWidget:
        page = QWidget()
        outer = QVBoxLayout(page)
        outer.setContentsMargins(32, 32, 32, 32)
        outer.setSpacing(18)

        # Layout centrado
        center = QHBoxLayout()
        center.setContentsMargins(0, 0, 0, 0)
        center.addStretch()

        card = QFrame()
        card.setObjectName("formCard")
        card.setFixedWidth(600)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        
        cl = QVBoxLayout(card)
        cl.setContentsMargins(32, 32, 32, 32)
        cl.setSpacing(18)
        
        title = QLabel("Restaurar Base de Datos")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setProperty("class", "view-title")
        cl.addWidget(title)
        
        cl.addSpacing(8)

        # — BD destino —
        cl.addWidget(self._field_label("Base de datos destino"))
        self.combo_db_restore.setPlaceholderText("Nombre de BD nueva o existente...")
        self.btn_refresh_restore.setIcon(qta.icon('fa5s.sync-alt', color='#7D8590'))
        self.btn_refresh_restore.setFixedWidth(42)
        self.btn_refresh_restore.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        db_wrapper = QFrame()
        db_wrapper.setObjectName("inputGroup")
        dw_lay = QHBoxLayout(db_wrapper)
        dw_lay.setContentsMargins(0, 0, 0, 0)
        dw_lay.setSpacing(0)
        dw_lay.addWidget(self.combo_db_restore, 1)
        dw_lay.addWidget(self.btn_refresh_restore)
        
        cl.addLayout(self._field_row('fa5s.database', db_wrapper))

        # — Modalidad —
        cl.addWidget(self._field_label("Modalidad"))
        self.combo_mode_restore.addItems(["Archivo único (.sql)", "Esquema y datos separados"])
        self.combo_mode_restore.currentIndexChanged.connect(self._toggle_restore_mode)
        cl.addLayout(self._field_row('fa5s.tools', self.combo_mode_restore))

        # — Archivo SQL —
        cl.addWidget(self._field_label("Archivo SQL"))
        self.schema_input.setPlaceholderText("Seleccionar archivo .sql...")
        self.btn_select_schema.setText("  Examinar  ")
        self.btn_select_schema.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        sch_wrapper = QFrame()
        sch_wrapper.setObjectName("inputGroup")
        sw_lay = QHBoxLayout(sch_wrapper)
        sw_lay.setContentsMargins(0, 0, 0, 0)
        sw_lay.setSpacing(0)
        sw_lay.addWidget(self.schema_input, 1)
        sw_lay.addWidget(self.btn_select_schema)
        
        cl.addLayout(self._field_row('fa5s.file-code', sch_wrapper))

        # — Datos separados (oculto) —
        self.data_section = QFrame()
        ds = QVBoxLayout(self.data_section)
        ds.setContentsMargins(0, 0, 0, 0); ds.setSpacing(8)
        ds.addWidget(self._field_label("Archivo de datos"))
        
        self.data_input.setPlaceholderText("Seleccionar archivo de datos .sql...")
        self.btn_select_data.setText("  Examinar  ")
        self.btn_select_data.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        dat_wrapper = QFrame()
        dat_wrapper.setObjectName("inputGroup")
        dw_lay = QHBoxLayout(dat_wrapper)
        dw_lay.setContentsMargins(0, 0, 0, 0)
        dw_lay.setSpacing(0)
        dw_lay.addWidget(self.data_input, 1)
        dw_lay.addWidget(self.btn_select_data)
        
        ds.addLayout(self._field_row('fa5s.file', dat_wrapper))
        self.data_section.setVisible(False)
        cl.addWidget(self.data_section)

        # Divisor
        cl.addWidget(self._hdiv())

        # — Advertencia —
        warn_frame = QFrame()
        warn_frame.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(210, 153, 34, 0.08);
                border: 1px solid rgba(210, 153, 34, 0.30);
                border-radius: 8px;
            }}
        """)
        wl = QHBoxLayout(warn_frame)
        wl.setContentsMargins(14, 12, 14, 12)
        wl.setSpacing(12)

        warn_icon = QLabel()
        warn_icon.setPixmap(qta.icon('fa5s.exclamation-triangle', color='#D29922').pixmap(20, 20))
        warn_icon.setFixedWidth(20)
        warn_icon.setAlignment(Qt.AlignmentFlag.AlignTop)

        warn_text = QLabel(
            "Esta operación sobreescribirá todos los datos existentes "
            "en la base de datos destino. Esta acción no se puede deshacer."
        )
        warn_text.setFont(QFont("Segoe UI", 11))
        warn_text.setProperty("class", "text-warning")
        warn_text.setWordWrap(True)

        wl.addWidget(warn_icon); wl.addWidget(warn_text, 1)
        cl.addWidget(warn_frame)

        # — Progress —
        self.progress_bar_restore = QProgressBar()
        self.progress_bar_restore.setFixedHeight(4)
        self.progress_bar_restore.setVisible(False)
        cl.addWidget(self.progress_bar_restore)

        # — Botón —
        self.btn_restore = AnimatedButton("Ejecutar Restauración")
        self.btn_restore.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_restore.setProperty("class", "btn-warning-hero")
        cl.addWidget(self.btn_restore)

        center.addWidget(card)
        center.addStretch()
        outer.addStretch()  # Centrado vertical superior
        outer.addLayout(center)
        outer.addStretch()  # Centrado vertical inferior
        return page

    # ══════════════════════════════════════════════════════════════════════════
    # Segmented Control Lógica
    # ══════════════════════════════════════════════════════════════════════════

    def _mode_toggle_bar(self) -> QWidget:
        container = QWidget()
        lay = QHBoxLayout(container)
        lay.setContentsMargins(0, 0, 0, 0)
        
        pill = QFrame()
        pill.setFixedHeight(40)
        pill.setObjectName("modeToggleContainer")
        pill_lay = QHBoxLayout(pill)
        pill_lay.setContentsMargins(4, 4, 4, 4)
        pill_lay.setSpacing(2)

        self.btn_mode_backup = QPushButton("Crear respaldo")
        self.btn_mode_restore = QPushButton("Restaurar")

        for btn in (self.btn_mode_backup, self.btn_mode_restore):
            btn.setFixedHeight(30)
            btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.setCheckable(True)
            pill_lay.addWidget(btn)

        self.btn_mode_backup.setChecked(True)
        self.btn_mode_backup.clicked.connect(lambda: self._switch_mode("backup"))
        self.btn_mode_restore.clicked.connect(lambda: self._switch_mode("restore"))

        self._style_toggle_btns()

        lay.addStretch()
        lay.addWidget(pill)
        lay.addStretch()
        
        return container

    def _switch_mode(self, mode: str):
        if self._active_mode == mode:
            return
        self._active_mode = mode
        idx = 0 if mode == "backup" else 1
        self.stack.setCurrentIndex(idx)
        
        self.btn_mode_backup.setChecked(mode == "backup")
        self.btn_mode_restore.setChecked(mode == "restore")
        self._style_toggle_btns()

    def _style_toggle_btns(self):
        self.btn_mode_backup.setProperty("transferMode", "active" if self._active_mode == "backup" else "inactive")
        self.btn_mode_restore.setProperty("transferMode", "active" if self._active_mode == "restore" else "inactive")
        
        for btn in (self.btn_mode_backup, self.btn_mode_restore):
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ══════════════════════════════════════════════════════════════════════════
    # Panel lateral — Registro / Log
    # ══════════════════════════════════════════════════════════════════════════

    def _create_log_panel(self) -> QWidget:
        page = QWidget()
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

        term_title = QLabel("Salida del proceso")
        term_title.setFont(QFont("Segoe UI", 11))
        term_title.setProperty("class", "text-muted")
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

    def _field_label(self, text: str) -> QLabel:
        """Label moderno: más pequeño que el input, color suave."""
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        lbl.setProperty("class", "form-label")
        return lbl

    def _hdiv(self) -> QFrame:
        """Separador horizontal usando token SEPARATOR."""
        d = QFrame()
        d.setFixedHeight(1)
        d.setProperty("class", "form-divider")
        return d

    def _field_row(self, icon_name: str, widget: QWidget) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)
        
        icon_lbl = QLabel()
        pm = qta.icon(icon_name, color='#7D8590').pixmap(18, 18)
        icon_lbl.setPixmap(pm)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFixedWidth(24)
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        
        row.addWidget(icon_lbl)
        row.addWidget(widget, 1)
        return row

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