from rest_framework import generics, permissions

from comments.models import Comment

from comments.api.serializers import CommentSerializer


class CommentCreateApiView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    filter_fields = (
        'fanfic',
        'chapter',
        'active',
    )
    ordering_fields = (
        '-created',
    )
    name='comment-create'