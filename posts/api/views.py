from rest_framework import generics, permissions

from posts.models import Post, Tag

from posts.api.serializers import PostSerializer, TagSerializer, PostCreateSerializer


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    pagination_class = None
    name = 'tag-list'


class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )
    name='post-create'



class PostUpdate(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (
        permissions.IsAdminUser,
    )
    name='post-update'


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
