from datetime import datetime

from rest_framework import generics, permissions
from rest_framework.response import Response
import platform
import psutil
import django
import socket
import os
from django.utils.timezone import now

START_TIME = datetime.now()


class HealthAPIResponse(generics.ListAPIView):
    name = 'health-api'
    permission_classes = [permissions.AllowAny,]
    queryset = []
    serializer_class = None

    def get(self, request, *args, **kwargs):
        return Response({
            'status': 'ok',
            'timestamp': datetime.now().isoformat()
        })


class SystemAPIView(generics.ListAPIView):
    name = 'system-api'
    permission_classes = [permissions.AllowAny,]
    queryset = []
    serializer_class = None

    def get(self, request, *args, **kwargs):
        uptime = datetime.now() - START_TIME
        disk_info = psutil.disk_usage('/')
        memory_info = psutil.virtual_memory()

        try:
            from django.db import connection
            connection.ensure_connection()
            db_connected = True
            db_engine = connection.settings_dict['ENGINE'].split('.')[-1]
        except (ImportError, AttributeError) as e:
            db_connected = False
            db_engine = None
        except Exception as e:
            db_engine = f"Error: {str(e)}"
            db_connected = False

        return Response({
            "status": "ok",
            "timestamp": datetime.now().isoformat(),
            "uptime_server": str(uptime).split('.')[0],
            "python_version": platform.python_version(),
            "django_version": django.get_version(),
            "disk_usage": {
                "total": f"{disk_info.total // (1024**3)} GB",
                "used": f"{disk_info.used // (1024**3)} GB",
                "free": round(disk_info.percent, 2)
            },
            "memory_usage": {
                "total": f"{memory_info.total // (1024**3)} GB",
                "used": f"{memory_info.used // (1024**3)} GB",
                "free": round(memory_info.percent, 2)
            },
            "database": {
                "engine": db_engine,
                "connected": db_connected
            }
        })

class ApiRootView(generics.GenericAPIView):
    name = 'api-root'
    permission_classes = [permissions.AllowAny,]

    @staticmethod
    def get(self, request, *args, **kwargs):
        return Response({
            'comments': 'http://localhost:8000/api/comments/',
            'categories': 'http://localhost:8000/api/categories/',
            'subcategory': 'http://localhost:8000/api/categories/subcategory/',
            'tags': 'http://localhost:8000/api/posts/tags/',
            'posts': 'http://localhost:8000/api/posts/',
            'genres': 'http://localhost:8000/api/fanfics/genres/',
            'classement': 'http://localhost:8000/api/fanfics/classement/',
            'status': 'http://localhost:8000/api/fanfics/status/',
            'notifications': 'http://localhost:8000/api/notifications/',
            'fanfics': 'http://localhost:8000/api/fanfics/',
        })
