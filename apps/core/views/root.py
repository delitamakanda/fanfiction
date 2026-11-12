from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse


class ApiRootView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="API Root",
        responses={200: OpenApiResponse(description="API Root")},
        tags=["API"],
    )
    def get(self, request, *args, **kwargs):
        def url(name):
            return reverse(name, request=request)

        return Response(
            {
                "health": url("api:health"),
                "health-detailed": url("api:health-detailed"),
                "system": url("api:system"),
                "documentation": {
                    "swagger": url("docs:swagger"),
                    "redoc": url("docs:redoc"),
                    "schema": url("docs:schema"),
                },
            }
        )
