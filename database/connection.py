import mysql.connector
from services.config_service import ConfigService

def get_connection():
    try:
        cfg = ConfigService.get_db_config()
        conn = mysql.connector.connect(**cfg, use_pure=True)
        print("✅ Conexión exitosa")
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None