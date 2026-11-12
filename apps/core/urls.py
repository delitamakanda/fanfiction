from django.urls import path

from apps.core.views import (
    ApiRootView,
    DetailHealthCheckApiView,
    HealthCheckApiView,
    SystemInfoApiView,
)

urlpatterns = [
    path("", ApiRootView.as_view(), name="root"),
    path(
        "health/detailed/", DetailHealthCheckApiView.as_view(), name="health-detailed"
    ),
    path("health/", HealthCheckApiView.as_view(), name="health"),
    path("system/", SystemInfoApiView.as_view(), name="system"),
]
