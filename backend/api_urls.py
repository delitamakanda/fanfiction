"""API URL hub, mounted under ``/api/`` with the ``api`` namespace.

- ``/api/`` and monitoring endpoints (health checks, system info)
- ``/api/auth/token/`` JWT
- ``/api/v1/<app>/`` resources
- ``/api/forum/`` forum (DRF + server-rendered pages)
"""

from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views

app_name = "api"

auth_patterns = [
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]

v1_patterns = [
    path("help/", include("apps.helpcenter.urls", namespace="helpcenter")),
    path("posts/", include("apps.posts.urls", namespace="posts")),
    path("categories/", include("apps.categories.urls", namespace="categories")),
    path("chapters/", include("apps.chapters.urls", namespace="chapters")),
    path("comments/", include("apps.comments.urls", namespace="comments")),
    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("fanfics/", include("apps.fanfics.urls", namespace="fanfics")),
]

urlpatterns = [
    path("", include("apps.core.urls")),
    path("forum/", include("apps.forum.urls", namespace="forum")),
    path("auth/", include(auth_patterns)),
    path("v1/", include(v1_patterns)),
]
