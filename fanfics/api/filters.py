import django_filters
from fanfics.models import Fanfic

class FanficFilter(django_filters.FilterSet):
    genres = django_filters.CharFilter(field_name='genres', lookup_expr='icontains')
    title = django_filters.CharFilter(field_name='title', lookup_expr='iexact')
    description = django_filters.CharFilter(field_name='description', lookup_expr='iexact')
    synopsis = django_filters.CharFilter(field_name='synopsis', lookup_expr='iexact')

    class Meta:
        model = Fanfic
        fields = ['title', 'description', 'synopsis', 'genres']
