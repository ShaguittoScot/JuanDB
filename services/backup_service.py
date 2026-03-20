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
