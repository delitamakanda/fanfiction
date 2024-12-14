from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, filters, status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from fanfics.models import Fanfic

from fanfics.api.serializers import  FanficSerializer
from fanfics.api.filters import FanficFilter

from api import custompermission, recommender, custompagination
from api.recommender import Recommender

from api.tasks import fanfic_created


class TemplateViewSet(ModelViewSet):
	permission_classes = [
		permissions.AllowAny,
	]
	lookup_field = 'id'
	lookup_url_kwarg ='id'
	http_method_names = ['get']


class GenresViewSet(TemplateViewSet):
	def get_queryset(self):
		return [{ 'id': id, 'libelle': libelle } for id, libelle in Fanfic.GENRES_CHOICES]

	def list(self, request):
		return Response({'genres': self.get_queryset()})


class ClassementViewSet(TemplateViewSet):
	def get_queryset(self):
		return [{'id': id, 'libelle': libelle } for id, libelle in Fanfic.CLASSEMENT_CHOICES]

	def list(self, request):
		return Response({'classement': self.get_queryset()})


class StatusViewSet(TemplateViewSet):
	def get_queryset(self):
		return  [{ 'id': id, 'libelle': libelle } for id, libelle in Fanfic.STATUS_CHOICES]

	def list(self, request):
		return Response({'status': self.get_queryset()})


class FanficCreateApiView(generics.CreateAPIView):
	serializer_class = FanficSerializer
	queryset = Fanfic.objects.all()
	permission_classes = (
		custompermission.IsCurrentAuthorOrReadOnly,
	)
	name = 'fanfic-create'

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)
		# launch asynchronous tasks
		fanfic_created.delay(serializer.data['id'])


class FanficViewSet(TemplateViewSet):
	serializer_class = FanficSerializer
	queryset = Fanfic.objects.all()
	filter_class = FanficFilter
	pagination_class = custompagination.StandardResultsSetPagination
	lookup_field = 'slug'
	lookup_url_kwarg = 'slug'
	throttle_scope = 'fanfic'
	throttle_classes = (ScopedRateThrottle,)
	filter_backends = [
		DjangoFilterBackend,
		filters.SearchFilter,
		filters.OrderingFilter,
	]
	search_fields = [
		'title',
		'^description',
		'^synopsis',
		'author__username',
	]
	ordering_fields = [
		'created',
		'total_likes',
		'views',
		'updated',
	]

	def retrieve(self, request, *args, **kwargs):
		instance = self.get_object()
		session_key = 'viewed_fanfic_{}'.format(instance.pk)
		if not self.request.session.get(session_key, False):
			instance.views += 1
			instance.save()
			self.request.session[session_key] = True
		r = recommender.Recommender()
		most_liked_fanfics = Fanfic.objects.filter(
				status='publié').order_by('-total_likes')[:10]
		for most_liked_fanfic in most_liked_fanfics:
			r.fanfics_liked([instance, most_liked_fanfic])


class RecommendedFanficViewSet(TemplateViewSet):
	permission_classes = (permissions.AllowAny,)

	def list(self, request, *args, **kwargs):
		r = Recommender()
		recommended_fanfics = r.suggest_fanfics_for([fanfic for fanfic in Fanfic.objects.filter(status='publié')], 10)

		reco_serializer_data = FanficSerializer(recommended_fanfics, many=True)

		return Response({'recommended_fanfics': reco_serializer_data.data})

