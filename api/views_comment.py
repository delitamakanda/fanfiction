from django.contrib.auth.models import User
from rest_framework import generics, permissions
from api.models import Comment
from api.serializers import CommentSerializer
from api.serializers import CommentCreateSerializer

class CommentList(generics.ListAPIView):
    """
    Liste des commentaires
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-list'


class CommentListByFanfic(generics.ListAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-list-by-fanfic'
    pagination_class = None

    def get_queryset(self):
        fanfic = self.kwargs['fanfic']
        return Comment.objects.filter(fanfic=fanfic)


class CommentCreate(generics.CreateAPIView):
    """
    Create a comment
    """
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-create'


class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-detail'
