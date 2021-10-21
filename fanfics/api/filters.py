import django_filters
from fanfics.models import Fanfic


class FanficFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__slug", lookup_expr="iexact")
    subcategory = django_filters.CharFilter(
        field_name="subcategory__slug", lookup_expr="iexact")
    author = django_filters.CharFilter(
        field_name="author__username", lookup_expr="iexact")
    genres = django_filters.CharFilter(field_name="genres", lookup_expr="icontains")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")

    class Meta:
        model = Fanfic
        fields = ['category', 'subcategory', 'author', 'genres', 'status']
