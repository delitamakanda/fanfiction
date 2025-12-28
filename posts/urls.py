from django.urls import path
from rest_framework.routers import DefaultRouter

from posts.api.views import (
	TagListAPIView, PostViewSet,
)

router = DefaultRouter()

app_name = 'posts'

urlpatterns = [
	path('tags/', TagListAPIView.as_view(), name='tag-list'),
]

router.register('', PostViewSet, basename='post')

urlpatterns += router.urls
