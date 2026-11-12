from rest_framework import permissions, viewsets

from apps.comments.api.serializers import CommentSerializer
from apps.comments.models import Comment
from apps.core.choices import PublicationStatus
from apps.core.permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    """Comments of published fanfics. Only the author can edit or delete one."""

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ["fanfic", "chapter"]
    ordering_fields = ["created", "updated"]
    ordering = ["-created"]

    def get_queryset(self):
        return Comment.objects.filter(
            active=True, fanfic__status=PublicationStatus.PUBLISHED
        ).select_related("author", "fanfic", "chapter", "in_reply_to__author")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
