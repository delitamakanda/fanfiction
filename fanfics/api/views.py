from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from rest_framework import generics, permissions, filters, status
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response

from fanfics.models import Fanfic

from fanfics.api.serializers import GenresSerializer, FanficSerializer, StatusSerializer, ClassementSerializer, FanficFormattedSerializer
from fanfics.api.filters import FanficFilter

from api import custompermission, recommender, custompagination

from api.tasks import fanfic_created


class GenresListView(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = GenresSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name = 'genre-list'


class ClassementListView(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = ClassementSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name = 'classement-list'


class StatusListView(generics.ListAPIView):
    queryset = Fanfic.objects.all()[:1]
    serializer_class = StatusSerializer
    pagination_class = None
    permission_classes = (
        permissions.AllowAny,
    )
    name = 'status-list'


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


class FanficListApiView(generics.ListAPIView):
    serializer_class = FanficFormattedSerializer
    queryset = Fanfic.objects.all()
    filter_class = FanficFilter
    pagination_class = custompagination.StandardResultsSetPagination
    permission_classes = (
        permissions.AllowAny,
    )
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
        'title',
		'id',
        'created',
		'total_likes',
		'views',
        'updated',
	]
    ordering = ['-id']
    name = 'fanfic-list'

    def get_queryset(self):
        queryset = super(FanficListApiView, self).get_queryset()

        try:
            username = self.kwargs['author']
            if username != '':
                queryset = Fanfic.objects.filter(author__username=username)
                return queryset
            return queryset
        except:
            return queryset


class FanficDetailView(generics.RetrieveAPIView):
    throttle_scope = 'fanfic'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Fanfic.objects.all()
    serializer_class = FanficFormattedSerializer
    name = 'fanfic-detail'
    permission_classes = (
        permissions.AllowAny,
    )
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            session_key = 'viewed_fanfic_{}'.format(instance.pk)

            if not self.request.session.get(session_key, False):
                instance.views += 1
                instance.save()
                self.request.session[session_key] = True

            r = recommender.Recommender()
            most_liked_fanfics = Fanfic.objects.filter(
                 status='publié').order_by('-total_likes')[:0]
            print(most_liked_fanfics)
            for most_liked_fanfic in most_liked_fanfics:
                r.fanfics_liked([instance, most_liked_fanfic])

            serializer = self.get_serializer(instance)
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except Http404:
            headers = ""
            response = {"status": "False",
                        "message": "Details not found", "data": ""}
            return Response(response, status=status.HTTP_404_NOT_FOUND, headers=headers)


class FanficUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_scope = 'fanfic'
    throttle_classes = (ScopedRateThrottle,)
    queryset = Fanfic.objects.all()
    serializer_class = FanficSerializer
    name = 'fanfic-update-detail'
    permission_classes = (
        permissions.AllowAny,
        custompermission.IsCurrentAuthorOrReadOnly,
    )
    lookup_field = 'pk'

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
