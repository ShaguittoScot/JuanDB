from database.connection import get_connection

class SecurityService:
    @staticmethod
    def get_users() -> list:
        conn = get_connection()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos.")
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT User, Host FROM mysql.user WHERE User != '' ORDER BY User ASC")
            return cursor.fetchall()
        finally:
            if conn:
                conn.close()

    @staticmethod
    def create_user(username: str, password: str, host: str = '%') -> bool:
        conn = get_connection()
        if not conn:
            raise Exception("Error de conexión.")
            
        try:
            cursor = conn.cursor()
            # Escapar comillas en usuario/password para evitar inyección simple. 
            # (Aunque execute paramétrico no soporta DDL/DCL en todos los drivers).
            username_safe = username.replace("'", "''")
            password_safe = password.replace("'", "''")
            host_safe = host.replace("'", "''")
            
            # Crear usuario
            cursor.execute(f"CREATE USER '{username_safe}'@'{host_safe}' IDENTIFIED BY '{password_safe}'")
            # Otorgar permisos base (para un uso genérico, a veces es GRANT ALL, o GRANT USAGE)
            # Para la demo, dejaremos GRANT USAGE para que al menos se cree correctamente.
            cursor.execute(f"GRANT USAGE ON *.* TO '{username_safe}'@'{host_safe}'")
            cursor.execute("FLUSH PRIVILEGES")
            
            return True
        except Exception as e:
            raise Exception(f"No se pudo crear: {str(e)}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def delete_user(username: str, host: str) -> bool:
        if username.lower() == 'root':
            raise Exception("Seguridad: No se permite eliminar al usuario root desde la interfaz.")
            
        conn = get_connection()
        if not conn:
            raise Exception("Error de conexión.")
            
        try:
            cursor = conn.cursor()
            username_safe = username.replace("'", "''")
            host_safe = host.replace("'", "''")
            
            cursor.execute(f"DROP USER '{username_safe}'@'{host_safe}'")
            cursor.execute("FLUSH PRIVILEGES")
            return True
        except Exception as e:
            raise Exception(f"Fallo al eliminar: {str(e)}")
        finally:
            if conn:
                conn.close()
