from django.urls import path
from rest_framework import routers

from apps.fanfics.api import views
from apps.fanfics.views import fanfic_pdf

app_name = "fanfics"

router = routers.SimpleRouter()
router.register("genres", views.GenresViewSet, basename="genres")
router.register("classement", views.ClassementViewSet, basename="classement")
router.register("status", views.StatusViewSet, basename="status")
router.register("", views.FanficViewSet, basename="fanfics")

urlpatterns = [
    path("share/", views.ShareFanficAPIView.as_view(), name="share"),
    path("feedback/", views.EmailFeedbackView.as_view(), name="feedback"),
    path(
        "recommendations/",
        views.UserRecommendationsAPIView.as_view(),
        name="recommendations",
    ),
    path("<int:fanfic_id>/pdf", fanfic_pdf, name="fanfic_pdf"),
    *router.urls,
]
