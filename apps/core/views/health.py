from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.core.constants import STATUS
from apps.core.serializers import HealthCheckSerializer
from apps.core.services import HealthCheckService


class HealthCheckApiView(generics.GenericAPIView):
    serializer_class = HealthCheckSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Get system health status",
        responses={200: OpenApiResponse(response=HealthCheckSerializer)},
        tags=["System"],
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(HealthCheckService.get_health_check_results())
        return Response(serializer.data)


class DetailHealthCheckApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]

    @extend_schema(
        summary="Detailed health status (database, cache)",
        responses={200: OpenApiResponse(description="Detailed health check")},
        tags=["System"],
    )
    def get(self, request, *args, **kwargs):
        database = HealthCheckService.check_database_connection()
        cache = HealthCheckService.check_cache_connection()
        return Response(
            {
                **HealthCheckService.get_health_check_results(),
                "status": STATUS["UP"] if database["connected"] else STATUS["DOWN"],
                "checks": {"database": database, "cache": cache},
            }
        )
