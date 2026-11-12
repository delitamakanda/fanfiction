from rest_framework import serializers

from apps.forum.models import Board, Message, Topic


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ("id", "name", "description")
        read_only_fields = ("id",)


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ("id", "subject", "last_updated", "views", "board", "starter")
        read_only_fields = ("id", "last_updated", "views", "starter")


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "id",
            "text",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "topic",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        )

    def validate_topic(self, topic):
        if self.instance is not None and topic.pk != self.instance.topic_id:
            raise serializers.ValidationError("A message cannot change topic.")
        return topic
