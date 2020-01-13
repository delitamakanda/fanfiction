from rest_framework import generics, permissions

from chapters.api.serializers import ChapterSerializer

from chapters.models import Chapter

from api import custompermission

from api.tasks import chapter_created

class ChapterCreateApiView(generics.ListCreateAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-create'
    permission_classes = (
        permissions.AllowAny,
        custompermission.IsCurrentAuthorOrReadOnly
    )
    filter_fields = (
        'status',
    )
    pagination_class = None

    def get_queryset(self):
        try:
            fanfic = self.kwargs['fanfic']
            if fanfic:
                return Chapter.objects.filter(fanfic=fanfic)
        except:
            fanfic = None
            return Chapter.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        chapter_created.delay(serializer.data['id'])


class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
    name='chapter-detail'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentAuthorOrReadOnly
    )

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
