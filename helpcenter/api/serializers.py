from rest_framework import serializers
from django.contrib.flatpages.models import FlatPage

from helpcenter.models import FoireAuxQuestions, Lexique

class FoireAuxQuestionsSerializer(serializers.ModelSerializer):
	libelle = serializers.CharField(source='get_libelle_display')

	class Meta:
		model = FoireAuxQuestions
		fields = ('id', 'libelle', 'question', 'order',)
		read_only_fields = ('id',)


class LexiqueSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lexique
		fields = ('id', 'title', 'definition',)
		read_only_fields = ('id',)


class FlatPageSerializer(serializers.ModelSerializer):
	class Meta:
		model = FlatPage
		fields = ('id', 'url', 'title', 'content')
		read_only_fields = ('id', 'url',)
