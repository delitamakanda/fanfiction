from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status, filters
from rest_framework.exceptions import PermissionDenied

from comments.models import Comment
from comments.api.serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fanfic', 'chapter',]
    ordering_fields = ['created', 'updated']
    ordering = ['-created']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('You are not authorized to update this comment.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('You are not authorized to delete this comment.')
        instance.delete()
