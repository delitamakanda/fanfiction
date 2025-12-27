from comments.api.views import (
CommentViewSet,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', CommentViewSet, basename='comments')

app_name = 'comments'

urlpatterns = router.urls
