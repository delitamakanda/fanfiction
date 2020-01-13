from django.utils import timezone

from rest_framework import serializers

from fanfics.models import Fanfic, Genres

from api.recommender import Recommender


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = '__all__'


class FanficSerializer(serializers.ModelSerializer):
    recommended_fanfics = serializers.SerializerMethodField()

    class Meta:
        model = Fanfic
        fields = (
          'id',
          'author',
          'title',
          'slug',
          'synopsis',
          'credits',
          'description',
          'genres',
          'classement',
          'publish',
          'created',
          'updated',
          'was_featured_in_home',
          'status',
          'users_like',
          'total_likes',
          'objects',
          'published',
          'category',
          'subcategory',
          'recommended_fanfics',
          'views',
        )
        lookup_field = 'slug'


    def create(self, validated_data):
        # will only be done if a new object is being created
        validated_data['updated'] = timezone.now()
        return Fanfic.objects.create(**validated_data)

    def save(self, **kwargs):
        # Will be done on every save
        kwargs['updated'] = timezone.now()
        return super().save(**kwargs)

    def update(self, instance, validated_data):
        instance.category = validated_data.get('category', instance.category)
        instance.subcategory = validated_data.get('subcategory', instance.subcategory)
        instance.title = validated_data.get('title', instance.title)
        instance.credits = validated_data.get('credits', instance.credits)
        instance.description = validated_data.get('description', instance.description)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.classement = validated_data.get('classement', instance.classement)
        instance.genres = validated_data.get('genres', instance.genres)
        instance.status = validated_data.get('status', instance.status)
        instance.updated = timezone.now()
        instance.save()
        return instance

    def get_recommended_fanfics(self, obj):
        r = Recommender()
        recommended_fanfics = r.suggest_fanfics_for([obj], 4)
        serializer = FanficSerializer(recommended_fanfics, many=True)
        return serializer.data
