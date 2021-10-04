from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404

from rest_framework import generics, permissions, filters, status, views
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.reverse import reverse
from rest_framework.response import Response

from fanfics.models import Fanfic

from fanfics.api.serializers import GenresSerializer, FanficSerializer, StatusSerializer, ClassementSerializer, FanficFormattedSerializer

from api import custompermission, recommender

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


class FanficCreateApiView(generics.ListCreateAPIView):
    serializer_class = FanficSerializer
    queryset = Fanfic.objects.all()
    permission_classes = (
        permissions.AllowAny,
        custompermission.IsCurrentAuthorOrReadOnly
    )
    filter_backends = (
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_fields = (
        'category',
        'subcategory',
        'status',
    )
    search_fields = (
        'title',
        'description',
        'synopsis',
    )
    ordering_fields = (
        'title',
        'created',
        'updated',
    )
    ordering = ('-title',)
    name = 'fanfic-create'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FanficSerializer
        return FanficFormattedSerializer

    def get_queryset(self):
        queryset = super(FanficCreateApiView, self).get_queryset()

        try:
            username = self.kwargs['author']
            if username != '':
                queryset = Fanfic.objects.filter(author__username=username)
                return queryset
            return queryset
        except:
            return queryset

    

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        # launch asynchronous tasks
        fanfic_created.delay(serializer.data['id'])


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
            most_viewed_fanfic = Fanfic.objects.filter(
                status='publié').order_by('-views')[0]
            print(most_viewed_fanfic)
            liked_fanfics = r.fanfics_liked([instance, most_viewed_fanfic])

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
