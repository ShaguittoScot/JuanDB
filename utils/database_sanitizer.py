from services.config_service import ConfigService

class DatabaseSanitizer:
    """
    Clase centralizada para filtrar bases de datos y usuarios de sistema.
    Maneja el 'Modo Avanzado' (God Mode) que permite bypass de estos filtros.
    """

    SYSTEM_DATABASES = ['information_schema', 'mysql', 'performance_schema', 'sys']
    SYSTEM_USERS = ['mysql.session', 'mysql.infoschema', 'mysql.sys'] # root NO se excluye aquí

    @staticmethod
    def is_advanced_mode() -> bool:
        """Verifica el estado del modo avanzado en la configuración."""
        cfg = ConfigService.load_config()
        return bool(cfg.get("modo_avanzado", False))

    @classmethod
    def filter_databases(cls, db_list: list) -> list:
        """
        Filtra una lista de nombres de bases de datos.
        Si el modo avanzado está activo, devuelve todo.
        """
        if cls.is_advanced_mode():
            return db_list
        
        return [db for db in db_list if db.lower() not in cls.SYSTEM_DATABASES]

    @classmethod
    def filter_users(cls, user_list: list) -> list:
        """
        Filtra una lista de diccionarios de usuarios (con llave 'User').
        Excluye cuentas técnicas de MySQL pero mantiene 'root'.
        """
        if cls.is_advanced_mode():
            return user_list

        return [u for u in user_list if u.get("User", "").lower() not in cls.SYSTEM_USERS]

    @classmethod
    def is_safe_database(cls, db_name: str) -> bool:
        """
        Valida si una base de datos es segura de manipular.
        Bloquea bases de sistema si NO se está en modo avanzado.
        """
        if cls.is_advanced_mode():
            return True
        return db_name.lower() not in cls.SYSTEM_DATABASES

    @classmethod
    def is_safe_user(cls, user_name: str) -> bool:
        """Valida si un usuario es seguro de manipular."""
        if cls.is_advanced_mode():
            return True
        return user_name.lower() not in cls.SYSTEM_USERS
