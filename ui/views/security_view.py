from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QPushButton, QAbstractItemView, QMessageBox, QCheckBox,
    QComboBox, QGroupBox, QSpacerItem
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QCursor, QColor, QPalette, QIcon
import re

from ui.components.animated_button import AnimatedButton
from ui.components.password_indicator import PasswordStrengthIndicator


class SecurityView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1200, 750)
        self._build_ui()
        self._setup_connections()
        

    def _setup_connections(self):
        """Configura las conexiones de señales"""
        self.btn_refresh.clicked.connect(self._on_refresh_clicked)
        self.btn_delete.clicked.connect(self._on_delete_clicked)
        self.btn_create.clicked.connect(self._on_create_clicked)
        self.table.itemSelectionChanged.connect(self._on_table_select)
        self.txt_pass.textChanged.connect(self._on_password_changed)
        
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
        tag = QLabel("<img src='assets/icons/lock.svg' width='14' height='14'> CONTROL DE ACCESO")
        tag.setObjectName("cardTag")
        tag.setFont(QFont("Courier New", 8, QFont.Weight.Bold))
        
        accent_line = QFrame()
        accent_line.setObjectName("accentLine")
        accent_line.setFixedSize(60, 3)
        
        tag_container.addWidget(tag)
        tag_container.addWidget(accent_line)
        
        title = QLabel("Seguridad y Permisos")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setProperty("class", "view-title")
        
        header_layout.addLayout(tag_container)
        header_layout.addStretch()
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        card_layout.addLayout(header_layout)
        
        # Descripción mejorada
        desc = QLabel("Administra las cuentas de usuario de la base de datos con control granular de permisos.\n"
                     "Puedes crear nuevos usuarios, modificar privilegios y revocar accesos de forma segura.")
        desc.setObjectName("cardDesc")
        desc.setFont(QFont("Segoe UI", 11))
        desc.setWordWrap(True)
        card_layout.addWidget(desc)
        
        card_layout.addSpacing(16)

        # Split principal
        split_layout = QHBoxLayout()
        split_layout.setSpacing(32)
        
        # Lado izquierdo - Tabla de usuarios
        left_container = QFrame()
        left_container.setProperty("class", "view-container")
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(16)
        
        # Header de tabla
        table_header = QHBoxLayout()
        table_icon = QLabel("<img src='assets/icons/users.svg' width='16' height='16'>")
        table_icon.setProperty("class", "icon-20")
        table_title = QLabel("Usuarios Registrados")
        table_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        table_title.setProperty("class", "view-subtitle-accent")
        
        table_header.addWidget(table_icon)
        table_header.addWidget(table_title)
        table_header.addStretch()
        
        # Contador de usuarios
        self.user_count_label = QLabel("0 usuarios")
        self.user_count_label.setProperty("class", "text-muted-11")
        table_header.addWidget(self.user_count_label)
        
        left_layout.addLayout(table_header)
        
        # Tabla mejorada
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Usuario", "Host", "Privilegios"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumHeight(300)
        
        left_layout.addWidget(self.table)
        
        # Botones de acción para tabla
        table_buttons = QHBoxLayout()
        table_buttons.setSpacing(12)
        
        self.btn_refresh = QPushButton("Refrescar")
        self.btn_refresh.setIcon(QIcon("assets/icons/refresh.svg"))
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh.setProperty("class", "btn-secondary-animated")
        
        self.btn_delete = QPushButton("Eliminar Seleccionado")
        self.btn_delete.setIcon(QIcon("assets/icons/trash.svg"))
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_delete.setEnabled(False)
        self.btn_delete.setProperty("class", "btn-danger")
        
        self.btn_edit_privileges = QPushButton("Editar Privilegios")
        self.btn_edit_privileges.setIcon(QIcon("assets/icons/wrench.svg"))
        self.btn_edit_privileges.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_edit_privileges.setEnabled(False)
        self.btn_edit_privileges.setProperty("class", "btn-secondary-animated")
        
        table_buttons.addWidget(self.btn_refresh)
        table_buttons.addWidget(self.btn_delete)
        table_buttons.addWidget(self.btn_edit_privileges)
        table_buttons.addStretch()
        
        left_layout.addLayout(table_buttons)
        
        # Lado derecho - Formulario de creación
        right_container = QFrame()
        right_container.setProperty("class", "view-container")
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(24, 24, 24, 24)
        right_layout.setSpacing(20)
        
        # Header del formulario
        form_header = QHBoxLayout()
        form_icon = QLabel("<img src='assets/icons/sparkles.svg' width='16' height='16'>")
        form_icon.setProperty("class", "icon-20")
        form_title = QLabel("Crear Nueva Cuenta")
        form_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        form_title.setProperty("class", "view-subtitle-muted")
        
        form_header.addWidget(form_icon)
        form_header.addWidget(form_title)
        form_header.addStretch()
        
        right_layout.addLayout(form_header)
        
        # Campos del formulario
        # Usuario
        user_label = QLabel("<img src='assets/icons/user.svg' width='14' height='14'> Nombre de Usuario")
        user_label.setProperty("class", "label")
        right_layout.addWidget(user_label)
        
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("ej. usuario_app")
        right_layout.addWidget(self.txt_user)
        
        # Host
        host_label = QLabel("<img src='assets/icons/globe.svg' width='14' height='14'> Host Autorizado")
        host_label.setProperty("class", "label")
        right_layout.addWidget(host_label)
        
        host_layout = QHBoxLayout()
        self.txt_host = QLineEdit()
        self.txt_host.setText("%")
        self.txt_host.setPlaceholderText("localhost, %, o IP específica")
        
        host_presets = QComboBox()
        host_presets.addItems(["Seleccionar preset", "localhost", "% (cualquier host)", "127.0.0.1"])
        host_presets.currentTextChanged.connect(lambda x: self._on_host_preset(x, host_presets))
        
        host_layout.addWidget(self.txt_host, 2)
        host_layout.addWidget(host_presets, 1)
        right_layout.addLayout(host_layout)
        
        # Contraseña
        pass_label = QLabel("<img src='assets/icons/key.svg' width='14' height='14'> Contraseña")
        pass_label.setProperty("class", "label")
        right_layout.addWidget(pass_label)
        
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Contraseña segura")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        right_layout.addWidget(self.txt_pass)
        
        # Indicador de fortaleza
        self.pass_strength = PasswordStrengthIndicator()
        right_layout.addWidget(self.pass_strength)
        
        # Mostrar contraseña
        self.chk_show_pass = QCheckBox("Mostrar contraseña")
        self.chk_show_pass.stateChanged.connect(self._toggle_password_visibility)
        right_layout.addWidget(self.chk_show_pass)
        
        # Confirmar contraseña
        confirm_label = QLabel("<img src='assets/icons/check.svg' width='14' height='14'> Confirmar Contraseña")
        confirm_label.setProperty("class", "label")
        right_layout.addWidget(confirm_label)
        
        self.txt_confirm_pass = QLineEdit()
        self.txt_confirm_pass.setPlaceholderText("Repite la contraseña")
        self.txt_confirm_pass.setEchoMode(QLineEdit.EchoMode.Password)
        right_layout.addWidget(self.txt_confirm_pass)
        
        # Opciones adicionales
        options_group = QGroupBox("Opciones Adicionales")
        options_layout = QVBoxLayout(options_group)
        
        self.chk_grant_priv = QCheckBox("Conceder privilegios administrativos")
        self.chk_expire_pass = QCheckBox("Expirar contraseña en primer inicio")
        
        options_layout.addWidget(self.chk_grant_priv)
        options_layout.addWidget(self.chk_expire_pass)
        right_layout.addWidget(options_group)
        
        # Mensaje de estado
        self.lbl_msg = QLabel("")
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setStyleSheet("""
            QLabel {
                padding: 8px;
                border-radius: 6px;
                background-color: rgba(18, 10, 28, 0.6);
            }
            QLabel[status="success"] {
                color: #4ADE80;
                border-left: 3px solid #4ADE80;
            }
            QLabel[status="error"] {
                color: #FF4444;
                border-left: 3px solid #FF4444;
            }
            QLabel[status="warning"] {
                color: #FFB86C;
                border-left: 3px solid #FFB86C;
            }
        """)
        right_layout.addWidget(self.lbl_msg)
        
        # Botón de creación
        self.btn_create = AnimatedButton("Crear Usuario")
        self.btn_create.setIcon(QIcon("assets/icons/sparkles.svg"))
        self.btn_create.setProperty("class", "btn-primary")
        self.btn_create.setMinimumHeight(44)
        right_layout.addWidget(self.btn_create)
        
        # Información de ayuda
        help_text = QLabel("<img src='assets/icons/info.svg' width='14' height='14'> Los usuarios creados tendrán acceso básico. "
                          "Puedes modificar sus privilegios después de la creación.")
        help_text.setWordWrap(True)
        help_text.setProperty("class", "text-hint")
        right_layout.addWidget(help_text)
        
        right_layout.addStretch()
        
        # Agregar ambos lados al split
        split_layout.addWidget(left_container, 2)
        split_layout.addWidget(right_container, 1)
        
        card_layout.addLayout(split_layout)
        card_layout.addStretch()

        layout.addWidget(card)
        layout.addStretch()
        
        # Datos de ejemplo
        self._load_sample_data()
        
    def _load_sample_data(self):
        """Carga datos de ejemplo para la tabla"""
        sample_users = [
            ("admin", "localhost", "Todos los privilegios"),
            ("app_user", "%", "SELECT, INSERT, UPDATE"),
            ("readonly", "192.168.1.%", "SELECT"),
        ]
        
        self.table.setRowCount(len(sample_users))
        for row, (user, host, privileges) in enumerate(sample_users):
            self.table.setItem(row, 0, QTableWidgetItem(user))
            self.table.setItem(row, 1, QTableWidgetItem(host))
            self.table.setItem(row, 2, QTableWidgetItem(privileges))
            
        self.user_count_label.setText(f"{len(sample_users)} usuarios")
        
    def _on_host_preset(self, preset, combo):
        """Maneja la selección de preset de host"""
        if preset != "Seleccionar preset":
            self.txt_host.setText(preset)
            combo.setCurrentIndex(0)
            
    def _toggle_password_visibility(self, state):
        """Muestra/oculta la contraseña"""
        echo_mode = QLineEdit.EchoMode.Normal if state else QLineEdit.EchoMode.Password
        self.txt_pass.setEchoMode(echo_mode)
        self.txt_confirm_pass.setEchoMode(echo_mode)
        
    def _on_password_changed(self, text):
        """Evalúa la fortaleza de la contraseña"""
        self.pass_strength.check_strength(text)
        
    def _on_table_select(self):
        """Maneja la selección en la tabla"""
        items = self.table.selectedItems()
        has_selection = len(items) > 0
        self.btn_delete.setEnabled(has_selection)
        self.btn_edit_privileges.setEnabled(has_selection)
        
    def _on_refresh_clicked(self):
        """Refresca la lista de usuarios"""
        self.show_message("Refrescando lista de usuarios...", "info")
        # Aquí iría la lógica para recargar usuarios
        # Simular carga
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self.show_message("Lista de usuarios actualizada", "success"))
        
    def _on_delete_clicked(self):
        """Elimina el usuario seleccionado"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            user = self.table.item(current_row, 0).text()
            host = self.table.item(current_row, 1).text()
            
            reply = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                f"¿Estás seguro de eliminar al usuario '{user}'@{host}?\n\n"
                "Esta acción no se puede deshacer.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.table.removeRow(current_row)
                self.user_count_label.setText(f"{self.table.rowCount()} usuarios")
                self.show_message(f"Usuario '{user}'@{host} eliminado correctamente", "success")
                
    def _on_create_clicked(self):
        """Crea un nuevo usuario"""
        user = self.txt_user.text().strip()
        host = self.txt_host.text().strip()
        password = self.txt_pass.text()
        confirm = self.txt_confirm_pass.text()
        
        # Validaciones
        if not user:
            self.show_message("<img src='assets/icons/cross.svg' width='14' height='14'> El nombre de usuario es obligatorio", "error")
            return
            
        if not host:
            self.show_message("<img src='assets/icons/cross.svg' width='14' height='14'> El host es obligatorio", "error")
            return
            
        if not password:
            self.show_message("<img src='assets/icons/cross.svg' width='14' height='14'> La contraseña es obligatoria", "error")
            return
            
        if password != confirm:
            self.show_message("<img src='assets/icons/cross.svg' width='14' height='14'> Las contraseñas no coinciden", "error")
            return
            
        if len(password) < 6:
            self.show_message("<img src='assets/icons/warning.svg' width='14' height='14'> La contraseña debe tener al menos 6 caracteres", "warning")
            return
            
        # Verificar si el usuario ya existe
        for row in range(self.table.rowCount()):
            existing_user = self.table.item(row, 0).text()
            existing_host = self.table.item(row, 1).text()
            if existing_user == user and existing_host == host:
                self.show_message(f"<img src='assets/icons/cross.svg' width='14' height='14'> El usuario '{user}'@{host} ya existe", "error")
                return
                
        # Agregar usuario
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(user))
        self.table.setItem(row, 1, QTableWidgetItem(host))
        
        privileges = "Privilegios básicos"
        if self.chk_grant_priv.isChecked():
            privileges = "Privilegios administrativos"
            
        self.table.setItem(row, 2, QTableWidgetItem(privileges))
        
        self.user_count_label.setText(f"{self.table.rowCount()} usuarios")
        
        # Limpiar formulario
        self.txt_user.clear()
        self.txt_pass.clear()
        self.txt_confirm_pass.clear()
        self.chk_grant_priv.setChecked(False)
        self.chk_expire_pass.setChecked(False)
        
        self.show_message(f"<img src='assets/icons/check.svg' width='14' height='14'> Usuario '{user}'@{host} creado exitosamente", "success")
        
    def show_message(self, msg, msg_type="info"):
        """Muestra mensajes de estado"""
        self.lbl_msg.setText(msg)
        self.lbl_msg.setProperty("status", msg_type)
        self.lbl_msg.style().polish(self.lbl_msg)
        
        # Auto-ocultar después de 5 segundos si es éxito o info
        if msg_type != "error":
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(5000, lambda: self.lbl_msg.setText(""))