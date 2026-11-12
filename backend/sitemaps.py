"""Sitemaps. Locations point at the Vue front routes or the public API."""

from django.contrib.sitemaps import Sitemap

from apps.categories.models import Category, SubCategory
from apps.fanfics.models import Fanfic


class FanficSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Fanfic.published.order_by("-publish")

    def lastmod(self, obj):
        return obj.updated or obj.publish

    def location(self, obj):
        return f"/fanfics/{obj.slug}/"


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()


class SubCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        return SubCategory.objects.select_related("category")
