from rest_framework import serializers

from posts.models import Post, Tag

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'word',
            'slug',
            'created_at',
        )


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = serializers.SlugRelatedField(
        many=True, 
        slug_field='word', 
        queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'header',
            'title',
            'slug',
            'content',
            'created',
            'tags',
        )
    
    def to_internal_value(self, data):
        for tag in data.get('tags', []):
            Tag.objects.get_or_create(word=tag)
        return super().to_internal_value(data)


class PostCreateSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, 
        slug_field='word', 
        queryset=Tag.objects.all())

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'header',
            'title',
            'content',
            'created',
            'tags',
        )

    def to_internal_value(self, data):
        for tag in data.get('tags', []):
            Tag.objects.get_or_create(word=tag)
        return super().to_internal_value(data)
