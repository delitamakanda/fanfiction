from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from drf_spectacular.utils import extend_schema, OpenApiResponse


class ApiRootView(generics.GenericAPIView):
	permission_classes = [permissions.AllowAny, ]

	@extend_schema(
		summary="API Root",
		description="This view returns the API root.",
		responses={
			200: OpenApiResponse(
				description="API Root",
			),
		},
		tags=['API']
	)
	def get(self, request, *args, **kwargs):
		return Response({
			'health': reverse('api:health', request=request),
			'health-detailed': reverse('api:health-detailed', request=request),
			'system': reverse('api:system', request=request),
			'documentation': {
				'swagger': reverse('docs:swagger', request=request),
				'redoc': reverse('docs:redoc', request=request),
				'schema': reverse('docs:schema', request=request),
			}
		})
