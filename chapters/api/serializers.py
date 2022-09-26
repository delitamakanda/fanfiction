from django.utils import timezone
from rest_framework import serializers

from chapters.models import Chapter
from fanfics.models import Fanfic

class ChapterFormattedSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Fanfic.STATUS_CHOICES, default='publié')

    class Meta:
        model = Chapter
        fields = (
          'id',
          'author',
          'fanfic',
          'title',
          'description',
          'text',
          'order',
          'status',
          'published',
        )
    
class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = (
          'id',
          'author',
          'fanfic',
          'title',
          'description',
          'text',
          'order',
          'status',
          'published',
        )


    def create(self, validated_data):
        fanfic = validated_data['fanfic']
        status = validated_data['status']
        if status == 'publié':
            fanfic.updated = timezone.now()
            fanfic.save()
        return Chapter.objects.create(**validated_data)

    def save(self, **kwargs):
        kwargs['updated'] = timezone.now()
        return super().save(**kwargs)

    def update(self, instance, validated_data):
        if instance.status == 'publié':
            instance.fanfic.updated = timezone.now()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.text = validated_data.get('text', instance.text)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
