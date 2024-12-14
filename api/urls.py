from django.urls import path

from api.views import (
    ApiRootView,
)

urlpatterns = [
	path('', ApiRootView.as_view(), name=ApiRootView.name),
]
