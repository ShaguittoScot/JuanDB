from database.connection import get_connection

def get_databases():
    conn = get_connection()
    
    if conn is None:
        return ["❌ No conexión"]

    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        result = cursor.fetchall()
        return result

    except Exception as e:
        return [f"Error SQL: {e}"]

    finally:
        if conn:
            conn.close()

def get_tables(db_name: str):
    conn = get_connection()
    if not conn:
        return ["❌ No conexión"]
        
    try:
        cursor = conn.cursor()
        cursor.execute(f"USE `{db_name}`")
        cursor.execute("SHOW TABLES")
        return cursor.fetchall()
    except Exception as e:
        return [f"Error SQL: {e}"]
    finally:
        if conn:
            conn.close()

def get_current_user_info():
    """
    Recupera el nombre de usuario y su rol dinámico desde el servidor SQL actual.
    """
    conn = get_connection()
    if not conn:
        return {"user": "Desconocido", "role": "Sin Conexión"}
        
    try:
        cursor = conn.cursor()
        
        # 1. Obtener el nombre
        cursor.execute("SELECT CURRENT_USER()")
        full_user = cursor.fetchone()[0] # ej. root@localhost
        username = full_user.split('@')[0].capitalize()
        
        # 2. Obtener privilegios
        cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
        grants = cursor.fetchall()
        
        role = "Usuario Estándar"
        for grant_row in grants:
            grant_str = grant_row[0].upper()
            if "GRANT ALL PRIVILEGES" in grant_str:
                role = "Administrador Total"
                break
                
        return {"user": username, "role": role}
    except Exception as e:
        return {"user": "Cuenta Local", "role": "Lector"}
    finally:
        if conn:
            conn.close()