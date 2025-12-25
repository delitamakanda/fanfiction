import platform
from datetime import datetime
from typing import Dict, Any

import psutil
import django

from api.utils.constants import SERVER_START_TIME, BYTES_PER_GB

class ServerStatusService:

    @staticmethod
    def get_uptime() -> str:
        """
        Get the current server status.

        Returns:
            Dict[str, Any]: The server status.
        """
        return str(datetime.now() - SERVER_START_TIME).split('.')[0]

    @staticmethod
    def get_python_info() -> Dict[str, str]:
        """
        Get the Python version information.

        Returns:
            Dict[str, str]: The Python version information.
        """
        return {
            'version': platform.python_version(),
            'implementation': platform.python_implementation(),
            'compiler': platform.python_compiler(),
        }

    @staticmethod
    def get_django_info() -> Dict[str, str]:
        """
        Get the Django version.

        Returns:
            Dict[str, str]: The Django version.
        """
        return {
            'version': django.get_version(),
        }

    @staticmethod
    def get_disk_usage(path: str = '/') -> Dict[str, Any]:
        """
        Get disk usage information.

        Args:
            path (str): The path to get disk usage information for. Defaults to '/'.

        Returns:
            Dict[str, Any]: The disk usage information.
        """
        try:
            disk_info = psutil.disk_usage(path)
            return {
                'total_gb': round(disk_info.total / BYTES_PER_GB, 2),
                'used_gb': round(disk_info.used / BYTES_PER_GB, 2),
                'free_gb': round(disk_info.percent / BYTES_PER_GB, 2),
                'percent_gb': round(disk_info.percent, 2),
            }
        except Exception as e:
            return {
                'error': str(e)
            }



    @staticmethod
    def get_memory_usage() -> Dict[str, Any]:
        """
        Get memory usage information.

        Returns:
            Dict[str, Any]: The memory usage information.
        """
        try:
            memory_info = psutil.virtual_memory()
            return {
                'total_gb': round(memory_info.total / BYTES_PER_GB, 2),
                'used_gb': round(memory_info.used / BYTES_PER_GB, 2),
                'free_gb': round(memory_info.percent / BYTES_PER_GB, 2),
                'percent_gb': round(memory_info.percent, 2),
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    @staticmethod
    def get_cpu_usage() -> Dict[str, Any]:
        """
        Get CPU usage information.

        Returns:
            Dict[str, Any]: The CPU usage information.
        """
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            return {
                'percent': cpu_percent,
                'count': psutil.cpu_count(),
                'architecture': platform.machine(),
                'processor_type': platform.processor(),
            }
        except Exception as e:
            return {
                'error': str(e)
            }

    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """
        Get system information.

        Returns:
            Dict[str, Any]: The system information.
            """
        return {
			'system': platform.system(),
			'release': platform.release(),
			'version': platform.version(),
			'machine': platform.machine(),
			'node': platform.node(),
		}



