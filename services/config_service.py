import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")

class ConfigService:
    @staticmethod
    def load_config() -> dict:
        if not os.path.exists(CONFIG_PATH):
            return {}
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def save_config(config_data: dict) -> bool:
        try:
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)
            return True
        except Exception as e:
            print("Error saving config:", e)
            return False

    @staticmethod
    def clear_config() -> bool:
        if os.path.exists(CONFIG_PATH):
            try:
                os.remove(CONFIG_PATH)
                return True
            except Exception as e:
                print("Error clearing config:", e)
                return False
        return True

    @staticmethod
    def is_setup_completed() -> bool:
        """Determina si la app ya fue configurada verificando datos clave"""
        cfg = ConfigService.load_config()
        return bool(cfg.get("host") and cfg.get("user") and cfg.get("app_user"))

    @staticmethod
    def get_db_config() -> dict:
        cfg = ConfigService.load_config()
        return {
            "host": cfg.get("host", "localhost"),
            "port": int(cfg.get("port", 3306)),
            "user": cfg.get("user", "root"),
            "password": cfg.get("password", "")
        }

