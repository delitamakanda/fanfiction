from django.utils import timezone
from rest_framework import serializers

from chapters.models import Chapter

class ChapterFormattedSerializer(serializers.ModelSerializer):
	status = serializers.CharField(source='get_status_display')
	author = serializers.CharField(source='author.username')
	fanfic = serializers.CharField(source='fanfic.title')

	class Meta:
		model = Chapter
		fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):

	class Meta:
		model = Chapter
		fields = '__all__'

	def create(self, validated_data):
		return Chapter.objects.create(**validated_data)
