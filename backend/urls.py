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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from django.contrib.flatpages.sitemaps import FlatPageSitemap

from backend.sitemaps import FanficSitemap, CategorySitemap, SubCategorySitemap

from markdownx import urls as markdownx

sitemaps = {
	'fanfics': FanficSitemap,
	'categories': CategorySitemap,
    'subcategories': SubCategorySitemap,
	'flatpages': FlatPageSitemap,
}

urlpatterns = [
	path('admin/', admin.site.urls),
	path('api/', include('api.urls')),
	path('docs/', include('backend.docs_urls')),
	path('forum/', include(('forum.urls', 'forum'))),

	path('markdownx/', include(markdownx)),
	path('pages/', include('django.contrib.flatpages.urls')),

	path('offline.html', TemplateView.as_view(template_name="offline.html"), name='offline.html'),
]

urlpatterns += [
	path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,
						  document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL,
						  document_root=settings.STATIC_ROOT)

	# django debug toolbar
	if 'debug_toolbar' in settings.INSTALLED_APPS:
		urlpatterns += [
            path('__debug__/', include('debug_toolbar.urls')),
        ]
