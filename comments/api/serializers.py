from rest_framework import serializers
from comments.models import Comment

class CommentCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comment
		fields = '__all__'

	def create(self, validated_data):
		return Comment.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.body = validated_data.get('body', instance.body)
		instance.save()
		return instance


class CommentSerializer(serializers.ModelSerializer):
	fanfic = serializers.CharField(source='fanfic.title')
	chapter = serializers.CharField(source='chapter.title')

	class Meta:
		model = Comment
		fields = '__all__'
