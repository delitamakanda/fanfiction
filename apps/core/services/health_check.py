from datetime import datetime
from typing import Any

from django.core.cache import cache
from django.db import DatabaseError, connection


class HealthCheckService:
    """Liveness information and dependency checks."""

    SERVICE_NAME = "fanfiction-api"
    VERSION = "1.0.0"

    @classmethod
    def get_health_check_results(cls) -> dict[str, Any]:
        return {
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "service": cls.SERVICE_NAME,
            "version": cls.VERSION,
        }

    @staticmethod
    def check_database_connection() -> dict[str, Any]:
        try:
            connection.ensure_connection()
        except DatabaseError as exc:
            return {"connected": False, "error": str(exc), "engine": None}
        db_settings = connection.settings_dict
        return {
            "connected": True,
            "engine": db_settings["ENGINE"].rsplit(".", 1)[-1],
            "name": str(db_settings.get("NAME") or "Unknown"),
            "host": db_settings.get("HOST") or "localhost",
        }

    @staticmethod
    def check_cache_connection() -> dict[str, Any]:
        try:
            cache.set("health_check", "ok", 10)
            connected = cache.get("health_check") == "ok"
        except Exception as exc:  # noqa: BLE001 - any backend error means "down"
            return {"connected": False, "error": str(exc)}
        return {"connected": connected, "backend": cache.__class__.__name__}
