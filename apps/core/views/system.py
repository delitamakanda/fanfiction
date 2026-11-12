from datetime import datetime

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.core.constants import STATUS
from apps.core.serializers import SystemInfoSerializer
from apps.core.services import HealthCheckService, ServerStatusService


class SystemInfoApiView(generics.GenericAPIView):
    serializer_class = SystemInfoSerializer
    permission_classes = [permissions.IsAdminUser]

    @extend_schema(
        responses={
            200: OpenApiResponse(response=SystemInfoSerializer),
            403: OpenApiResponse(description="Forbidden"),
        },
        tags=["System"],
    )
    def get(self, request, *args, **kwargs):
        system_info = {
            "status": STATUS["UP"],
            "timestamp": datetime.now().isoformat(),
            "uptime_server": ServerStatusService.get_uptime(),
            "python": ServerStatusService.get_python_info(),
            "django": ServerStatusService.get_django_info(),
            "system": ServerStatusService.get_system_info(),
            "disk_usage": ServerStatusService.get_disk_usage(),
            "memory_usage": ServerStatusService.get_memory_usage(),
            "cpu_info": ServerStatusService.get_cpu_usage(),
            "database": HealthCheckService.check_database_connection(),
            "cache": HealthCheckService.check_cache_connection(),
        }
        return Response(self.get_serializer(system_info).data)
