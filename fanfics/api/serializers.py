from django.utils import timezone
from django.utils.functional import lazy
from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import Social, AccountProfile, FollowStories, FollowUser
from fanfics.models import Fanfic

from api.recommender import Recommender


class GenresSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Fanfic
        fields = ('genres',)

    def get_genres(self, obj):
        return Fanfic.GENRES_CHOICES


class ClassementSerializer(serializers.ModelSerializer):
    classement = serializers.SerializerMethodField()

    class Meta:
        model = Fanfic
        fields = ('classement',)

    def get_classement(self, obj):
        return Fanfic.CLASSEMENT_CHOICES


class StatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Fanfic
        fields = ('status',)

    def get_status(self, obj):
        return Fanfic.STATUS_CHOICES


class UserFanficSerializer(serializers.ModelSerializer):
    social = serializers.SerializerMethodField()
    fanfics = serializers.SerializerMethodField()
    stories = serializers.SerializerMethodField()
    authors = serializers.SerializerMethodField()

    def get_social(self, obj):
        social_acc = Social.objects.filter(user=obj)
        serializer = SocialSerializer(social_acc, many=True)
        return serializer.data

    def get_fanfics(self, obj):
        fanfics = Fanfic.objects.filter(author=obj)
        serializer = FanficSerializer(fanfics, many=True)
        return serializer.data

    def get_stories(self, obj):
        stories = FollowStories.objects.filter(from_user=obj)
        serializer = FanficSerializer(stories, many=True)
        return serializer.data

    def get_authors(self, obj):
        authors = FollowUser.objects.filter(user_from=obj)
        serializer = UserSerializer(authors, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = (
          'id',
          'username',
          'email',
          'social',
          'fanfics',
          'authors',
          'stories',
        )


class FanficSerializer(serializers.ModelSerializer):
    genres = serializers.MultipleChoiceField(choices=Fanfic.GENRES_CHOICES)
    classement = serializers.ChoiceField(choices=Fanfic.CLASSEMENT_CHOICES, default='g')
    status = serializers.ChoiceField(choices=Fanfic.STATUS_CHOICES, default='brouillon')

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
          'views',
          'fanfic_is_scraped',
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


class FanficFormattedSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    subcategory = serializers.CharField()
    genres = serializers.CharField()
    classement = serializers.CharField(source='get_classement_display')
    status = serializers.CharField(source='get_status_display')
    #author = UserFanficSerializer(read_only=True)
    #users_like = UserFanficSerializer(read_only=True, many=True)
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
          'fanfic_is_scraped',
        )
        lookup_field = 'slug'


    def get_genres(self, obj):
        return obj.get_genres_display()

    def get_classement(self, obj):
        return obj.get_classement_display()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_recommended_fanfics(self, obj):
        r = Recommender()
        recommended_fanfics = r.suggest_fanfics_for([obj], 6)
        serializer = FanficSerializer(recommended_fanfics, many=True)
        return serializer.data
