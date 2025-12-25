from datetime import datetime
from typing import Dict, Any

class HealthCheckService:

    @staticmethod
    def get_health_check_results() -> Dict[str, Any]:
        """
        Get the current health check results for the fanfiction-api service.

        Returns:
            Dict[str, Any]: The health check results.
        """
        current_time = datetime.now()
        return {
            'status': 'ok',
            'timestamp': current_time.isoformat(),
            'service': 'fanfiction-api',
            'version': '1.0.0',
        }

    @staticmethod
    def check_database_connection() -> Dict[str, Any]:
        """
        Check the connectivity to the database.

        Returns:
            Dict[str, Any]: The database connection status.
        """
        try:
            from django.db import connection
            connection.ensure_connection()
            db_settings = connection.settings_dict
            return {
                'connected': True,
                'engine': db_settings['ENGINE'].split('.')[-1],
                'name': db_settings.get('NAME', 'Unknown'),
                'host': db_settings.get('HOST', 'localhost'),
            }
        except Exception as e:
            return {
                'connected': False,
                'error': str(e),
                'engine': None,
            }


    @staticmethod
    def check_cache_connection() -> Dict[str, Any]:
        """
        Check the connectivity to the cache.

        Returns:
            Dict[str, Any]: The cache connection status.
        """
        try:
            from django.core.cache import cache
            cache.set('health_check', 'ok', 10)
            result = cache.get('health_check')
            return {
                'connected': result == 'ok',
                'backend': cache.__class__.__name__,
            }
        except Exception as e:
            return {
                'connected': False,
                'error': str(e),
            }
