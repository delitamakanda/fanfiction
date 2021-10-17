import django_filters
from rest_framework import filters as drf_filters
from django_filters import rest_framework as df_filters
from django_filters.fields import CSVWidget

from fanfics.models import Fanfic

class MultipleField(MultipleChoiceField):
    def valid_value(self, value):   
        return True

class MultipleFilter(df_filters.MultipleChoiceFilter):
    field_class = MultipleField

class FanficFilter(df_filters.FilterSet):
    #genres = MultipleFilter(lookup_expr="icontains", field_name = "genres", widget=CSVWidget)
	genres = df_filters.MultipleChoiceFilter(
		choices=Fanfic.GENRES_CHOICES,
		action=lambda queryset, value:
			queryset.filter(genres__genres__in=value)
	)
    title = django_filters.CharFilter(field_name='title', lookup_expr='iexact')
    description = django_filters.CharFilter(field_name='description', lookup_expr='iexact')
    synopsis = django_filters.CharFilter(field_name='synopsis', lookup_expr='iexact')

    class Meta:
        model = Fanfic
        fields = ['title', 'description', 'synopsis', 'genres']
