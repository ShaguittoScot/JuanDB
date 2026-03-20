from PyQt6.QtCore import QObject, QTimer
from services.monitor_service import MonitorService

class MonitorController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_metrics)
        self.timer.setInterval(1000) # 1 segundo por defecto
        
        self.last_questions = 0
        self.history_len = 60
        self.time_data = list(range(-self.history_len + 1, 1))
        self.qps_history = [0] * self.history_len
        self.threads_history = [0] * self.history_len
        
        self.view.btn_toggle.clicked.connect(self.toggle_monitoring)

    def toggle_monitoring(self):
        if self.timer.isActive():
            self.timer.stop()
            self.view.btn_toggle.setText("▶ Iniciar Monitoreo")
            self.view.status_label.setText("Estado: Pausado")
            self.view.status_label.setStyleSheet("color: #A78BFA;")
        else:
            self.timer.start()
            self.view.btn_toggle.setText("⏸ Pausar Monitoreo")
            self.view.status_label.setText("Estado: Monitorizando...")
            self.view.status_label.setStyleSheet("color: #10B981;") # Verde
            self.update_metrics()

    def update_metrics(self):
        metrics = MonitorService.get_metrics()
        
        if not metrics:
            self.view.show_error("No se pudo conectar a la base de datos.")
            return
            
        # Parse data safely
        try:
            uptime = int(metrics.get("Uptime", 0))
            threads = metrics.get("Threads_connected", "0")
            questions = int(metrics.get("Questions", 0))
            
            # Consultas Por Segundo (QPS)
            qps = 0
            if self.last_questions > 0:
                qps = questions - self.last_questions
            self.last_questions = questions
            
            # Formatear Uptime
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{hours}h {minutes}m {seconds}s"
            
            self.view.update_display(
                uptime=uptime_str, 
                threads=str(threads), 
                qps=str(qps), 
                total_queries=str(questions)
            )
            
            # Actualizar historial para la gráfica
            self.qps_history.pop(0)
            self.qps_history.append(int(qps))
            
            self.threads_history.pop(0)
            self.threads_history.append(int(threads))
            
            self.view.update_graph(self.time_data, self.qps_history, self.threads_history)
            
            self.view.clear_error()
            
        except Exception as e:
            self.view.show_error(f"Error procesando métricas: {str(e)}")
