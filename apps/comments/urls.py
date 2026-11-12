from rest_framework.routers import SimpleRouter

from apps.comments.api.views import CommentViewSet

app_name = "comments"

router = SimpleRouter()
router.register("", CommentViewSet, basename="comments")

urlpatterns = router.urls
