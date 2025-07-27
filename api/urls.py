from django.urls import path

from api.views import (
    ApiRootView,
HealthAPIResponse,
SystemAPIView,
)

urlpatterns = [
	path('', ApiRootView.as_view(), name=ApiRootView.name),
	path('health/', HealthAPIResponse.as_view(), name=HealthAPIResponse.name),
    path('system/', SystemAPIView.as_view(), name=SystemAPIView.name),
]
