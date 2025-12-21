from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path
from rest_framework import permissions


class PublicSpectacularAPIView(SpectacularAPIView):
    permission_classes = (permissions.AllowAny,)

app_name = 'docs'

urlpatterns = [
    path('schema/', PublicSpectacularAPIView.as_view(), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='docs:schema'), name='redoc'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='docs:schema'), name='swagger'),
]
