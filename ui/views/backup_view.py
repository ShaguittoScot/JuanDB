from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QLineEdit, QTextEdit, QProgressBar,
    QCheckBox, QGroupBox, QSpacerItem, QStackedWidget
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
from PyQt6.QtGui import QFont, QCursor, QTextCursor, QColor, QTextCharFormat, QIcon
from datetime import datetime
import os

from ui.components.animated_button import AnimatedButton
from ui.components.log_text_edit import LogTextEdit


class BackupView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 750)
        self._build_ui()
        self._setup_connections()
        

    def _setup_connections(self):
        """Configura las conexiones de señales"""
        self.btn_refresh.clicked.connect(self._on_refresh_clicked)
        self.btn_select_dir.clicked.connect(self._on_select_directory)
        self.btn_backup.clicked.connect(self._on_backup_clicked)
        
    def _build_ui(self):
        # Inicializar componentes obligatorios
        self.combo_db = QComboBox()
        self.path_input = QLineEdit()
        self.btn_refresh = QPushButton()
        self.btn_select_dir = QPushButton()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Tarjeta principal
        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 32, 40, 32)
        card_layout.setSpacing(20)

        # Header mejorado
        header_layout = QHBoxLayout()
        
        tag_container = QVBoxLayout()
        tag = QLabel("<img src='assets/icons/save.svg' width='14' height='14'> RESPALDO DE DATOS")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 8, QFont.Weight.Bold))
        
        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(60, 3)
        
        tag_container.addWidget(tag)
        tag_container.addWidget(accent_line)
        
        title = QLabel("Copias de Seguridad")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setProperty("class", "view-title")
        
        header_layout.addLayout(tag_container)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)

        # Contenedor de columnas con mejor espaciado
        columns_container = QFrame()
        columns_container.setProperty("class", "view-container")
        columns_layout = QHBoxLayout(columns_container)
        columns_layout.setContentsMargins(20, 20, 20, 20)
        columns_layout.setSpacing(32)
        
        col_backup = self._build_backup_column()
        col_restore = self._build_restore_column()
        
        # Separador vertical elegante
        vdiv = QFrame()
        vdiv.setFixedWidth(2)
        vdiv.setProperty("class", "v-gradient-divider")
        
        columns_layout.addLayout(col_backup, 1)
        columns_layout.addWidget(vdiv)
        columns_layout.addLayout(col_restore, 1)
        
        card_layout.addWidget(columns_container)
        
        # Sección de estadísticas
        stats_container = QFrame()
        stats_container.setProperty("class", "view-container-small")
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setContentsMargins(16, 12, 16, 12)
        
        self.stats_last_backup = QLabel("Último backup: --")
        self.stats_last_backup.setProperty("class", "text-muted-11")
        self.stats_backup_count = QLabel("Backups realizados: 0")
        self.stats_backup_count.setProperty("class", "text-muted-11")
        
        stats_layout.addWidget(self.stats_last_backup)
        stats_layout.addStretch()
        stats_layout.addWidget(self.stats_backup_count)
        
        card_layout.addWidget(stats_container)
        
        # Consola/Log mejorada
        log_header = QHBoxLayout()
        log_icon = QLabel("<img src='assets/icons/clipboard.svg' width='16' height='16'>")
        log_icon.setProperty("class", "icon-14")
        log_title = QLabel("Registro del proceso")
        log_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        log_title.setProperty("class", "view-subtitle-accent")
        
        clear_btn = QPushButton("Limpiar")
        clear_btn.setObjectName("btnSecondary")
        clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        clear_btn.clicked.connect(self.clear_log)
        
        log_header.addWidget(log_icon)
        log_header.addWidget(log_title)
        log_header.addStretch()
        log_header.addWidget(clear_btn)
        
        card_layout.addLayout(log_header)
        
        self.log_area = LogTextEdit()
        self.log_area.setObjectName("logArea")
        self.log_area.setMinimumHeight(180)
        
        card_layout.addWidget(self.log_area)

        layout.addWidget(card)
        layout.addStretch()
        
    def _build_backup_column(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Header con ícono
        header_layout = QHBoxLayout()
        icon = QLabel("<img src='assets/icons/upload.svg' width='24' height='24'>")
        icon.setFont(QFont("Segoe UI", 24))
        title = QLabel("Crear Copia")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setProperty("class", "view-subtitle-accent")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        desc = QLabel("Genera un respaldo completo de la base de datos seleccionada.")
        desc.setWordWrap(True)
        desc.setProperty("class", "desc-muted")
        layout.addWidget(desc)
        layout.addSpacing(8)

        # Fila 1: Seleccionar base de datos
        db_widget = self._create_form_row(
            "<img src='assets/icons/database.svg' width='14' height='14'> Base de Datos:",
            self.combo_db,
            self.btn_refresh,
            "Actualizar"
        )
        self.btn_refresh.setIcon(QIcon("assets/icons/refresh.svg"))
        layout.addLayout(db_widget)
        
        # Fila 2: Seleccionar directorio
        dir_widget = self._create_form_row(
            "<img src='assets/icons/folder.svg' width='14' height='14'> Destino:",
            self.path_input,
            self.btn_select_dir,
            "Examinar..."
        )
        self.btn_select_dir.setIcon(QIcon("assets/icons/folder.svg"))
        layout.addLayout(dir_widget)
        
        # Opciones avanzadas
        advanced_group = QGroupBox("Opciones Avanzadas")
        advanced_layout = QVBoxLayout(advanced_group)
        
        options_layout = QHBoxLayout()
        self.chk_compress = QCheckBox("Comprimir backup (.zip)")
        self.chk_compress.setChecked(True)
        self.chk_drop_tables = QCheckBox("DROP TABLE IF EXISTS")
        self.chk_create_db = QCheckBox("CREATE DATABASE")
        
        options_layout.addWidget(self.chk_compress)
        options_layout.addWidget(self.chk_drop_tables)
        options_layout.addWidget(self.chk_create_db)
        options_layout.addStretch()
        
        advanced_layout.addLayout(options_layout)
        
        name_layout = QHBoxLayout()
        name_label = QLabel("Nombre personalizado (opcional):")
        name_label.setProperty("class", "text-adaptive")
        self.custom_name = QLineEdit()
        self.custom_name.setPlaceholderText("dejar vacío para nombre automático")
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.custom_name, 1)
        advanced_layout.addLayout(name_layout)
        
        layout.addWidget(advanced_group)
        
        # Barra de progreso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMinimumHeight(30)
        layout.addWidget(self.progress_bar)
        
        # Fila 3: Botón de respaldo principal
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self.btn_backup = AnimatedButton("Crear Copia")
        self.btn_backup.setIcon(QIcon("assets/icons/save.svg"))
        self.btn_backup.setProperty("class", "btn-primary")
        self.btn_backup.setMinimumWidth(200)
        
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setObjectName("btnSecondary")
        self.btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_cancel.setVisible(False)
        self.btn_cancel.clicked.connect(self._on_cancel_backup)
        
        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_backup)
        btn_row.addStretch()
        
        layout.addLayout(btn_row)
        layout.addStretch()
        return layout

    def _build_restore_column(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # inicializar widgets para la restauracion
        self.combo_db_restore = QComboBox()
        self.combo_db_restore.setEditable(True)
        self.combo_db_restore.setPlaceholderText("Seleccionar o escribir nueva BD...")
        self.combo_mode_restore = QComboBox()
        self.schema_input = QLineEdit()
        self.data_input = QLineEdit()
        self.btn_refresh_restore = QPushButton()
        self.btn_select_schema = QPushButton()
        self.btn_select_data = QPushButton()

        # Header con ícono
        header_layout = QHBoxLayout()
        icon = QLabel("<img src='assets/icons/download.svg' width='24' height='24'>")
        icon.setFont(QFont("Segoe UI", 24))
        title = QLabel("Restaurar Copia")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setProperty("class", "view-subtitle-muted")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        desc = QLabel("Restaura la estructura y datos de un archivo .sql a una base de datos.")
        desc.setWordWrap(True)
        desc.setProperty("class", "desc-muted")
        layout.addWidget(desc)
        layout.addSpacing(8)

        # Seleccionar base de datos origen
        db_widget = self._create_form_row(
            "<img src='assets/icons/database.svg' width='14' height='14'> BD Destino:",
            self.combo_db_restore,
            self.btn_refresh_restore,
            "Actualizar"
        )
        self.btn_refresh_restore.setIcon(QIcon("assets/icons/refresh.svg"))
        layout.addLayout(db_widget)

        # Modo de Restauración
        mode_widget = self._create_form_row(
            "<img src='assets/icons/settings.svg' width='14' height='14'> Modalidad:",
            self.combo_mode_restore
        )
        self.combo_mode_restore.addItems(["Archivo Único (.sql)", "Esquema y Datos Divididos"])
        self.combo_mode_restore.currentIndexChanged.connect(self._toggle_restore_mode)
        layout.addLayout(mode_widget)

        # Seleccionar archivo sql / esquema
        self.schema_widget = self._create_form_row(
            "<img src='assets/icons/document.svg' width='14' height='14'> Archivo SQL:",
            self.schema_input,
            self.btn_select_schema,
            "Buscar..."
        )
        self.btn_select_schema.setIcon(QIcon("assets/icons/folder.svg"))
        layout.addLayout(self.schema_widget)
        
        # Seleccionar archivo datos
        self.data_widget_container = QFrame()
        self.data_widget_layout = QVBoxLayout(self.data_widget_container)
        self.data_widget_layout.setContentsMargins(0, 0, 0, 0)
        
        data_row = self._create_form_row(
            "<img src='assets/icons/clipboard.svg' width='14' height='14'> Archivo Datos:",
            self.data_input,
            self.btn_select_data,
            "Buscar..."
        )
        self.btn_select_data.setIcon(QIcon("assets/icons/folder.svg"))
        self.data_widget_layout.addLayout(data_row)
        
        self.data_widget_container.setVisible(False)
        layout.addWidget(self.data_widget_container)
        
        # Advertencia
        warning = QLabel("<img src='assets/icons/warning.svg' width='14' height='14'> ¡Peligro! Restaurar un backup sobreescribirá cualquier dato existente en la base de datos destino y esta acción no se puede deshacer.")
        warning.setProperty("class", "warning-box")
        warning.setWordWrap(True)
        layout.addWidget(warning)
        
        # Barra de progreso para restauracion
        self.progress_bar_restore = QProgressBar()
        self.progress_bar_restore.setVisible(False)
        self.progress_bar_restore.setMinimumHeight(30)
        layout.addWidget(self.progress_bar_restore)

        # Botón de restaurar
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        self.btn_restore = AnimatedButton("Restaurar Backup")
        self.btn_restore.setIcon(QIcon("assets/icons/download.svg"))
        self.btn_restore.setProperty("class", "btn-secondary-animated")
        self.btn_restore.setMinimumWidth(200)
        
        btn_row.addWidget(self.btn_restore)
        btn_row.addStretch()
        
        layout.addLayout(btn_row)
        layout.addStretch()
        return layout
        
    def _toggle_restore_mode(self, index: int):
        """Muestra u oculta la selección de datos separados basado en la modalidad"""
        if index == 1:
            self.data_widget_container.setVisible(True)
            self.schema_input.setPlaceholderText("Ej. sakila-schema.sql")
            self.data_input.setPlaceholderText("Ej. sakila-data.sql")
        else:
            self.data_widget_container.setVisible(False)
            self.schema_input.setPlaceholderText("Buscar...")
            self.data_input.clear()
        

        
    def _create_form_row(self, label_text, widget, button_widget=None, button_text=None):
        """Crea una fila de formulario consistente"""
        layout = QHBoxLayout()
        layout.setSpacing(12)
        
        label = QLabel(label_text)
        label.setProperty("class", "label")
        label.setMinimumWidth(100)
        
        layout.addWidget(label)
        
        if isinstance(widget, QComboBox) or isinstance(widget, QLineEdit):
            layout.addWidget(widget, 1)
        
        if button_widget and button_text:
            button_widget.setText(button_text)
            button_widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            button_widget.setProperty("class", "btn-secondary-animated")
            layout.addWidget(button_widget)
        
        return layout
        
    def _on_refresh_clicked(self):
        """Maneja el clic en actualizar bases de datos"""
        self.log_area.append_log("Actualizando lista de bases de datos...", "process")
        # Aquí iría la lógica para cargar bases de datos
        QTimer.singleShot(1000, lambda: self.log_area.append_log("Bases de datos actualizadas", "success"))
        
    def _on_select_directory(self):
        """Maneja la selección de directorio"""
        from PyQt6.QtWidgets import QFileDialog
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio de Backup")
        if directory:
            self.path_input.setText(directory)
            self.log_area.append_log(f"Directorio seleccionado: {directory}", "info")
            
    def _on_backup_clicked(self):
        """Maneja el inicio del backup"""
        if not self.path_input.text():
            self.log_area.append_log("Por favor selecciona un directorio de destino", "error")
            return
            
        if self.combo_db.currentText() == "":
            self.log_area.append_log("Por favor selecciona una base de datos", "error")
            return
            
        # Mostrar barra de progreso
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.btn_backup.setEnabled(False)
        self.btn_cancel.setVisible(True)
        
        # Simular progreso (reemplazar con lógica real)
        self.log_area.append_log(f"Iniciando backup de {self.combo_db.currentText()}...", "process")
        
        # Aquí iría la lógica real de backup
        QTimer.singleShot(3000, self._simulate_backup_complete)
        
    def _simulate_backup_complete(self):
        """Simula la finalización del backup"""
        self.progress_bar.setValue(100)
        self.log_area.append_log(f"Backup completado exitosamente en {self.path_input.text()}", "success")
        
        # Actualizar estadísticas
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats_last_backup.setText(f"Último backup: {now}")
        current_count = int(self.stats_backup_count.text().split(": ")[1])
        self.stats_backup_count.setText(f"Backups realizados: {current_count + 1}")
        
        # Resetear UI
        QTimer.singleShot(1000, self._reset_backup_ui)
        
    def _reset_backup_ui(self):
        """Reinicia la UI después del backup"""
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)
        self.btn_backup.setEnabled(True)
        self.btn_cancel.setVisible(False)
        
    def _on_cancel_backup(self):
        """Cancela el proceso de backup"""
        self.log_area.append_log("Backup cancelado por el usuario", "warning")
        self._reset_backup_ui()
        
    def log_message(self, msg: str, msg_type="info"):
        """Método de compatibilidad con la versión anterior"""
        self.log_area.append_log(msg, msg_type)
        
    def clear_log(self):
        """Limpia el área de log"""
        self.log_area.clear()
        self.log_area.append_log("Registro limpiado", "info")
        
    def set_backup_progress(self, value: int):
        """Actualiza la barra de progreso"""
        self.progress_bar.setValue(value)
        
    def update_database_list(self, databases: list):
        """Actualiza la lista de bases de datos"""
        self.combo_db.clear()
        self.combo_db.addItems(databases)