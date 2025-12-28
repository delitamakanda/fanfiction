from rest_framework import serializers

from forum.models import Board, Topic, Message


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description')


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'subject', 'last_updated', 'views', 'board', 'starter')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'created_at', 'updated_at', 'created_by', 'updated_by', 'topic')
