from rest_framework import serializers

from comments.models import Comment
from fanfics.api.serializers import FanficSerializer

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
          'id',
          'fanfic',
          'name',
          'email',
          'body',
          'created',
          'active',
          'in_reply_to',
          'chapter',
        )

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)
