"""
server_status_checker.py — Componente reutilizable para verificar
la conectividad con el servidor MySQL/MariaDB.

Uso:
    checker = ServerStatusChecker()
    checker.status_changed.connect(my_callback)   # opcional
    layout.addWidget(checker)

El widget corre la verificación en un QThread para no bloquear la UI.
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QCursor

from ui.colors import DARK_THEME as APP_COLORS


# ─────────────────────────────────────────────────────────────────────────────
# Worker — ejecuta el ping al servidor en un hilo separado
# ─────────────────────────────────────────────────────────────────────────────

class _PingWorker(QThread):
    """
    Intenta una conexión real al servidor MySQL usando las credenciales
    almacenadas en config, o las inyectadas explícitamente.
    """
    result = pyqtSignal(bool, str)    # (ok, mensaje)

    def __init__(self, host: str = "", port: int = 0,
                 user: str = "", password: str = ""):
        super().__init__()
        self._host     = host
        self._port     = port
        self._user     = user
        self._password = password

    def run(self):
        try:
            if self._host:
                # Verificación con credenciales explícitas (SetupView)
                import mysql.connector
                conn = mysql.connector.connect(
                    host=self._host,
                    port=self._port or 3306,
                    user=self._user,
                    password=self._password,
                    connection_timeout=5,
                )
                version = conn.get_server_info()
                conn.close()
                self.result.emit(True, f"Conectado · MySQL/MariaDB {version}")
            else:
                # Verificación con credenciales guardadas en config
                from database.connection import get_connection
                conn = get_connection()
                if conn is None:
                    self.result.emit(False, "No se pudo establecer la conexión")
                    return
                cur = conn.cursor()
                cur.execute("SELECT VERSION()")
                version = cur.fetchone()[0]
                conn.close()
                self.result.emit(True, f"Conectado · {version}")
        except Exception as e:
            msg = str(e)
            # Extraer el mensaje más útil de errores comunes
            if "Access denied" in msg:
                msg = "Acceso denegado — verifica usuario y contraseña"
            elif "Can't connect" in msg or "Connection refused" in msg:
                msg = "No se puede conectar — verifica host y puerto"
            elif "timed out" in msg.lower():
                msg = "Tiempo de espera agotado (timeout)"
            self.result.emit(False, msg)


# ─────────────────────────────────────────────────────────────────────────────
# ServerStatusChecker — Widget visual
# ─────────────────────────────────────────────────────────────────────────────

class ServerStatusChecker(QFrame):
    """
    Botón + indicador de estado para verificar si MySQL/MariaDB está activo.

    Señales:
        status_changed(ok: bool, message: str)

    Props:
        get_credentials_fn  — función opcional que retorna (host, port, user, pwd)
                              para usar credenciales del formulario en tiempo real.
    """

    status_changed = pyqtSignal(bool, str)

    _STATES = {
        "idle":    ("○", APP_COLORS["TEXT_HINT"],    "—"),
        "checking":("◌", APP_COLORS["INFO"],         "Verificando..."),
        "ok":      ("●", APP_COLORS["SUCCESS"],      ""),
        "error":   ("●", APP_COLORS["ERROR"],        ""),
    }

    def __init__(self, get_credentials_fn=None, parent=None):
        super().__init__(parent)
        self._get_creds = get_credentials_fn   # callable → (host, port, user, pwd)
        self._worker: _PingWorker | None = None
        self._state = "idle"
        self._build_ui()
        self.setStyleSheet("QFrame { background: transparent; border: none; }")

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(8)

        # Botón de verificación
        self.btn_check = QPushButton("Verificar conexión")
        self.btn_check.setFixedHeight(36)
        self.btn_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_check.setProperty("class", "btn-secondary-animated")
        self.btn_check.setFont(QFont("Segoe UI", 12, QFont.Weight.Medium))
        self.btn_check.clicked.connect(self._on_check)

        # Indicador de estado: dot + texto
        self._dot = QLabel("○")
        self._dot.setFont(QFont("Segoe UI", 12))
        self._dot.setStyleSheet(f"color: {APP_COLORS['TEXT_HINT']}; border: none;")
        self._dot.setFixedWidth(16)

        self._status_lbl = QLabel("—")
        self._status_lbl.setFont(QFont("Segoe UI", 11))
        self._status_lbl.setStyleSheet(f"color: {APP_COLORS['TEXT_HINT']}; border: none;")
        self._status_lbl.setMinimumWidth(200)

        lay.addWidget(self.btn_check)
        lay.addWidget(self._dot)
        lay.addWidget(self._status_lbl, 1)

    # ── Animación de "verificando" ───────────────────────────────────────────

    def _start_spinner(self):
        self._spinner_chars = ["◌", "◎", "◉", "◎"]
        self._spinner_idx = 0
        self._spinner = QTimer(self)
        self._spinner.setInterval(200)
        self._spinner.timeout.connect(self._spin)
        self._spinner.start()

    def _spin(self):
        self._dot.setText(self._spinner_chars[self._spinner_idx % len(self._spinner_chars)])
        self._spinner_idx += 1

    def _stop_spinner(self):
        if hasattr(self, "_spinner") and self._spinner.isActive():
            self._spinner.stop()

    # ── Lógica ────────────────────────────────────────────────────────────────

    def _on_check(self):
        if self._worker and self._worker.isRunning():
            return  # ya hay verificación en curso

        self._set_state("checking")
        self.btn_check.setEnabled(False)
        self._start_spinner()

        # Obtener credenciales (del formulario si se provee la función)
        host, port, user, pwd = "", 0, "", ""
        if self._get_creds:
            try:
                host, port, user, pwd = self._get_creds()
            except Exception:
                pass

        self._worker = _PingWorker(host=host, port=port, user=user, password=pwd)
        self._worker.result.connect(self._on_result)
        self._worker.start()

    def _on_result(self, ok: bool, message: str):
        self._stop_spinner()
        self.btn_check.setEnabled(True)
        self._set_state("ok" if ok else "error", message)
        self.status_changed.emit(ok, message)

    def _set_state(self, state: str, detail: str = ""):
        self._state = state
        dot_char, color, default_msg = self._STATES[state]
        msg = detail if detail else default_msg

        if state != "checking":
            self._dot.setText(dot_char)

        self._dot.setStyleSheet(f"color: {color}; border: none;")
        self._status_lbl.setText(msg)
        self._status_lbl.setStyleSheet(f"color: {color}; border: none; font-size: 11px;")

    # ── API pública ───────────────────────────────────────────────────────────

    def reset(self):
        """Vuelve al estado inicial (idle)."""
        self._stop_spinner()
        self.btn_check.setEnabled(True)
        self._set_state("idle")
