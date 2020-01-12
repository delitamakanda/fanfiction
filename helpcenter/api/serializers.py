from rest_framework import serializers

from helpcenter.models import FoireAuxQuestions, Lexique

class FoireAuxQuestionsSerializer(serializers.ModelSerializer):
    full_libelle = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoireAuxQuestions
        fields = (
            'id',
            'libelle',
            'full_libelle',
            'question',
            'reponse',
        )

    def get_full_libelle(self, obj):
        return obj.get_libelle_display()


class LexiqueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lexique
        fields = (
            'id',
            'title',
            'definition',
            'created',
            'updated',
        )