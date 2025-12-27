from rest_framework import serializers
from comments.models import Comment


class CommentNestedSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'body', 'created',
        )
        read_only_fields = ['id', 'author', 'created',]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    in_reply_to = CommentNestedSerializer(read_only=True)
    in_reply_to_id = serializers.IntegerField(write_only=True, required=False)
    fanfic_title = serializers.CharField(source='fanfic.title', read_only=True)
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id', 'author', 'author_id', 'body', 'created', 'updated', 'active',
            'in_reply_to', 'in_reply_to_id', 'fanfic_title', 'chapter_title', 'is_author',
        )
        read_only_fields = ['id', 'author', 'created', 'updated', 'active', 'fanfic_title', 'chapter_title', 'is_author',]

    def get_is_author(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.author == request.user
        return False

    def validate_body(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError('Comment body must be at least 5 characters long')
        if len(value) > 5000:
            raise serializers.ValidationError('Comment body cannot exceed 5000 characters')
        return value.strip()

    def validate_in_reply_to_id(self, value):
        if value:
            try:
                return Comment.objects.get(id=value)
            except Comment.DoesNotExist:
                raise serializers.ValidationError('Invalid reply to comment ID')
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
