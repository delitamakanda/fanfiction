from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from api.views import (
    ApiRootView,
HealthAPIResponse,
SystemAPIView,
)

app_name = 'api'

urlpatterns = [
	# authentication
	path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

	path('v1/', include([
		path('accounts/', include(('accounts.urls', 'accounts'))),
		path('fanfics/', include(('fanfics.urls', 'fanfics'))),
	])),

	path('', include([
		path('help/', include(('helpcenter.urls', 'helpcenter'))),
		path('posts/', include(('posts.urls', 'posts'))),
		path('categories/', include(('categories.urls', 'categories'))),
		path('chapters/', include(('chapters.urls', 'chapters'))),
		path('comments/', include(('comments.urls', 'comments'))),
	])),

	# path('', ApiRootView.as_view(), name=ApiRootView.name),
	path('health/', HealthAPIResponse.as_view(), name=HealthAPIResponse.name),
    path('system/', SystemAPIView.as_view(), name=SystemAPIView.name),
]
