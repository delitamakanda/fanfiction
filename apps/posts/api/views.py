from rest_framework import generics, permissions, viewsets

from apps.core.permissions import IsOwnerOrReadOnly
from apps.posts.api.serializers import PostSerializer, TagSerializer
from apps.posts.models import Post, Tag


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.order_by("word")
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]


class PostViewSet(viewsets.ModelViewSet):
    """Posts (news, tutorials).

    Anyone can read, authenticated users can write a post, and only a staff
    member who wrote a post can edit or delete it.
    """

    serializer_class = PostSerializer
    lookup_field = "slug"
    owner_field = "user"
    filterset_fields = ["user", "title", "category"]
    search_fields = ["title", "content"]
    ordering_fields = ["created"]
    ordering = ["-created"]

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            return [permissions.IsAdminUser(), IsOwnerOrReadOnly()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_queryset(self):
        return Post.objects.select_related("user").prefetch_related("tags")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
