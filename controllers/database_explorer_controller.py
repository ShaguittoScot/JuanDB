from PyQt6.QtCore import QObject
from services.db_service import get_databases, get_tables, get_table_permissions
from utils.database_sanitizer import DatabaseSanitizer
from PyQt6.QtWidgets import QMessageBox


class DatabaseExplorerController(QObject):
    """
    Controlador para el Explorador de Bases de Datos.
    Conecta la lógica de negocio (db_service) con la vista.
    """

    def __init__(self, view):
        super().__init__()
        self.view = view
        self._setup_connections()
        self.load_databases()

    def _setup_connections(self):
        self.view.refresh_requested.connect(self.load_databases)
        self.view.database_selected.connect(self.load_tables)
        self.view.drop_database_requested.connect(self.drop_database)
        self.view.drop_table_requested.connect(self.drop_table)

    def load_databases(self):
        dbs_raw = get_databases()
        raw_names = []
        
        for db in dbs_raw:
            if isinstance(db, tuple) and len(db) > 0:
                raw_names.append(db[0])
            elif isinstance(db, str):
                print(f"[Explorer] Info: {db}")
        
        # Filtrar vía Sanitizer
        valid_dbs = DatabaseSanitizer.filter_databases(raw_names)
        self.view.set_databases(valid_dbs)

    def load_tables(self, db_name: str):
        # Evitar recargar si es lo mismo (opcional)
        tables_raw = get_tables(db_name)
        valid_tables = []
        
        for t in tables_raw:
            if isinstance(t, tuple) and len(t) > 0:
                valid_tables.append(t[0])
            elif isinstance(t, str):
                print(f"[Explorer] Error cargando tablas de {db_name}: {t}")
        
        # Obtener permisos reales
        permissions = get_table_permissions(db_name, valid_tables)
        
        # Convertir a lista de tuplas (table_name, permission_level)
        table_data = [(t, permissions.get(t, 0)) for t in valid_tables]
                
        self.view.set_tables(db_name, table_data)

    def check_permissions(self, user: str, table_name: str) -> int:
        """
        Método solicitado para verificar nivel de acceso.
        """
        # En esta arquitectura, el controlador ya procesa esto en load_tables,
        # pero exponemos el método para uso externo si es necesario.
        # Por simplicidad, re-consultamos si es necesario, 
        # pero usualmente la vista ya tiene el estado.
        return get_table_permissions(self.view._current_db, [table_name]).get(table_name, 0)

    def drop_database(self, db_name: str):
        # Validación de seguridad
        if not DatabaseSanitizer.is_safe_database(db_name):
            QMessageBox.critical(self.view, "Acceso Denegado", 
                                f"No se permite eliminar la base de datos de sistema '{db_name}' sin Modo Avanzado.")
            return

        print(f"[Explorer] Ejecutando: DROP DATABASE `{db_name}`")
        # Aquí iría la llamada real al service
        # Para demostración, simplemente refrescamos
        QMessageBox.information(self.view, "Acción Simulada", f"Se activó la señal para eliminar '{db_name}'.\n(Lógica de persistencia pendiente en db_service).")
        self.load_databases()

    def drop_table(self, db_name: str, table_name: str):
        print(f"[Explorer] Ejecutando: DROP TABLE `{db_name}`.`{table_name}`")
        QMessageBox.information(self.view, "Acción Simulada", f"Se activó la señal para eliminar tabla '{table_name}' de '{db_name}'.")
        self.load_tables(db_name)
