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

def get_table_permissions(db_name: str, tables: list) -> dict:
    """
    Retorna un diccionario {table_name: level} donde level es:
    2: Verde (Lectura/Escritura), 1: Amarillo (Solo Lectura), 0: Rojo (Sin acceso)
    """
    conn = get_connection()
    if not conn:
        return {t: 0 for t in tables}
    
    permissions = {t: 0 for t in tables}
    try:
        cursor = conn.cursor()
        
        # 1. Verificar si tiene acceso total GLOBAL o de ESQUEMA
        cursor.execute("SHOW GRANTS FOR CURRENT_USER()")
        grants = cursor.fetchall()
        
        has_full_db_access = False
        for grant_row in grants:
            g = grant_row[0].upper()
            if "GRANT ALL PRIVILEGES" in g:
                if "*.*" in g or f"`{db_name}`.*" in g.lower() or f"{db_name}.*" in g.lower():
                    has_full_db_access = True
                    break
        
        if has_full_db_access:
            return {t: 2 for t in tables}

        # 2. Verificación individual
        cursor.execute(f"USE `{db_name}`")
        for table in tables:
            level = 0
            try:
                # ¿Puede leer?
                cursor.execute(f"SELECT 1 FROM `{table}` LIMIT 0")
                cursor.fetchall()
                level = 1
                
                # ¿Puede escribir?
                try:
                    # Update falso para probar permisos sin cambiar nada
                    cursor.execute(f"UPDATE `{table}` SET `{table}`.`{table}`=`{table}`.`{table}` WHERE 1=0")
                    level = 2
                except:
                    pass
            except:
                level = 0
            permissions[table] = level
            
        return permissions
    except Exception as e:
        print(f"[DB Service] Error en permisos: {e}")
        return {t: 1 for t in tables}
    finally:
        if conn:
            conn.close()