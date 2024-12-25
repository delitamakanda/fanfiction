from django.urls import path

from fanfics.api.views import (
    GenresViewSet,
    ClassementViewSet,
    StatusViewSet,
    FanficCreateApiView,
    FanficViewSet,
RecommendedFanficViewSet,
ShareFanficAPIView,
EmailFeedbackView,
)

from fanfics.views import fanfic_detail
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'genres', GenresViewSet, basename='genres'),
router.register(r'classement', ClassementViewSet, basename='classement')
router.register(r'status', StatusViewSet, basename='status')
router.register(r'', FanficViewSet, basename='fanfics')
router.register(r'recommended/list', RecommendedFanficViewSet, basename='recommended')

urlpatterns = [
    path('fanfics-create/', FanficCreateApiView.as_view(), name='fanfic-create'),
	path('share/', ShareFanficAPIView.as_view(), name='share'),
	path('feedback/', EmailFeedbackView.as_view(), name='feedback'),
]

urlpatterns += router.urls
