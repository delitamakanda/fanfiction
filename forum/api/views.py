from rest_framework import viewsets, permissions
from rest_framework.response import Response
from forum.models import Topic, Message, Board
from forum.api.serializers import TopicSerializer, MessageSerializer, BoardSerializer
from rest_framework.decorators import action

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @action(detail=True, methods=['GET'])
    def topics(self, request, pk=None):
        board = self.get_object()
        topics = board.topics.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @action(detail=True, methods=['GET'])
    def messages(self, request, pk=None):
        topic = self.get_object()
        messages = topic.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
