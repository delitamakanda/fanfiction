from datetime import datetime

from rest_framework import generics, permissions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from api.services import HealthCheckService
from api.serializers import HealthCheckSerializer
from api.utils.constants import STATUS

class HealthCheckApiView(generics.GenericAPIView):
    serializer_class = HealthCheckSerializer
    permission_classes = [permissions.AllowAny,]

    @extend_schema(
		summary="Get system health status",
		description="This view returns the system health status.",
        responses={
			200: OpenApiResponse(
                description="Health check response",
                response=HealthCheckSerializer),
		},
        tags=['System'],
    )
    def get(self, request, *args, **kwargs):
        health_status = HealthCheckService.get_health_check_results()
        serializer = self.get_serializer(health_status)
        return Response(serializer.data)


class DetailHealthCheckApiView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny,]
    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Detail health check response",)
        },
        tags=['System'],
    )
    def get(self, request, *args, **kwargs):
        health_status = HealthCheckService.get_health_check_results()
        db_status = HealthCheckService.check_database_connection()
        cache_status = HealthCheckService.check_cache_connection()

        status = STATUS['UP']
        if not db_status['connected']:
            status = STATUS['DOWN']

        return Response({
            **health_status,
            'status': status,
            'checks': {
                'database': db_status,
                'cache': cache_status,
            }
        })

