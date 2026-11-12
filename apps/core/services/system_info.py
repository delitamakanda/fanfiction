import platform
from datetime import datetime
from typing import Any

import django
import psutil

from apps.core.constants import BYTES_PER_GB, SERVER_START_TIME


def _usage_in_gb(info) -> dict[str, float]:
    return {
        "total_gb": round(info.total / BYTES_PER_GB, 2),
        "used_gb": round(info.used / BYTES_PER_GB, 2),
        "free_gb": round(info.free / BYTES_PER_GB, 2),
        "percent_gb": round(info.percent, 2),
    }


class ServerStatusService:
    """Host and runtime information for the admin-only system endpoint."""

    @staticmethod
    def get_uptime() -> str:
        return str(datetime.now() - SERVER_START_TIME).split(".")[0]

    @staticmethod
    def get_python_info() -> dict[str, str]:
        return {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
        }

    @staticmethod
    def get_django_info() -> dict[str, str]:
        return {"version": django.get_version()}

    @staticmethod
    def get_disk_usage(path: str = "/") -> dict[str, Any]:
        try:
            return _usage_in_gb(psutil.disk_usage(path))
        except OSError as exc:
            return {"error": str(exc)}

    @staticmethod
    def get_memory_usage() -> dict[str, Any]:
        return _usage_in_gb(psutil.virtual_memory())

    @staticmethod
    def get_cpu_usage() -> dict[str, Any]:
        return {
            # Non-blocking: compares with the previous call instead of sleeping.
            "percent": psutil.cpu_percent(interval=None),
            "count": psutil.cpu_count(),
            "architecture": platform.machine(),
            "processor_type": platform.processor(),
        }

    @staticmethod
    def get_system_info() -> dict[str, str]:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "node": platform.node(),
        }
