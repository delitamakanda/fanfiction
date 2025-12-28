from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.throttling import UserRateThrottle

from chapters.api.serializers import ChapterSerializer, ChapterFormattedSerializer

from chapters.models import Chapter

from api import custompagination

import logging

logger = logging.getLogger(__name__)


class ChapterBaseAPIView(generics.GenericAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create_or_update(self, serializer):
        serializer.save(author=self.request.user)


class ChapterListApiView(generics.ListAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterFormattedSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    pagination_class = custompagination.StandardResultsSetPagination
    filter_fields = (
        'status',
    )

    def get_queryset(self):
        fanfic_id = self.request.query_params.get('fanfic', None)
        if fanfic_id is None:
            raise NotFound('No fanfic id provided')
        return Chapter.objects.filter(fanfic=fanfic_id)


class ChapterCreateApiView(ChapterBaseAPIView, generics.CreateAPIView):
    throttle_classes = [UserRateThrottle,]
    def perform_create(self, serializer):
        self.perform_create_or_update(serializer)




class ChapterDetailView(ChapterBaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'
    name = 'chapter-detail'

    def get_queryset(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Chapter.objects.filter(author=self.request.user)
        return Chapter.objects.all()

    def perform_update(self, serializer):
        instance = serializer.save(author=self.request.user)
        instance.full_clean()
        self.perform_create_or_update(serializer)
