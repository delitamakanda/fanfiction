from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from forum.models import Topic, Message, Board
from forum.api.serializers import TopicSerializer, MessageSerializer, BoardSerializer
from rest_framework.decorators import action

class BoardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing forum boards.
    
    Provides CRUD operations for forum boards. Authenticated users can create, update,
    and delete boards. Anonymous users can list and retrieve boards (read-only access).
    
    Endpoints:
        - GET /api/forum/boards/ - List all boards
        - POST /api/forum/boards/ - Create a new board (authentication required)
        - GET /api/forum/boards/{id}/ - Retrieve a specific board
        - PUT /api/forum/boards/{id}/ - Update a board (authentication required)
        - PATCH /api/forum/boards/{id}/ - Partially update a board (authentication required)
        - DELETE /api/forum/boards/{id}/ - Delete a board (authentication required)
        - GET /api/forum/boards/{id}/topics/ - List all topics in a board
    
    Permissions:
        - List/Retrieve: Anyone (including anonymous users)
        - Create/Update/Delete: Authenticated users only
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @action(detail=True, methods=['GET'])
    def topics(self, request, pk=None):
        """
        Retrieve all topics within a specific board.
        
        Args:
            request: The HTTP request object
            pk (int, optional): The primary key of the board
            
        Returns:
            Response: A list of topics belonging to the specified board,
                     serialized using TopicSerializer
        """
        board = self.get_object()
        topics = board.topics.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)


class TopicViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing forum topics.
    
    Provides CRUD operations for forum topics. Authenticated users can create, update,
    and delete topics. Anonymous users can list and retrieve topics (read-only access).
    
    Endpoints:
        - GET /api/forum/topics/ - List all topics
        - POST /api/forum/topics/ - Create a new topic (authentication required)
        - GET /api/forum/topics/{id}/ - Retrieve a specific topic
        - PUT /api/forum/topics/{id}/ - Update a topic (authentication required)
        - PATCH /api/forum/topics/{id}/ - Partially update a topic (authentication required)
        - DELETE /api/forum/topics/{id}/ - Delete a topic (authentication required)
        - GET /api/forum/topics/{id}/messages/ - List all messages in a topic
    
    Permissions:
        - List/Retrieve: Anyone (including anonymous users)
        - Create/Update/Delete: Authenticated users only
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    @action(detail=True, methods=['GET'])
    def messages(self, request, pk=None):
        """
        Retrieve all messages within a specific topic.
        
        Args:
            request: The HTTP request object
            pk (int, optional): The primary key of the topic
            
        Returns:
            Response: A list of messages belonging to the specified topic,
                     serialized using MessageSerializer
        """
        topic = self.get_object()
        messages = topic.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing forum messages.
    
    Provides CRUD operations for forum messages. Authenticated users can create, update,
    and delete messages. Anonymous users can list and retrieve messages (read-only access).
    
    Endpoints:
        - GET /api/forum/messages/ - List all messages
        - POST /api/forum/messages/ - Create a new message (authentication required)
        - GET /api/forum/messages/{id}/ - Retrieve a specific message
        - PUT /api/forum/messages/{id}/ - Update a message (authentication required)
        - PATCH /api/forum/messages/{id}/ - Partially update a message (authentication required)
        - DELETE /api/forum/messages/{id}/ - Delete a message (authentication required)
    
    Permissions:
        - List/Retrieve: Anyone (including anonymous users)
        - Create/Update/Delete: Authenticated users only
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
