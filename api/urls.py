from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from api.views import (
	ApiRootView,
	DetailHealthCheckApiView,
	SystemInfoApiView,
	HealthCheckApiView
)

app_name = 'api'

monitoring_patterns = [
	path('health/detailed/', DetailHealthCheckApiView.as_view(), name='health-detailed'),
	path('health/', HealthCheckApiView.as_view(), name='health'),
	path('system/', SystemInfoApiView.as_view(), name='system'),
]

auth_patterns = [
	path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

resources_patterns = [
	path('help/', include(('helpcenter.urls', 'helpcenter'), namespace='helpcenter')),
	path('posts/', include(('posts.urls', 'posts'), namespace='posts')),
	path('categories/', include(('categories.urls', 'categories'), namespace='categories')),
	path('chapters/', include(('chapters.urls', 'chapters'), namespace='chapters')),
	path('comments/', include(('comments.urls', 'comments'), namespace='comments')),
	path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
	path('fanfics/', include(('fanfics.urls', 'fanfics'), namespace='fanfics')),
]

forum_patterns = [
	path('forum/', include(('forum.urls', 'forum'))),
]

urlpatterns = [
	path('', ApiRootView.as_view(), name='root'),
	path('', include(monitoring_patterns)),
	path('', include(forum_patterns)),
	path('auth/', include(auth_patterns)),
	path('v1/', include(resources_patterns)),
]
