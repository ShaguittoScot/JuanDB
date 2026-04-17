from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QListWidget, QListWidgetItem, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QSplitter, QAbstractItemView,
    QSizePolicy, QMessageBox, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QCursor
import qtawesome as qta

from ui.colors import DARK_THEME as APP_COLORS
from ui.components.help_icon import HelpIcon
from ui.components.animated_button import AnimatedButton


class DatabaseExplorer(QWidget):
    """
    Vista de Explorador de Base de Datos:
    - Lista de bases de datos (izquierda)
    - Detalle de tablas y acciones (derecha)
    """

    refresh_requested = pyqtSignal()
    database_selected = pyqtSignal(str) # db_name
    drop_database_requested = pyqtSignal(str) # db_name
    drop_table_requested = pyqtSignal(str, str) # db_name, table_name

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("databaseExplorer")
        self._current_db = None
        self._build_ui()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────────
        header_bar = QHBoxLayout()
        header_bar.setContentsMargins(24, 18, 24, 0)
        header_bar.addStretch()
        header_bar.addWidget(HelpIcon("Visualiza, administra y elimina bases de datos y tablas de tu servidor MySQL."))
        root.addLayout(header_bar)

        # ── Cuerpo con Splitter ───────────────────────────────────────────────
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(1)
        self.splitter.setStyleSheet(f"QSplitter::handle {{ background-color: {APP_COLORS['BORDER']}; }}")

        # --- Lado Izquierdo: Lista de DBs ---
        left_panel = QFrame()
        left_panel.setObjectName("explorerLeftPanel")
        ll = QVBoxLayout(left_panel)
        ll.setContentsMargins(24, 20, 16, 24)
        ll.setSpacing(16)

        # Header de lista
        list_hdr = QHBoxLayout()
        lbl_dbs = QLabel("BASES DE DATOS")
        lbl_dbs.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        lbl_dbs.setStyleSheet(f"color: {APP_COLORS['TEXT_MUTED']}; letter-spacing: 1px;")
        
        self.btn_refresh = QPushButton()
        self.btn_refresh.setIcon(qta.icon('fa5s.sync-alt', color=APP_COLORS['TEXT_MUTED']))
        self.btn_refresh.setIconSize(QSize(14, 14))
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setFixedSize(24, 24)
        self.btn_refresh.setStyleSheet("border: none; background: transparent;")
        self.btn_refresh.clicked.connect(self.refresh_requested.emit)

        list_hdr.addWidget(lbl_dbs)
        list_hdr.addStretch()
        list_hdr.addWidget(self.btn_refresh)
        ll.addLayout(list_hdr)

        self.db_list = QListWidget()
        self.db_list.setObjectName("explorerDbList")
        self.db_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.db_list.setSpacing(2)
        self.db_list.currentRowChanged.connect(self._on_db_item_changed)
        # Efecto de hover se maneja via CSS global o property
        ll.addWidget(self.db_list)

        # --- Lado Derecho: Detalle ---
        self.right_container = QStackedWidget()
        
        # Estado vacío
        self.empty_view = QLabel("Selecciona una base de datos\npara ver sus detalles")
        self.empty_view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_view.setFont(QFont("Segoe UI", 12))
        self.empty_view.setStyleSheet(f"color: {APP_COLORS['TEXT_HINT']};")
        
        # Detalle de DB
        self.detail_view = self._build_detail_card()
        
        self.right_container.addWidget(self.empty_view)
        self.right_container.addWidget(self.detail_view)
        
        self.splitter.addWidget(left_panel)
        self.splitter.addWidget(self.right_container)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 7)

        root.addWidget(self.splitter, 1)

    def _build_detail_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("formCard")
        cl = QVBoxLayout(card)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(0)

        # Header del detalle
        hdr = QFrame()
        hdr.setFixedHeight(56)
        hdr.setStyleSheet(f"border-bottom: 1px solid {APP_COLORS['BORDER']}; background: transparent;")
        hl = QHBoxLayout(hdr)
        hl.setContentsMargins(20, 0, 20, 0)

        self.lbl_selected_db = QLabel("")
        self.lbl_selected_db.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.lbl_selected_db.setStyleSheet(f"color: {APP_COLORS['TEXT_LIGHT']};")
        
        self.btn_drop_db = QPushButton("  Eliminar Base de Datos")
        self.btn_drop_db.setIcon(qta.icon('fa5s.trash', color=APP_COLORS['ERROR']))
        self.btn_drop_db.setIconSize(QSize(14, 14))
        self.btn_drop_db.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_drop_db.setFixedHeight(30)
        self.btn_drop_db.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
        self.btn_drop_db.setStyleSheet(f"""
            QPushButton {{
                color: {APP_COLORS['ERROR']};
                border: 1px solid rgba(248, 81, 73, 0.3);
                border-radius: 4px;
                padding: 0 12px;
                background: transparent;
            }}
            QPushButton:hover {{
                background: rgba(248, 81, 73, 0.1);
                border: 1px solid {APP_COLORS['ERROR']};
            }}
        """)
        self.btn_drop_db.clicked.connect(self._confirm_drop_db)

        hl.addWidget(self.lbl_selected_db)
        hl.addStretch()
        hl.addWidget(self.btn_drop_db)
        cl.addWidget(hdr)

        # Tabla de tablas
        self.table_list = QTableWidget()
        self.table_list.setColumnCount(2)
        self.table_list.setHorizontalHeaderLabels(["NOMBRE DE TABLA", "ACCIONES"])
        self.table_list.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table_list.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        self.table_list.setColumnWidth(1, 100)
        self.table_list.verticalHeader().setVisible(False)
        self.table_list.setShowGrid(False)
        self.table_list.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_list.setStyleSheet(f"""
            QTableWidget {{ background: transparent; border: none; }}
            QHeaderView::section {{
                background: transparent;
                padding: 10px;
                color: {APP_COLORS['TEXT_MUTED']};
                font-weight: bold;
                border: none;
                border-bottom: 1px solid {APP_COLORS['BORDER']};
            }}
        """)
        
        cl.addWidget(self.table_list, 1)

        wrapper = QFrame()
        wl = QVBoxLayout(wrapper)
        wl.setContentsMargins(24, 24, 24, 24)
        wl.addWidget(card)
        
        return wrapper

    def set_databases(self, dbs: list):
        self.db_list.clear()
        for db in dbs:
            item = QListWidgetItem(f"   {db}")
            item.setIcon(qta.icon('fa5s.database', color=APP_COLORS['TEXT_MUTED']))
            item.setFont(QFont("Segoe UI", 11))
            self.db_list.addItem(item)
        
        if self._current_db is None:
            self.right_container.setCurrentIndex(0)

    def set_tables(self, db_name: str, tables_with_perms: list):
        """
        Renderiza la lista de tablas con semáforos de permisos.
        tables_with_perms: list of (table_name, permission_level)
        levels: 2: Green, 1: Yellow, 0: Red
        """
        self._current_db = db_name
        self.lbl_selected_db.setText(db_name)
        self.right_container.setCurrentIndex(1)
        
        self.table_list.setRowCount(len(tables_with_perms))
        
        perm_config = {
            2: {"color": "#2dd4bf", "text": "Control Total", "desc": "Tienes permisos de lectura y escritura en esta tabla."},
            1: {"color": "#f59e0b", "text": "Solo Lectura", "desc": "Acceso limitado: Solo puedes realizar consultas (SELECT)."},
            0: {"color": "#f43f5e", "text": "Acceso Denegado", "desc": "No tienes permisos para acceder a esta tabla."}
        }

        for i, (table, level) in enumerate(tables_with_perms):
            conf = perm_config.get(level, perm_config[0])
            
            # --- Celda 0: Nombre + Semáforo ---
            cell_widget = QWidget()
            cell_lay = QHBoxLayout(cell_widget)
            cell_lay.setContentsMargins(12, 0, 12, 0)
            cell_lay.setSpacing(10)
            
            # El Semáforo (Círculo)
            semaphore = QLabel()
            semaphore.setFixedSize(10, 10)
            semaphore.setToolTip(conf["desc"])
            semaphore.setStyleSheet(f"""
                QLabel {{
                    background-color: {conf['color']};
                    border-radius: 5px;
                }}
            """)
            
            name_lbl = QLabel(table)
            name_lbl.setFont(QFont("Segoe UI", 11, QFont.Weight.Medium))
            
            cell_lay.addWidget(semaphore)
            cell_lay.addWidget(name_lbl)
            cell_lay.addStretch()
            
            self.table_list.setCellWidget(i, 0, cell_widget)
            
            # --- Celda 1: Acciones ---
            btn_del = QPushButton()
            btn_del.setIcon(qta.icon('fa5s.trash', color=APP_COLORS['TEXT_HINT']))
            btn_del.setIconSize(QSize(14, 14))
            btn_del.setFixedSize(28, 28)
            btn_del.setToolTip("Eliminar tabla")
            btn_del.setStyleSheet(f"""
                QPushButton {{ border: none; background: transparent; border-radius: 4px; }}
                QPushButton:hover {{ background: rgba(248, 81, 73, 0.1); }}
            """)
            btn_del.clicked.connect(lambda chk, t=table: self._confirm_drop_table(t))
            
            action_w = QWidget()
            al = QHBoxLayout(action_w)
            al.setContentsMargins(0, 0, 0, 0)
            al.setAlignment(Qt.AlignmentFlag.AlignCenter)
            al.addWidget(btn_del)
            
            self.table_list.setCellWidget(i, 1, action_w)
            self.table_list.setRowHeight(i, 42)

            # --- Lógica de Restricción ---
            if level == 1: # Amarillo: Bloquear eliminación
                btn_del.setEnabled(False)
                btn_del.setToolTip("Acceso limitado: No puedes eliminar esta tabla")
                btn_del.setCursor(Qt.CursorShape.ForbiddenCursor)
            
            elif level == 0: # Rojo: Inhabilitar fila completa
                name_lbl.setStyleSheet(f"color: {APP_COLORS['TEXT_HINT']};")
                btn_del.setVisible(False)
                cell_widget.setEnabled(False)
                # Opcional: Hacer la celda no seleccionable
                it = QTableWidgetItem()
                it.setFlags(Qt.ItemFlag.NoItemFlags)
                self.table_list.setItem(i, 0, it)

    def _on_db_item_changed(self, row: int):
        if row >= 0:
            db_name = self.db_list.item(row).text().strip()
            self.database_selected.emit(db_name)

    def _confirm_drop_db(self):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmar eliminación")
        msg.setText(f"¿Estás seguro de eliminar la base de datos '{self._current_db}'?")
        msg.setInformativeText("Esta acción no se puede deshacer y borrará todas sus tablas y datos.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        # Aplicar estilo al message box
        msg.setStyleSheet(f"""
            QMessageBox {{ background-color: {APP_COLORS['BG_SURFACE']}; }}
            QLabel {{ color: {APP_COLORS['TEXT_LIGHT']}; }}
            QPushButton {{
                padding: 6px 16px;
                border-radius: 4px;
                min-width: 80px;
            }}
        """)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.drop_database_requested.emit(self._current_db)

    def _confirm_drop_table(self, table_name: str):
        msg = QMessageBox()
        msg.setWindowTitle("Confirmar eliminación")
        msg.setText(f"¿Estás seguro de eliminar la tabla '{table_name}'?")
        msg.setInformativeText("Esta acción no se puede deshacer y borrará todos los registros de la tabla.")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg.setDefaultButton(QMessageBox.StandardButton.No)
        
        msg.setStyleSheet(f"""
            QMessageBox {{ background-color: {APP_COLORS['BG_SURFACE']}; }}
            QLabel {{ color: {APP_COLORS['TEXT_LIGHT']}; }}
        """)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            self.drop_table_requested.emit(self._current_db, table_name)
