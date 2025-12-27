from django.urls import path

from fanfics.api.views import (
    GenresViewSet,
    ClassementViewSet,
    StatusViewSet,
    FanficViewSet,
ShareFanficAPIView,
EmailFeedbackView,
UserRecommendationsAPIView,
)

from fanfics.views import (
    fanfic_pdf,
)

from rest_framework import routers

app_name = 'fanfics'

router = routers.DefaultRouter()
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'classement', ClassementViewSet, basename='classement')
router.register(r'status', StatusViewSet, basename='status')
router.register(r'', FanficViewSet, basename='fanfics')

urlpatterns = [
	path('share/', ShareFanficAPIView.as_view(), name='share'),
	path('feedback/', EmailFeedbackView.as_view(), name='feedback'),
	path('recommendations/', UserRecommendationsAPIView.as_view(), name='recommendations'),
]

urlpatterns += [
    path('<int:fanfic_id>/pdf', fanfic_pdf, name='fanfic_pdf'),
]

urlpatterns += router.urls
