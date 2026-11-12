"""Root URL configuration."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from backend.sitemaps import CategorySitemap, FanficSitemap, SubCategorySitemap

sitemaps = {
    "fanfics": FanficSitemap,
    "categories": CategorySitemap,
    "subcategories": SubCategorySitemap,
    "flatpages": FlatPageSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("backend.api_urls", namespace="api")),
    path("docs/", include("backend.docs_urls", namespace="docs")),
    path("markdownx/", include("markdownx.urls")),
    path("pages/", include("django.contrib.flatpages.urls")),
    path(
        "offline.html",
        TemplateView.as_view(template_name="offline.html"),
        name="offline",
    ),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if "debug_toolbar" in settings.INSTALLED_APPS:
        urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
