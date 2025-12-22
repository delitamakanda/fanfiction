from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path

app_name = 'docs'

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(api_version="v1"), name='schema'),
    path('redoc/', SpectacularRedocView.as_view(url_name='docs:schema'), name='redoc'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='docs:schema'), name='swagger'),
]
