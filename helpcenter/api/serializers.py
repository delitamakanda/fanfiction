from rest_framework import serializers
from django.contrib.flatpages.models import FlatPage

from helpcenter.models import FoireAuxQuestions, Lexique

class FoireAuxQuestionsSerializer(serializers.ModelSerializer):
	libelle = serializers.CharField(source='get_libelle_display')

	class Meta:
		model = FoireAuxQuestions
		fields = '__all__'


class LexiqueSerializer(serializers.ModelSerializer):
	class Meta:
		model = Lexique
		fields = '__all__'


class FlatPageSerializer(serializers.ModelSerializer):
	class Meta:
		model = FlatPage
		fields = '__all__'
