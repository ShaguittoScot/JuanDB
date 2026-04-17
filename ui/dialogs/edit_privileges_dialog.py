from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QCheckBox, 
    QPushButton, QComboBox, QGroupBox, QGridLayout, QWidget, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
import qtawesome as qta
from services.db_service import get_databases


class EditPrivilegesDialog(QDialog):
    """
    Diálogo para gestionar privilegios de un usuario MySQL.
    Permite seleccionar alcance (Global/Tabla) y permisos granulares.
    """
    
    def __init__(self, username, host, current_grants=None, parent=None):
        super().__init__(parent)
        self.username = username
        self.host = host
        self.current_grants = current_grants or []
        
        self.setWindowTitle(f"Gestionar Permisos: {username}")
        self.setMinimumWidth(500)
        self.setObjectName("formCard")
        
        # Heredar el stylesheet de la aplicación
        app = QApplication.instance()
        if app:
            self.setStyleSheet(app.styleSheet())
        
        self._build_ui()
        self._load_current_state()
        self.update_semaphore()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # ── Cabecera ──────────────────────────────────────────────────
        header = QVBoxLayout()
        header.setSpacing(4)
        
        title = QLabel(f"Gestionar Permisos")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setProperty("class", "text-light")
        
        subtitle = QLabel(f"Usuario: {self.username}@{self.host}")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setProperty("class", "text-muted")
        
        header.addWidget(title)
        header.addWidget(subtitle)
        layout.addLayout(header)

        # ── Alcance (Scope) ───────────────────────────────────────────
        scope_layout = QVBoxLayout()
        scope_layout.setSpacing(12)
        
        scope_lbl = QLabel("Alcance de los permisos")
        scope_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        scope_lbl.setProperty("class", "text-muted")
        
        self.cmb_scope = QComboBox()
        self.cmb_scope.setFixedHeight(42)
        self.cmb_scope.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cmb_scope.addItem("Toda la Base de Datos (*.*)", "*.*")
        
        # Cargar bases de datos reales para el alcance específico
        try:
            dbs = get_databases()
            for db in dbs:
                if isinstance(db, tuple) and len(db) > 0:
                    name = db[0]
                    if name.lower() not in ["information_schema", "mysql", "performance_schema", "sys"]:
                        self.cmb_scope.addItem(f"Esquema: {name}.*", f"`{name}`.*")
        except:
            # Fallback si no hay conexión
            pass
        
        scope_layout.addWidget(scope_lbl)
        scope_layout.addWidget(self.cmb_scope)
        layout.addLayout(scope_layout)

        # ── Divisor ───────────────────────────────────────────────────
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: #30363D; border: none;")
        line.setFixedHeight(1)
        layout.addWidget(line)

        # ── Matriz de Permisos ────────────────────────────────────────
        matrix_container = QWidget()
        matrix_layout = QVBoxLayout(matrix_container)
        matrix_layout.setContentsMargins(0, 0, 0, 0)
        matrix_layout.setSpacing(20)

        # Grupo: Datos
        data_group = QGroupBox("Datos (Lectura/Escritura)")
        data_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        data_grid = QGridLayout(data_group)
        data_grid.setContentsMargins(16, 16, 16, 16)
        
        self.chk_select = QCheckBox("SELECT")
        self.chk_insert = QCheckBox("INSERT")
        self.chk_update = QCheckBox("UPDATE")
        self.chk_delete = QCheckBox("DELETE")
        
        self.data_checks = [self.chk_select, self.chk_insert, self.chk_update, self.chk_delete]
        data_grid.addWidget(self.chk_select, 0, 0)
        data_grid.addWidget(self.chk_insert, 0, 1)
        data_grid.addWidget(self.chk_update, 1, 0)
        data_grid.addWidget(self.chk_delete, 1, 1)

        # Grupo: Estructura
        struct_group = QGroupBox("Estructura (DDL)")
        struct_group.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        struct_grid = QGridLayout(struct_group)
        struct_grid.setContentsMargins(16, 16, 16, 16)
        
        self.chk_create = QCheckBox("CREATE")
        self.chk_drop   = QCheckBox("DROP")
        self.chk_alter  = QCheckBox("ALTER")
        
        self.struct_checks = [self.chk_create, self.chk_drop, self.chk_alter]
        struct_grid.addWidget(self.chk_create, 0, 0)
        struct_grid.addWidget(self.chk_drop, 0, 1)
        struct_grid.addWidget(self.chk_alter, 1, 0)

        matrix_layout.addWidget(data_group)
        matrix_layout.addWidget(struct_group)
        layout.addWidget(matrix_container)

        # Conectar cambios para el semáforo
        for chk in self.data_checks + self.struct_checks:
            chk.stateChanged.connect(self.update_semaphore)

        # ── Footer con Semáforo y Botones ─────────────────────────────
        footer = QHBoxLayout()
        
        # Semáforo de Previsualización
        self.semaphore_icon = QLabel()
        self.semaphore_icon.setFixedSize(16, 16)
        self.semaphore_icon.setStyleSheet("background-color: #F85149; border-radius: 8px;") # Default Red
        
        self.semaphore_text = QLabel("Sin permisos")
        self.semaphore_text.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.semaphore_text.setProperty("class", "text-muted")
        
        footer.addWidget(self.semaphore_icon)
        footer.addWidget(self.semaphore_text)
        footer.addStretch()
        
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)
        btn_cancel.setProperty("class", "btn-secondary-animated")
        btn_cancel.setFixedHeight(36)
        
        self.btn_save = QPushButton("Guardar Cambios")
        self.btn_save.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_save.clicked.connect(self.accept)
        self.btn_save.setProperty("class", "btn-primary")
        self.btn_save.setFixedHeight(36)
        self.btn_save.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        
        footer.addWidget(btn_cancel)
        footer.addWidget(self.btn_save)
        layout.addLayout(footer)

    def update_semaphore(self):
        """Actualiza el color del círculo según los checkboxes marcados."""
        has_select = self.chk_select.isChecked()
        has_write = any(chk.isChecked() for chk in (self.data_checks[1:] + self.struct_checks))
        
        if has_select and has_write:
            color = "#3FB950" # Green
            text = "Control Total"
        elif has_select:
            color = "#D29922" # Yellow
            text = "Solo Lectura"
        else:
            color = "#F85149" # Red
            text = "Sin permisos"
            
        self.semaphore_icon.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        self.semaphore_text.setText(text)

    def _load_current_state(self):
        """Parsea los grants actuales para marcar los checkboxes."""
        grants_all = " ".join(self.current_grants).upper()
        
        if "ALL PRIVILEGES" in grants_all:
            for chk in self.data_checks + self.struct_checks:
                chk.setChecked(True)
            return

        # Mapeo simple de keywords
        mapping = {
            "SELECT": self.chk_select,
            "INSERT": self.chk_insert,
            "UPDATE": self.chk_update,
            "DELETE": self.chk_delete,
            "CREATE": self.chk_create,
            "DROP":   self.chk_drop,
            "ALTER":  self.chk_alter
        }
        
        for p, chk in mapping.items():
            if p in grants_all:
                chk.setChecked(True)

    def get_selected_privileges(self) -> list:
        """Retorna la lista de strings de privilegios seleccionados."""
        mapping = {
            "SELECT": self.chk_select,
            "INSERT": self.chk_insert,
            "UPDATE": self.chk_update,
            "DELETE": self.chk_delete,
            "CREATE": self.chk_create,
            "DROP":   self.chk_drop,
            "ALTER":  self.chk_alter
        }
        selected = [p for p, chk in mapping.items() if chk.isChecked()]
        return selected

    def get_scope(self) -> str:
        return self.cmb_scope.currentData()
