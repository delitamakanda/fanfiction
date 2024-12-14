from rest_framework import generics, permissions, response, status

from chapters.api.serializers import ChapterSerializer, ChapterFormattedSerializer

from chapters.models import Chapter

from api import custompermission, custompagination

from api.tasks import chapter_created

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
        try:
            fanfic = self.kwargs['fanfic']
            if fanfic:
                return Chapter.objects.filter(fanfic=fanfic)
        except:
            return response.Response({'error': 'No fanfic found'}, status=status.HTTP_404_NOT_FOUND)


class ChapterCreateApiView(generics.CreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        chapter_created.delay(serializer.data['id'])


class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    lookup_field = 'id'
    name='chapter-detail'
    permission_classes = (
        custompermission.IsCurrentAuthorOrReadOnly
    )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
