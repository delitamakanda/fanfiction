from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.decorators import action

from apps.core.permissions import IsOwnerOrReadOnly
from apps.forum.api.serializers import (
    BoardSerializer,
    MessageSerializer,
    TopicSerializer,
)
from apps.forum.models import Board, Message, Topic


class BoardViewSet(viewsets.ModelViewSet):
    """Forum boards.

    Anyone can read, authenticated users can create a board, staff can edit or
    delete one. ``GET /boards/{id}/topics/`` lists the topics of a board.
    """

    queryset = Board.objects.order_by("name")
    serializer_class = BoardSerializer

    def get_permissions(self):
        if self.action in {"update", "partial_update", "destroy"}:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    @action(detail=True, methods=["get"])
    def topics(self, request, pk=None):
        topics = self.get_object().topics.order_by("-last_updated")
        page = self.paginate_queryset(topics)
        serializer = TopicSerializer(
            page, many=True, context=self.get_serializer_context()
        )
        return self.get_paginated_response(serializer.data)


class TopicViewSet(viewsets.ModelViewSet):
    """Forum topics. Only the starter can edit or delete a topic.

    ``GET /topics/{id}/messages/`` lists the messages of a topic.
    """

    queryset = Topic.objects.select_related("board", "starter").order_by(
        "-last_updated"
    )
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    owner_field = "starter"
    filterset_fields = ["board"]

    def perform_create(self, serializer):
        serializer.save(starter=self.request.user)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        messages = self.get_object().messages.order_by("created_at")
        page = self.paginate_queryset(messages)
        serializer = MessageSerializer(
            page, many=True, context=self.get_serializer_context()
        )
        return self.get_paginated_response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """Forum messages. Only the author can edit or delete a message."""

    queryset = Message.objects.select_related("topic", "created_by").order_by(
        "created_at"
    )
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    owner_field = "created_by"
    filterset_fields = ["topic"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user, updated_at=timezone.now())
