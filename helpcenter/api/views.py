from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, filters, generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.flatpages.models import FlatPage

from helpcenter.api.serializers import FlatPageSerializer, LexiqueSerializer, FoireAuxQuestionsSerializer

from helpcenter.models import Lexique, FoireAuxQuestions

class FoireAuxQuestionsApiView(ModelViewSet):
	serializer_class = FoireAuxQuestionsSerializer
	permission_classes = (
		permissions.AllowAny,
	)
	queryset = FoireAuxQuestions.objects.all()
	http_method_names = ['get']


class LexiqueApiView(ModelViewSet):
	serializer_class = LexiqueSerializer
	filter_backends = (
		filters.SearchFilter,
		DjangoFilterBackend,
		filters.OrderingFilter,
	)
	permission_classes = (
		permissions.AllowAny,
	)
	ordering_fields = (
		'title',
	)
	search_fields = (
		'definition',
	)
	queryset = Lexique.objects.all()
	http_method_names = ['get']


class FlatPageApiView(ModelViewSet):
	queryset = FlatPage.objects.all()
	serializer_class = FlatPageSerializer
	permission_classes = (
		permissions.AllowAny,
	)
	lookup_field = 'id'
	lookup_url_kwarg ='id'
	http_method_names = ['get']

@method_decorator(xframe_options_exempt, name='dispatch')
class FlatPagesHTMLByIDView(generics.RetrieveAPIView):
	"""docstring for FlatPagesHTMLByIdView."""
	queryset = FlatPage.objects.all()
	renderer_classes = (TemplateHTMLRenderer,)
	serializer_class = FlatPageSerializer

	permission_classes = (
		permissions.AllowAny,
	)
	lookup_field = 'id'
	lookup_url_kwarg ='id'

	def get(self, request, *args, **kwargs):
		self.object = self.get_object()
		return Response({'page': self.object}, template_name='webview/static_pages.html')

