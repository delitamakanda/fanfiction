from rest_framework import serializers
from api.customserializer import TemplateSerializer
from fanfics.models import Fanfic
from chapters.models import Chapter

from chapters.api.serializers import ChapterSerializer

class FanficSerializer(TemplateSerializer):
	genres = serializers.MultipleChoiceField(choices=Fanfic.GENRES_CHOICES)
	classement = serializers.ChoiceField(
		choices=Fanfic.CLASSEMENT_CHOICES)
	status = serializers.ChoiceField(
		choices=Fanfic.STATUS_CHOICES)
	category = serializers.CharField()
	subcategory = serializers.CharField()
	author = serializers.CharField(source='author.username')
	chapters_count = serializers.SerializerMethodField()

	class Meta:
		model = Fanfic
		fields = '__all__'
		lookup_field = 'slug'

	@staticmethod
	def get_chapters_count(obj):
		all_published_chapters = Chapter.objects.filter(
			fanfic=obj, status='publié')
		return len(ChapterSerializer(all_published_chapters, many=True).data)
