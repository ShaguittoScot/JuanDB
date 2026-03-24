from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QPushButton, QLineEdit, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QCursor, QPalette, QColor, QIcon
import os

from ui.components.animated_button import AnimatedButton
from ui.components.file_selector import FileSelector


class ImportExportView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 700)
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

        # Header mejorado
        header_layout = QHBoxLayout()
        
        tag_container = QVBoxLayout()
        tag = QLabel("<img src='assets/icons/package.svg' width='14' height='14'> TRANSFERENCIA DE DATOS")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 8, QFont.Weight.Bold))
        
        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(60, 3)
        
        tag_container.addWidget(tag)
        tag_container.addWidget(accent_line)
        
        title = QLabel("Importar / Exportar Datos")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setProperty("class", "view-title")
        
        header_layout.addLayout(tag_container)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Descripción mejorada
        desc = QLabel("Transfiere información entre tus tablas y archivos locales de forma segura y eficiente.\n"
                     "Soporta formatos CSV y JSON con validación automática de estructura de datos.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Segoe UI", 11))
        desc.setWordWrap(True)
        card_layout.addWidget(desc)
        
        card_layout.addSpacing(16)

        # Contenedor de columnas con mejor espaciado
        columns_container = QFrame()
        columns_container.setProperty("class", "view-container")
        columns_layout = QHBoxLayout(columns_container)
        columns_layout.setContentsMargins(20, 20, 20, 20)
        columns_layout.setSpacing(32)
        
        # Columnas mejoradas
        col_exp = self._build_export_column()
        col_imp = self._build_import_column()
        
        # Separador vertical elegante
        vdiv = QFrame()
        vdiv.setFixedWidth(2)
        vdiv.setProperty("class", "v-gradient-divider")
        
        columns_layout.addLayout(col_exp, 1)
        columns_layout.addWidget(vdiv)
        columns_layout.addLayout(col_imp, 1)
        
        card_layout.addWidget(columns_container)
        card_layout.addStretch()

        layout.addWidget(card)
        layout.addStretch()

    def _build_export_column(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Header con ícono
        header_layout = QHBoxLayout()
        icon = QLabel("<img src='assets/icons/upload.svg' width='24' height='24'>")
        icon.setFont(QFont("Segoe UI", 24))
        title = QLabel("Exportar Datos")
        title.setProperty("class", "section-title")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setProperty("class", "view-subtitle-accent")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Descripción de la sección
        desc = QLabel("Exporta datos de tus tablas a archivos locales en formato CSV o JSON.")
        desc.setWordWrap(True)
        desc.setProperty("class", "desc-muted")
        layout.addWidget(desc)
        
        layout.addSpacing(8)
        
        # Campos de formulario
        self._add_form_field(layout, "<img src='assets/icons/database.svg' width='14' height='14'> Base de Datos Origen:", self._create_combo(), "db_exp")
        self._add_form_field(layout, "<img src='assets/icons/clipboard.svg' width='14' height='14'> Tabla a Exportar:", self._create_combo(), "table_exp")
        self._add_form_field(layout, "<img src='assets/icons/file.svg' width='14' height='14'> Formato:", self._create_combo(["CSV", "JSON"]), "format_exp")
        
        # Selector de ruta
        path_label = QLabel("<img src='assets/icons/save.svg' width='14' height='14'> Dónde guardar:")
        path_label.setProperty("class", "label")
        layout.addWidget(path_label)
        
        self.file_selector_exp = FileSelector("Seleccionar carpeta de destino...", mode="directory")
        layout.addWidget(self.file_selector_exp)
        
        layout.addSpacing(8)
        
        # Mensaje de estado
        self.lbl_msg_exp = QLabel("")
        self.lbl_msg_exp.setProperty("class", "status-message")
        self.lbl_msg_exp.setWordWrap(True)
        self.lbl_msg_exp.hide()
        layout.addWidget(self.lbl_msg_exp)
        
        # Botón de acción
        self.btn_export = AnimatedButton("Exportar Datos")
        self.btn_export.setIcon(QIcon("assets/icons/upload.svg"))
        self.btn_export.setProperty("class", "btn-primary")
        self.btn_export.setMinimumHeight(44)
        layout.addWidget(self.btn_export)
        
        # Información adicional
        info = QLabel("<img src='assets/icons/info.svg' width='14' height='14'> Los archivos se guardarán con nombre: tabla_fecha.formato")
        info.setProperty("class", "text-hint")
        info.setWordWrap(True)
        layout.addWidget(info)
        
        layout.addStretch()
        
        return layout

    def _build_import_column(self) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(16)
        
        # Header con ícono
        header_layout = QHBoxLayout()
        icon = QLabel("<img src='assets/icons/download.svg' width='24' height='24'>")
        icon.setFont(QFont("Segoe UI", 24))
        title = QLabel("Importar Datos")
        title.setProperty("class", "section-title")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setProperty("class", "view-subtitle-muted")
        header_layout.addWidget(icon)
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Descripción de la sección
        desc = QLabel("Importa datos desde archivos CSV o JSON a tus tablas existentes.")
        desc.setWordWrap(True)
        desc.setProperty("class", "desc-muted")
        layout.addWidget(desc)
        
        layout.addSpacing(8)
        
        # Campos de formulario
        self._add_form_field(layout, "<img src='assets/icons/file.svg' width='14' height='14'> Formato Origen:", self._create_combo(["CSV", "JSON"]), "format_imp")
        
        # Selector de archivo
        file_label = QLabel("<img src='assets/icons/folder.svg' width='14' height='14'> Archivo Local:")
        file_label.setProperty("class", "label")
        layout.addWidget(file_label)
        
        self.file_selector_imp = FileSelector("Seleccionar archivo CSV o JSON...", mode="file")
        layout.addWidget(self.file_selector_imp)
        
        self._add_form_field(layout, "<img src='assets/icons/database.svg' width='14' height='14'> Base de Datos Destino:", self._create_combo(), "db_imp")
        self._add_form_field(layout, "<img src='assets/icons/clipboard.svg' width='14' height='14'> Tabla Destino:", self._create_combo(), "table_imp")
        
        layout.addSpacing(8)
        
        # Opciones adicionales
        options_frame = QFrame()
        options_frame.setProperty("class", "options-frame")
        options_layout = QVBoxLayout(options_frame)
        
        self.chk_overwrite = QPushButton("Sobrescribir si existe")
        self.chk_overwrite.setIcon(QIcon("assets/icons/refresh.svg"))
        self.chk_overwrite.setCheckable(True)
        
        options_layout.addWidget(self.chk_overwrite)
        
        layout.addWidget(options_frame)
        
        # Mensaje de estado
        self.lbl_msg_imp = QLabel("")
        self.lbl_msg_imp.setProperty("class", "status-message")
        self.lbl_msg_imp.setWordWrap(True)
        self.lbl_msg_imp.hide()
        layout.addWidget(self.lbl_msg_imp)
        
        # Botón de acción
        self.btn_import = AnimatedButton("Importar Datos")
        self.btn_import.setIcon(QIcon("assets/icons/download.svg"))
        self.btn_import.setProperty("class", "btn-secondary-animated")
        self.btn_import.setMinimumHeight(44)
        layout.addWidget(self.btn_import)
        
        # Advertencia
        warning = QLabel("<img src='assets/icons/warning.svg' width='14' height='14'> Importante: Las columnas del archivo deben coincidir con la estructura de la tabla destino.")
        warning.setProperty("class", "warning-box")
        warning.setWordWrap(True)
        layout.addWidget(warning)
        
        layout.addStretch()
        
        return layout

    def _add_form_field(self, layout, label_text, widget, widget_name):
        """Agrega un campo de formulario con su etiqueta"""
        label = QLabel(label_text)
        label.setProperty("class", "label")
        layout.addWidget(label)
        layout.addWidget(widget)
        setattr(self, widget_name, widget)

    def _create_combo(self, items=None) -> QComboBox:
        combo = QComboBox()
        combo.setMinimumHeight(38)
        if items:
            combo.addItems(items)
        
        return combo
        
    def show_message(self, section, message, msg_type="info"):
        """Muestra mensajes de estado con diferentes estilos"""
        if section == "export":
            label = self.lbl_msg_exp
        else:
            label = self.lbl_msg_imp
            
        label.setText(message)
        label.setProperty("status", msg_type)
        label.style().polish(label)
        label.show()
        
        # Auto-ocultar después de 5 segundos si es éxito o info
        if msg_type != "error":
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(5000, lambda: label.hide())
    
    def clear_messages(self):
        """Limpia todos los mensajes de estado"""
        self.lbl_msg_exp.hide()
        self.lbl_msg_imp.hide()
        self.lbl_msg_exp.setText("")
        self.lbl_msg_imp.setText("")