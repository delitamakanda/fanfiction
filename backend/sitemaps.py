from django.contrib.sitemaps import Sitemap
from fanfics.models import Fanfic
from categories.models import Category, SubCategory


class FanficSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Fanfic.objects.filter(status='publié').select_related('category','subcategory').order_by('-publish')

    def lastmod(self, obj):
        return obj.updated if hasattr(obj, 'updated') else obj.publish

    def location(self, obj):
        return f'/fanfics/{obj.slug}/'


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class SubCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.3

    def items(self):
        return SubCategory.objects.select_related('category')

    def location(self, obj):
        return obj.get_absolute_url()
