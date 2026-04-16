"""
BackupFormCard — Tarjeta de formulario para crear copias de seguridad.

Componente modular que encapsula todo el formulario de "Crear respaldo",
aplicando las Reglas de Oro de diseño del proyecto JuanDB.
Usa exclusivamente tokens de ui.colors (DARK_THEME / LIGHT_THEME).
"""

from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QComboBox, QLineEdit, QPushButton, QProgressBar,
    QCheckBox, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
import qtawesome as qta

from ui.components.animated_button import AnimatedButton
from ui.colors import DARK_THEME as APP_COLORS


class BackupFormCard(QFrame):
    """
    Form Card centrada con max-width 850px que contiene:
      • Selector de base de datos + refresh
      • Directorio de destino con botón "Examinar" integrado
      • Nombre de archivo (opcional)
      • Checkboxes horizontales personalizados
      • Barra de progreso
      • Stats (último backup, conteo)
      • Botón principal "Crear copia de seguridad"
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("formCard")
        self.setFixedWidth(600)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        
        self.setStyleSheet(f"""
            QFrame#formCard {{
                background-color: {APP_COLORS['BG_CARD']};
                border-radius: 12px;
                border: 1px solid {APP_COLORS['BORDER']};
            }}
        """)

        self._build()

    # ══════════════════════════════════════════════════════════════════════════
    # Construcción
    # ══════════════════════════════════════════════════════════════════════════

    def _build(self):
        main = QVBoxLayout(self)
        main.setContentsMargins(32, 32, 32, 32)
        main.setSpacing(18)
        
        title = QLabel("Crear Copia de Seguridad")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {APP_COLORS['TEXT_LIGHT']}; border: none;")
        main.addWidget(title)
        
        main.addSpacing(8)

        # ── Base de datos ────────────────────────────────────────────────
        main.addWidget(self._field_label("Base de datos"))

        self.combo_db = QComboBox()
        self.combo_db.setPlaceholderText("Seleccionar base de datos...")

        self.btn_refresh = QPushButton("↺")
        self.btn_refresh.setObjectName("inputGroupBtn")
        self.btn_refresh.setFixedWidth(42)
        self.btn_refresh.setToolTip("Actualizar lista")
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        db_group = self._input_group(self.combo_db, self.btn_refresh)
        main.addLayout(self._field_row('fa5s.database', db_group))

        # ── Directorio de destino ────────────────────────────────────────
        main.addWidget(self._field_label("Directorio de destino"))

        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Ej.  C:/backups/mysql")

        self.btn_select_dir = QPushButton("  Examinar  ")
        self.btn_select_dir.setObjectName("inputGroupBtn")
        self.btn_select_dir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        dir_group = self._input_group(self.path_input, self.btn_select_dir)
        main.addLayout(self._field_row('fa5s.folder-open', dir_group))

        # ── Nombre del archivo (opcional) ────────────────────────────────
        main.addWidget(self._field_label("Nombre del archivo  ·  opcional"))

        self.custom_name = QLineEdit()
        self.custom_name.setPlaceholderText("Se genera automáticamente si se deja vacío")
        main.addLayout(self._field_row('fa5s.file', self.custom_name))

        # ── Divisor ─────────────────────────────────────────────────────
        main.addWidget(self._hdiv())

        # ── Opciones (checkboxes horizontales) ──────────────────────────
        main.addWidget(self._field_label("Opciones"))

        opts_row = QHBoxLayout()
        opts_row.setSpacing(28)

        self.chk_compress = QCheckBox("Comprimir (.zip)")
        self.chk_compress.setChecked(True)
        self.chk_drop_tables = QCheckBox("DROP TABLE IF EXISTS")
        self.chk_create_db = QCheckBox("CREATE DATABASE")

        for chk in (self.chk_compress, self.chk_drop_tables, self.chk_create_db):
            chk.setFont(QFont("Segoe UI", 12))
            chk.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            opts_row.addWidget(chk)

        opts_row.addStretch()
        main.addLayout(opts_row)

        # ── Progress bar ────────────────────────────────────────────────
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setVisible(False)
        main.addWidget(self.progress_bar)

        # ── Stats ───────────────────────────────────────────────────────
        stats_row = QHBoxLayout()
        self.stats_last_backup = QLabel("Último backup: —")
        self.stats_backup_count = QLabel("Realizados: 0")
        for lbl in (self.stats_last_backup, self.stats_backup_count):
            lbl.setFont(QFont("Segoe UI", 11))
            lbl.setProperty("class", "text-hint")
        stats_row.addWidget(self.stats_last_backup)
        stats_row.addStretch()
        stats_row.addWidget(self.stats_backup_count)
        main.addLayout(stats_row)

        # ── Botones ─────────────────────────────────────────────────────
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setProperty("class", "btn-secondary-animated")
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setFixedHeight(44)
        self.btn_cancel.setFont(QFont("Segoe UI", 13, QFont.Weight.Medium))
        self.btn_cancel.setVisible(False)

        self.btn_backup = AnimatedButton("Crear copia de seguridad")
        self.btn_backup.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        self.btn_backup.setFixedHeight(44)
        self.btn_backup.setStyleSheet(f"""
            QPushButton {{
                background-color: {APP_COLORS['ACCENT']};
                color: #FFFFFF;
                border-radius: 6px;
                padding: 10px 0;
            }}
            QPushButton:hover {{ background-color: {APP_COLORS['ACCENT_DARK']}; }}
        """)

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_backup, 1)
        main.addLayout(btn_row)

    # ══════════════════════════════════════════════════════════════════════════
    # Helpers internos
    # ══════════════════════════════════════════════════════════════════════════

    def _field_label(self, text: str) -> QLabel:
        """Label moderno: 20% más pequeño, color TEXT_MUTED."""
        lbl = QLabel(text)
        lbl.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        lbl.setProperty("class", "form-label")
        return lbl

    def _input_group(self, input_widget: QWidget, button: QPushButton) -> QFrame:
        """
        Fusiona un input y un botón dentro de un solo bloque visual.
        El frame actúa como wrapper con borde compartido.
        """
        group = QFrame()
        group.setObjectName("inputGroup")
        lay = QHBoxLayout(group)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        lay.addWidget(input_widget, 1)
        lay.addWidget(button)
        return group

    def _hdiv(self) -> QFrame:
        """Separador horizontal usando token SEPARATOR."""
        d = QFrame()
        d.setFixedHeight(1)
        d.setStyleSheet(f"background-color: {APP_COLORS['SEPARATOR']}; border: none;")
        return d

    def _field_row(self, icon_name: str, widget: QWidget) -> QHBoxLayout:
        row = QHBoxLayout()
        row.setSpacing(12)
        
        icon_lbl = QLabel()
        pm = qta.icon(icon_name, color=APP_COLORS['TEXT_MUTED']).pixmap(18, 18)
        icon_lbl.setPixmap(pm)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFixedWidth(24)
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        
        row.addWidget(icon_lbl)
        row.addWidget(widget, 1)
        return row
