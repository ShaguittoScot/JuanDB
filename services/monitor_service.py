from database.connection import get_connection

class MonitorService:
    @staticmethod
    def get_metrics() -> dict:
        """
        Obtiene métricas clave de rendimiento del servidor MySQL en tiempo real.
        """
        conn = get_connection()
        if not conn:
            return {}
            
        metrics = {}
        try:
            cursor = conn.cursor()
            cursor.execute("SHOW GLOBAL STATUS WHERE Variable_name IN ('Uptime', 'Threads_connected', 'Questions')")
            results = cursor.fetchall()
            for row in results:
                # row[0] = nombre de variable, row[1] = valor de variable
                metrics[row[0]] = row[1]
                
        except Exception as e:
            print("Error obteniendo métricas de monitoreo:", e)
        finally:
            if conn:
                conn.close()
                
        return metrics
