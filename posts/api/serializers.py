from rest_framework import serializers

from posts.models import Post, Tag

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = ('word',)
		read_only_fields = ('id', 'created_at',)


class PostSerializer(serializers.ModelSerializer):
	username_author = serializers.CharField(source='user.username', read_only=True)
	email_author = serializers.CharField(source='user.email', read_only=True)
	tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='word')

	class Meta:
		model = Post
		fields = (
			'id',
			'username_author',
			'email_author',
			'header',
			'title',
			'slug',
			'content',
			'created',
			'tags',
			'category',
		)

	def to_internal_value(self, data):
		for tag in data.get('tags', []):
			Tag.objects.get_or_create(word=tag)
		return super().to_internal_value(data)

