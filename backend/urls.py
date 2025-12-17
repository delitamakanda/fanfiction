"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from sys import api_version

from django.contrib import admin

from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
	SpectacularAPIView,
	SpectacularRedocView,
	SpectacularSwaggerView,
)
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from fanfics.models import Fanfic
from markdownx import urls as markdownx

from rest_framework_simplejwt import views as jwt_views


class FanficSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.5

	def items(self):
		return Fanfic.objects.all()

	@staticmethod
	def lastmod(obj):
		return obj.publish


urlpatterns = [
	path('schema/', SpectacularAPIView.as_view(), name='schema'),
	path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
	path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
]

urlpatterns += [
	path('api/', include(('api.urls', 'api'), namespace='api')),
	path('admin/', admin.site.urls),
	path('api/accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
	path('api/help/', include(('helpcenter.urls', 'helpcenter'), namespace='helpcenter')),
	path('api/posts/', include(('posts.urls', 'posts'), namespace='posts')),
	path('forum/', include(('forum.urls', 'forum'), namespace='forum')),
	path('api/categories/', include(('categories.urls', 'categories'), namespace='categories')),
	path('api/chapters/', include(('chapters.urls', 'chapters'), namespace='chapters')),
	path('api/comments/', include(('comments.urls', 'comments'), namespace='comments')),
	path('api/fanfics/', include(('fanfics.urls', 'fanfics'), namespace='fanfics')),
	path('offline.html', (TemplateView.as_view(template_name="offline.html")), name='offline.html'),
]

urlpatterns += [
	path('sitemap.xml', sitemap, {'sitemaps': {'fanfics': FanficSitemap}}, name='sitemap'),
	path('sitemap2.xml', sitemap, {'sitemaps': {'flatpages': FlatPageSitemap}}, name='sitemap2'),
	path('api/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/refresh-token', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
						  document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL,
						  document_root=settings.STATIC_ROOT)

urlpatterns += [
	path('markdownx/', include(markdownx)),
	path('pages/', include('django.contrib.flatpages.urls')),
]
