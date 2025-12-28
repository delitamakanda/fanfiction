from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, viewsets, status, filters
from rest_framework.response import Response

from api.custompermission import IsCurrentUserOrReadonly
from posts.models import Post, Tag

from posts.api.serializers import PostSerializer, TagSerializer


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )
    name = 'tag-list'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['user', 'title']
    ordering_fields = ['created']
    ordering = ['-created']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(),]
        elif self.action in ['update', 'partial_update', 'destroy' ]:
            return [permissions.IsAdminUser(), IsCurrentUserOrReadonly(),]
        return [permissions.AllowAny(),]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
