from rest_framework import serializers

from chapters.models import Chapter

class ChapterFormattedSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display', read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)
    fanfic = serializers.CharField(source='fanfic.title', read_only=True)

    class Meta:
        model = Chapter
        fields = [
            'id', 'title', 'description', 'order', 'status', 'author', 'fanfic',
            'created', 'updated', 'published',
        ]
        read_only_fields = ['id', 'created', 'updated', 'author',]


class ChapterSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    fanfic_id = serializers.IntegerField(write_only=True)
    is_published = serializers.BooleanField(read_only=True)

    class Meta:
        model = Chapter
        fields = (
            'id', 'title', 'description', 'text', 'order', 'status', 'author', 'fanfic_id',
            'created', 'updated', 'published', 'is_published',
        )
        read_only_fields = ['id', 'created', 'updated', 'author', 'order', 'is_published',]

        @staticmethod
        def validate_title(value):
            if not value or not value.strip():
                raise serializers.ValidationError('Title is required and cannot be empty')
            return value.strip()

        @staticmethod
        def validate_text(value):
            if not value or not value.strip():
                raise serializers.ValidationError('Text is required and cannot be empty')
            return value.strip()
        @staticmethod
        def validate_status(value):
            valid_statuses = dict(Chapter.STATUS_CHOICES)
            if value not in valid_statuses:
                raise serializers.ValidationError('Invalid status')
            return value

        @staticmethod
        def validate(self, data):
            from fanfics.models import Fanfic
            try:
                fanfic = Fanfic.objects.get(id=data['fanfic_id'])
            except Fanfic.DoesNotExist:
                raise serializers.ValidationError('Fanfic not found')

            if fanfic.author!= self.context['request'].user:
                raise serializers.ValidationError('You are not authorized to create chapters for this fanfic')

            return data

        @staticmethod
        def create(cls, validated_data):
            from fanfics.models import Fanfic
            fanfic = Fanfic.objects.get(id=validated_data.pop('fanfic_id'))
            return Chapter.objects.create(fanfic=fanfic, **validated_data)

        @staticmethod
        def update(instance, validated_data):
            validated_data.pop('fanfic_id', None)
            return super().update(instance, validated_data)

