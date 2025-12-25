from datetime import datetime

from rest_framework import generics, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.services import HealthCheckService, ServerStatusService
from api.serializers import SystemInfoSerializer
from api.utils.constants import STATUS


class SystemInfoApiView(generics.GenericAPIView):
	serializer_class = SystemInfoSerializer
	permission_classes = [permissions.IsAdminUser, ]

	@extend_schema(
		responses={
			200: OpenApiResponse(
				description="System information response",
				response=SystemInfoSerializer),
			403: OpenApiResponse(
				description="Forbidden",
			)
		},
		tags=['System'],
	)
	def get(self, request, *args, **kwargs):
		system_info = {
			'status': STATUS['UP'],
			'timestamp': datetime.now().isoformat(),
			'uptime_server': ServerStatusService.get_uptime(),
			'python': ServerStatusService.get_python_info(),
			'django': ServerStatusService.get_django_info(),
			'system': ServerStatusService.get_system_info(),
			'disk_usage': ServerStatusService.get_disk_usage(),
			'memory_usage': ServerStatusService.get_memory_usage(),
			'cpu_info': ServerStatusService.get_cpu_usage(),
			'database': HealthCheckService.check_database_connection(),
			'cache': HealthCheckService.check_cache_connection()
		}
		serializer = self.get_serializer(system_info)
		return Response(serializer.data)
