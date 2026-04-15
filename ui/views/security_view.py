from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
    QPushButton, QAbstractItemView, QMessageBox, QCheckBox, QComboBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor

from ui.components.animated_button import AnimatedButton
from ui.components.password_indicator import PasswordStrengthIndicator


class SecurityView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 580)
        self._build_ui()
        self._setup_connections()

    # ── Señales ───────────────────────────────────────────────────────────────

    def _setup_connections(self):
        self.btn_refresh.clicked.connect(self._on_refresh_clicked)
        self.btn_delete.clicked.connect(self._on_delete_clicked)
        self.btn_edit.clicked.connect(self._on_edit_clicked)
        self.btn_create.clicked.connect(self._on_create_clicked)
        self.table.itemSelectionChanged.connect(self._on_table_select)
        self.txt_pass.textChanged.connect(self._on_password_changed)

    # ── Construcción ──────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._page_header())

        body = QFrame()
        bl = QHBoxLayout(body)
        bl.setContentsMargins(24, 20, 24, 24)
        bl.setSpacing(16)
        bl.addWidget(self._users_card(), 3)
        bl.addWidget(self._form_card(), 2)

        root.addWidget(body, 1)

    # ── Page header ───────────────────────────────────────────────────────────

    def _page_header(self) -> QFrame:
        h = QFrame()
        l = QVBoxLayout(h)
        l.setContentsMargins(24, 18, 24, 14)
        l.setSpacing(3)

        title = QLabel("Seguridad")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setProperty("class", "view-title")

        sub = QLabel("Administra cuentas de usuario MySQL, hosts autorizados y privilegios de acceso.")
        sub.setFont(QFont("Segoe UI", 12))
        sub.setProperty("class", "text-muted")

        l.addWidget(title)
        l.addWidget(sub)
        h.setStyleSheet("border-bottom: 1px solid #21262D;")
        return h

    # ─────────────────────────────────────────────────────────────────────────
    # Card izquierda — Tabla de usuarios
    # ─────────────────────────────────────────────────────────────────────────

    def _users_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("formCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Header
        hdr = QFrame()
        hdr.setFixedHeight(52)
        hdr.setStyleSheet("""
            QFrame {
                border: none;
                border-bottom: 1px solid #30363D;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                background: transparent;
            }
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(16, 0, 16, 0)

        t = QLabel("Usuarios registrados")
        t.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        t.setProperty("class", "view-subtitle-muted")

        self.user_count_label = QLabel("—")
        self.user_count_label.setFont(QFont("Segoe UI", 11))
        self.user_count_label.setProperty("class", "text-hint")
        self.user_count_label.setStyleSheet(
            "background-color: #21262D; border-radius: 10px; padding: 2px 10px;"
        )

        hl.addWidget(t)
        hl.addStretch()
        hl.addWidget(self.user_count_label)
        cl.addWidget(hdr)

        # Tabla
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["USUARIO", "HOST", "PRIVILEGIOS"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setHighlightSections(False)
        self.table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        cl.addWidget(self.table, 1)

        # Toolbar plana
        toolbar = QFrame()
        toolbar.setFixedHeight(48)
        toolbar.setStyleSheet("""
            QFrame {
                border: none;
                border-top: 1px solid #30363D;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background: transparent;
            }
        """)
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(12, 0, 12, 0)
        tl.setSpacing(6)

        self.btn_refresh = QPushButton("↺  Actualizar")
        self.btn_refresh.setProperty("class", "btn-secondary-animated")
        self.btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_refresh.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.btn_refresh.setFixedHeight(32)

        self.btn_edit = QPushButton("✎  Editar")
        self.btn_edit.setProperty("class", "btn-secondary-animated")
        self.btn_edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_edit.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.btn_edit.setFixedHeight(32)
        self.btn_edit.setEnabled(False)

        self.btn_delete = QPushButton("🗑  Eliminar")
        self.btn_delete.setProperty("class", "btn-danger")
        self.btn_delete.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_delete.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.btn_delete.setFixedHeight(32)
        self.btn_delete.setEnabled(False)

        tl.addWidget(self.btn_refresh)
        tl.addWidget(self.btn_edit)
        tl.addStretch()
        tl.addWidget(self.btn_delete)
        cl.addWidget(toolbar)

        self._load_sample_data()
        return card

    # ─────────────────────────────────────────────────────────────────────────
    # Card derecha — Formulario de creación
    # ─────────────────────────────────────────────────────────────────────────

    def _form_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("formCard")
        card.setMaximumWidth(420)
        cl = QVBoxLayout(card)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Header
        hdr = QFrame()
        hdr.setFixedHeight(52)
        hdr.setStyleSheet("""
            QFrame {
                border: none;
                border-bottom: 1px solid #30363D;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                background: transparent;
            }
        """)
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(16, 0, 16, 0)

        t = QLabel("Nueva cuenta")
        t.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        t.setProperty("class", "view-subtitle-muted")
        hl.addWidget(t)
        cl.addWidget(hdr)

        # Campos
        form = QFrame()
        fl = QVBoxLayout(form)
        fl.setContentsMargins(20, 20, 20, 20)
        fl.setSpacing(14)

        # Nombre de usuario
        fl.addWidget(self._lbl("Nombre de usuario"))
        self.txt_user = QLineEdit()
        self.txt_user.setPlaceholderText("ej.  usuario_app")
        self.txt_user.setFixedHeight(38)
        fl.addWidget(self.txt_user)

        # Host + preset inline
        fl.addWidget(self._lbl("Host autorizado"))
        host_row = QHBoxLayout(); host_row.setSpacing(6)
        self.txt_host = QLineEdit()
        self.txt_host.setText("%")
        self.txt_host.setFixedHeight(38)

        self.cmb_host_preset = QComboBox()
        self.cmb_host_preset.addItems(["Preset…", "localhost", "% (todos)", "127.0.0.1"])
        self.cmb_host_preset.setFixedHeight(38)
        self.cmb_host_preset.setFixedWidth(120)
        self.cmb_host_preset.currentTextChanged.connect(self._on_host_preset)

        host_row.addWidget(self.txt_host, 1)
        host_row.addWidget(self.cmb_host_preset)
        fl.addLayout(host_row)

        # Contraseña
        fl.addWidget(self._lbl("Contraseña"))
        pass_row = QHBoxLayout(); pass_row.setSpacing(6)
        self.txt_pass = QLineEdit()
        self.txt_pass.setPlaceholderText("Mínimo 6 caracteres")
        self.txt_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_pass.setFixedHeight(38)

        self.btn_show_pass = QPushButton("👁")
        self.btn_show_pass.setFixedSize(38, 38)
        self.btn_show_pass.setCheckable(True)
        self.btn_show_pass.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_show_pass.setProperty("class", "btn-secondary-animated")
        self.btn_show_pass.toggled.connect(self._toggle_pass_vis)

        pass_row.addWidget(self.txt_pass, 1)
        pass_row.addWidget(self.btn_show_pass)
        fl.addLayout(pass_row)

        self.pass_strength = PasswordStrengthIndicator()
        fl.addWidget(self.pass_strength)

        # Confirmar
        fl.addWidget(self._lbl("Confirmar contraseña"))
        self.txt_confirm = QLineEdit()
        self.txt_confirm.setPlaceholderText("Repite la contraseña")
        self.txt_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_confirm.setFixedHeight(38)
        fl.addWidget(self.txt_confirm)

        # Divisor
        fl.addWidget(self._hdiv())

        # Opciones
        self.chk_grant = QCheckBox("Otorgar privilegios administrativos")
        self.chk_expire = QCheckBox("Expirar contraseña en primer inicio")
        for chk in (self.chk_grant, self.chk_expire):
            chk.setFont(QFont("Segoe UI", 12))
            fl.addWidget(chk)

        # Mensaje de estado
        self.lbl_msg = QLabel("")
        self.lbl_msg.setWordWrap(True)
        self.lbl_msg.setFont(QFont("Segoe UI", 12))
        self.lbl_msg.hide()
        fl.addWidget(self.lbl_msg)

        fl.addStretch()

        # Botón de creación — full width
        self.btn_create = AnimatedButton("Crear usuario")
        self.btn_create.setProperty("class", "btn-primary")
        self.btn_create.setFixedHeight(40)
        self.btn_create.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        fl.addWidget(self.btn_create)

        # Nota
        note = QLabel("ℹ  Las cuentas nuevas tienen privilegios básicos. Usa 'Editar' para ampliarlos.")
        note.setFont(QFont("Segoe UI", 11))
        note.setProperty("class", "text-hint")
        note.setWordWrap(True)
        fl.addWidget(note)

        cl.addWidget(form, 1)
        return card

    # ── Helpers ───────────────────────────────────────────────────────────────

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

    def _show_msg(self, text: str, kind: str = "info"):
        # Usa los tokens del tema — solo necesitamos el color del tipo
        color_map = {
            "success": "#3FB950",   # SUCCESS
            "error":   "#F85149",   # ERROR
            "warning": "#D29922",   # WARNING
            "info":    "#58A6FF",   # INFO
        }
        c = color_map.get(kind, "#7D8590")
        self.lbl_msg.setText(text)
        self.lbl_msg.setStyleSheet(
            f"color:{c}; border-left:2px solid {c}; padding:7px 10px; border-radius:4px;"
        )
        self.lbl_msg.show()
        if kind != "error":
            QTimer.singleShot(5000, self.lbl_msg.hide)

    # ── Datos de ejemplo ─────────────────────────────────────────────────────

    def _load_sample_data(self):
        rows = [
            ("admin",    "localhost",   "Todos los privilegios"),
            ("app_user", "%",           "SELECT, INSERT, UPDATE"),
            ("readonly", "192.168.1.%", "SELECT"),
        ]
        self.table.setRowCount(len(rows))
        for r, (user, host, privs) in enumerate(rows):
            for c, val in enumerate([user, host, privs]):
                item = QTableWidgetItem(val)
                item.setFont(QFont("Segoe UI", 13))
                self.table.setItem(r, c, item)
            self.table.setRowHeight(r, 38)
        self.user_count_label.setText(str(len(rows)))

    # ── Lógica ────────────────────────────────────────────────────────────────

    def _on_host_preset(self, text: str):
        mapping = {"localhost": "localhost", "% (todos)": "%", "127.0.0.1": "127.0.0.1"}
        if text in mapping:
            self.txt_host.setText(mapping[text])
            self.cmb_host_preset.blockSignals(True)
            self.cmb_host_preset.setCurrentIndex(0)
            self.cmb_host_preset.blockSignals(False)

    def _toggle_pass_vis(self, checked: bool):
        mode = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self.txt_pass.setEchoMode(mode)
        self.txt_confirm.setEchoMode(mode)

    def _on_password_changed(self, text: str):
        self.pass_strength.check_strength(text)

    def _on_table_select(self):
        has = len(self.table.selectedItems()) > 0
        self.btn_delete.setEnabled(has)
        self.btn_edit.setEnabled(has)

    def _on_refresh_clicked(self):
        self._show_msg("Actualizando lista de usuarios...", "info")
        QTimer.singleShot(900, lambda: self._show_msg("Lista actualizada", "success"))

    def _on_edit_clicked(self):
        row = self.table.currentRow()
        if row >= 0:
            user = self.table.item(row, 0).text()
            self._show_msg(f"Editar privilegios de '{user}' — (pendiente)", "info")

    def _on_delete_clicked(self):
        row = self.table.currentRow()
        if row < 0:
            return
        user = self.table.item(row, 0).text()
        host = self.table.item(row, 1).text()
        reply = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Eliminar '{user}'@'{host}'?\nEsta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)
            self.user_count_label.setText(str(self.table.rowCount()))
            self._show_msg(f"Usuario '{user}' eliminado", "success")

    def _on_create_clicked(self):
        user = self.txt_user.text().strip()
        host = self.txt_host.text().strip()
        pw   = self.txt_pass.text()
        conf = self.txt_confirm.text()

        checks = [
            (not user,    "El nombre de usuario es obligatorio"),
            (not host,    "El host es obligatorio"),
            (not pw,      "La contraseña es obligatoria"),
            (pw != conf,  "Las contraseñas no coinciden"),
            (len(pw) < 6, "La contraseña debe tener al menos 6 caracteres"),
        ]
        for condition, msg in checks:
            if condition:
                self._show_msg(msg, "error")
                return

        for r in range(self.table.rowCount()):
            if self.table.item(r, 0).text() == user and self.table.item(r, 1).text() == host:
                self._show_msg(f"'{user}'@'{host}' ya existe", "error")
                return

        r = self.table.rowCount()
        self.table.insertRow(r)
        privs = "Administrativos" if self.chk_grant.isChecked() else "Básicos"
        for c, val in enumerate([user, host, privs]):
            item = QTableWidgetItem(val)
            item.setFont(QFont("Segoe UI", 13))
            self.table.setItem(r, c, item)
        self.table.setRowHeight(r, 38)
        self.user_count_label.setText(str(self.table.rowCount()))

        for w in (self.txt_user, self.txt_pass, self.txt_confirm):
            w.clear()
        self.chk_grant.setChecked(False)
        self.chk_expire.setChecked(False)
        self._show_msg(f"'{user}'@'{host}' creado exitosamente", "success")

    # ── API pública ─────────────────────────────────────────────────────────

    def show_message(self, msg: str, msg_type: str = "info"):
        self._show_msg(msg, msg_type)