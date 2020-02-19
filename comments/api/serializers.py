from rest_framework import serializers

from comments.models import Comment
from fanfics.api.serializers import FanficSerializer
from chapters.api.serializers import ChapterSerializer


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
            "id",
            "fanfic",
            "name",
            "email",
            "body",
            "created",
            "active",
            "in_reply_to",
            "chapter",
        )

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    fanfic = FanficSerializer(read_only=True)
    chapter = ChapterSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "fanfic",
            "name",
            "email",
            "body",
            "created",
            "active",
            "in_reply_to",
            "chapter",
        )
