from django.contrib.flatpages.models import FlatPage
from rest_framework import serializers

from apps.helpcenter.models import FoireAuxQuestions, Lexique


class FoireAuxQuestionsSerializer(serializers.ModelSerializer):
    libelle = serializers.CharField(source="get_libelle_display", read_only=True)

    class Meta:
        model = FoireAuxQuestions
        fields = ("id", "libelle", "question", "reponse", "order")
        read_only_fields = fields


class LexiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lexique
        fields = ("id", "title", "definition")
        read_only_fields = fields


class FlatPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlatPage
        fields = ("id", "url", "title", "content")
        read_only_fields = fields
