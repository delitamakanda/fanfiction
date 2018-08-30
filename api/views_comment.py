from django.contrib.auth.models import User
from rest_framework import generics, permissions
from api.models import Comment
from api.models import CommentByChapter
from api.serializers import CommentSerializer
from api.serializers import CommentCreateSerializer
from api.serializers import CommentByChapterSerializer
from api.serializers import CommentByChapterCreateSerializer

class CommentListView(generics.ListAPIView):
    """
    Liste des commentaires
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-list'


class CommentListByFanficView(generics.ListAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-list-by-fanfic'
    pagination_class = None

    def get_queryset(self):
        fanfic = self.kwargs['fanfic']
        return Comment.objects.filter(fanfic=fanfic).order_by('-created')


class CommentCreateView(generics.CreateAPIView):
    """
    Create a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-create'


class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-detail'


"""
Comments by chapter
"""

class CommentByChapterCreateView(generics.CreateAPIView):
    """
    Create a comment by chapter and fanfic
    """
    queryset = CommentByChapter.objects.all()
    serializer_class = CommentByChapterCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-create'


class CommentByChapterListByFanficAndChapterView(generics.ListAPIView):
    """
    List all comments by fanfic and chapter
    """
    serializer_class = CommentByChapterSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-list-by-fanfic-and-chapter'
    pagination_class = None

    def get_queryset(self):
        fanfic = self.kwargs['fanfic']
        chapter = self.kwargs['chapter']
        return CommentByChapter.objects.filter(fanfic=fanfic, chapter=chapter).order_by('-created')
