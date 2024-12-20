from rest_framework import serializers

from posts.models import Post, Tag

class TagSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tag
		fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
	username_author = serializers.ReadOnlyField(source='user.username')
	email_author = serializers.ReadOnlyField(source='user.email')
	tags = TagSerializer(read_only=True, many=True)

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
		)



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
