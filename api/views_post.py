from django.utils import timezone

from rest_framework import generics, permissions
from api.models import Post
from api.serializers import PostSerializer
from api import custompermission


"""
Liste des news
"""
class PostList(generics.ListAPIView):
    queryset = Post.objects.order_by('-created').all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    pagination_class = None
    name='post-list'


class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    name='post-detail'
    lookup_field = 'slug'
