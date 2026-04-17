import csv
import json
import os
from pathlib import Path
from database.connection import get_connection

class ImportExportService:
    @staticmethod
    def _validate_export_path(dest_path: str) -> None:
        """
        Valida que el directorio existe y tiene permisos de escritura.
        Crea el directorio si es necesario.
        """
        try:
            path = Path(dest_path)
            parent_dir = path.parent
            
            # Crear directorio si no existe
            if not parent_dir.exists():
                try:
                    parent_dir.mkdir(parents=True, exist_ok=True)
                except PermissionError:
                    raise Exception(f"Permiso denegado: No se puede crear directorio '{parent_dir}'")
                except Exception as e:
                    raise Exception(f"Error creando directorio '{parent_dir}': {str(e)}")
            
            # Verificar permisos de escritura
            if not os.access(parent_dir, os.W_OK):
                raise Exception(f"Permiso denegado: No tiene permisos de escritura en '{parent_dir}'")
                
        except PermissionError as e:
            raise Exception(f"Acceso denegado al directorio: {str(e)}")
        except Exception as e:
            if "Permiso denegado" in str(e) or "Acceso denegado" in str(e):
                raise e
            raise Exception(f"Error validando ruta: {str(e)}")

    @staticmethod
    def export_data(db_name: str, table_name: str, fmt: str, dest_path: str) -> int:
        """
        Exporta la tabla solicitada a CSV o JSON.
        Retorna la cantidad de registros (filas) exportados exitosamente.
        """
        # Validar ruta antes de conectar a BD
        ImportExportService._validate_export_path(dest_path)
        
        conn = get_connection()
        if not conn:
            raise Exception("No se pudo conectar a la base de datos MySQL.")
            
        try:
            cursor = conn.cursor(dictionary=True) # Devuelve resultados como diccionarios
            cursor.execute(f"USE `{db_name}`")
            cursor.execute(f"SELECT * FROM `{table_name}`")
            rows = cursor.fetchall()
            
            if not rows:
                return 0
            
            try:
                if fmt == "CSV":
                    with open(dest_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                        writer.writeheader()
                        writer.writerows(rows)
                elif fmt == "JSON":
                    with open(dest_path, 'w', encoding='utf-8') as f:
                        # Convierte valores extraños nativos de SQL a texto (ej Datetime)
                        json.dump(rows, f, indent=4, default=str)
                else:
                    raise Exception(f"Formato no soportado: {fmt}")
            except PermissionError as e:
                raise Exception(f"Permiso denegado al escribir en '{dest_path}'. Verifique que el archivo no está abierto en otro programa o que tiene permisos de escritura.")
            except Exception as e:
                if "Permission denied" in str(e) or "Permiso denegado" in str(e):
                    raise Exception(f"Permiso denegado: {str(e)}")
                raise
                
            return len(rows)
        finally:
            if conn:
                conn.close()

    @staticmethod
    def import_data(db_name: str, table_name: str, fmt: str, source_path: str) -> int:
        """
        Lee el archivo CSV o JSON y lo inserta masivamente en la tabla especificada.
        Se asume que la cabecera / keys coinciden con las columnas de la Base de Datos.
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Archivo no encontrado: '{source_path}'")
        
        # Verificar permisos de lectura
        if not os.access(source_path, os.R_OK):
            raise PermissionError(f"Permiso denegado al leer '{source_path}'. Verifique que tiene permisos de lectura.")
            
        data = []
        try:
            if fmt == "CSV":
                with open(source_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
            elif fmt == "JSON":
                with open(source_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                raise Exception("El formato seleccionado no se encuentra en el índice soportado.")
        except PermissionError as e:
            raise Exception(f"Permiso denegado al leer el archivo: {str(e)}")
        except Exception as e:
            if "Permiso" in str(e) or "Permission" in str(e):
                raise
            raise Exception(f"Error leyendo archivo: {str(e)}")
            
        if not data:
            return 0
            
        conn = get_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión para transferir los datos local-sql.")
            
        try:
            cursor = conn.cursor()
            cursor.execute(f"USE `{db_name}`")
            
            columns = list(data[0].keys())
            cols_str = ", ".join([f"`{c}`" for c in columns])
            vals_str = ", ".join(["%s"] * len(columns))
            
            sql = f"INSERT INTO `{table_name}` ({cols_str}) VALUES ({vals_str})"
            
            # Optimización masiva usando executemany para reducir overhead I/O SQL
            batch = [[row.get(col) for col in columns] for row in data]
            cursor.executemany(sql, batch)
            conn.commit()
            
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise Exception(f"Fallo al correr el comando INSERT bulk: {str(e)}")
        finally:
            if conn:
                conn.close()
