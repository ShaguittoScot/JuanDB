import subprocess
import os
from datetime import datetime
from services.config_service import ConfigService

class BackupService:
    @staticmethod
    def create_backup(db_name: str, dest_dir: str) -> str:
        """
        Genera un respaldo de la base de datos y retorna la ruta del archivo.
        Lanza excepción si falla.
        """
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{db_name}_backup_{timestamp}.sql"
        filepath = os.path.normpath(os.path.join(dest_dir, filename))

        cfg = ConfigService.get_db_config()
        host = cfg.get("host", "localhost")
        port = str(cfg.get("port", 3306))
        user = cfg.get("user", "root")
        password = cfg.get("password", "")

        # Comando mysqldump
        cmd = [
            "mysqldump",
            f"--host={host}",
            f"--port={port}",
            f"--user={user}"
        ]
        
        if password:
            cmd.append(f"--password={password}")
            
        cmd.append(db_name)

        # Ejecutar el comando para crear el dump
        with open(filepath, 'w', encoding='utf-8') as f:
            process = subprocess.Popen(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            _, stderr = process.communicate()
            
            if process.returncode != 0:
                # Falló, tratar de borrar el archivo truncado
                if os.path.exists(filepath):
                    os.remove(filepath)
                raise Exception(f"No se pudo crear el backup. Error mysqldump:\n{stderr}\n\nNota: 'mysqldump' debe estar en el PATH del sistema.")

        return filepath

    @staticmethod
    def restore_backup(db_name: str, filepath: str) -> None:
        """
        Restaura una base de datos a partir de un archivo .sql.
        Lanza excepción si falla.
        """
        if not os.path.exists(filepath):
            raise Exception("El archivo de respaldo no existe.")

        cfg = ConfigService.get_db_config()
        host = cfg.get("host", "localhost")
        port = str(cfg.get("port", 3306))
        user = cfg.get("user", "root")
        password = cfg.get("password", "")

        # Comando mysql
        cmd = [
            "mysql",
            f"--host={host}",
            f"--port={port}",
            f"--user={user}"
        ]
        
        if password:
            cmd.append(f"--password={password}")
            
        if db_name:
            cmd.append(db_name)

        with open(filepath, 'r', encoding='utf-8') as f:
            process = subprocess.Popen(cmd, stdin=f, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            _, stderr = process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"No se pudo restaurar el backup. Error mysql:\n{stderr}\n\nNota: 'mysql' debe estar en el PATH del sistema.")

    @staticmethod
    def create_database_if_not_exists(db_name: str) -> None:
        """
        Crea la base de datos si no existe.
        """
        from database.connection import get_connection
        conn = get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            finally:
                conn.close()
