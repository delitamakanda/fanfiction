from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.posts.api.views import PostViewSet, TagListAPIView

app_name = "posts"

router = SimpleRouter()
router.register("", PostViewSet, basename="post")

urlpatterns = [
    path("tags/", TagListAPIView.as_view(), name="tag-list"),
    *router.urls,
]
