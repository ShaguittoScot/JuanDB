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
            username_safe = username.replace("'", "''")
            password_safe = password.replace("'", "''")
            host_safe = host.replace("'", "''")
            
            cursor.execute(f"CREATE USER '{username_safe}'@'{host_safe}' IDENTIFIED BY '{password_safe}'")
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

    @staticmethod
    def get_user_grants(username: str, host: str) -> list:
        """Obtiene la lista de privilegios actuales de un usuario."""
        conn = get_connection()
        if not conn:
            raise Exception("No se pudo conectar.")
        try:
            cursor = conn.cursor()
            cursor.execute(f"SHOW GRANTS FOR '{username}'@'{host}'")
            grants = cursor.fetchall()
            return [g[0] for g in grants]
        finally:
            if conn:
                conn.close()

    @staticmethod
    def update_user_privileges(username: str, host: str, privileges: list, scope: str = "*.*") -> bool:
        """Construye y ejecuta la sentencia GRANT para actualizar privilegios."""
        conn = get_connection()
        if not conn:
            raise Exception("Error de conexión.")
        try:
            cursor = conn.cursor()
            username_safe = username.replace("'", "''")
            host_safe = host.replace("'", "''")
            
            # 1. Limpiar privilegios existentes para asegurar sobreescritura limpia
            try:
                cursor.execute(f"REVOKE ALL PRIVILEGES, GRANT OPTION FROM '{username_safe}'@'{host_safe}'")
            except:
                pass 
            
            # 2. Aplicar nuevos privilegios si hay alguno
            if privileges:
                priv_str = ", ".join(privileges)
                cursor.execute(f"GRANT {priv_str} ON {scope} TO '{username_safe}'@'{host_safe}'")
            
            cursor.execute("FLUSH PRIVILEGES")
            return True
        except Exception as e:
            raise Exception(f"Fallo al actualizar privilegios: {str(e)}")
        finally:
            if conn:
                conn.close()

    @staticmethod
    def flush_privileges():
        """Refresca la tabla de privilegios del servidor."""
        conn = get_connection()
        if not conn: return
        try:
            cursor = conn.cursor()
            cursor.execute("FLUSH PRIVILEGES")
        finally:
            if conn:
                conn.close()
