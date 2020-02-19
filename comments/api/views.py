from rest_framework import generics, permissions

from comments.models import Comment

from comments.api.serializers import CommentSerializer, CommentCreateSerializer


class CommentCreateApiView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='comment-create'


class CommentListApiView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    pagination_class = None
    filter_fields = (
        'fanfic',
        'chapter',
        'active',
    )
    ordering_fields = (
        '-created',
    )
    name='comment-list'
