from django.utils import timezone
from django.utils.functional import lazy
from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import FollowStories, FollowUser, Social, AccountProfile
from fanfics.models import Fanfic

from api.recommender import Recommender
from django.core.mail import mail_admins
from api.utils import create_notification


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


class SocialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Social
        fields = (
            'id',
            'account',
            'network',
            'nichandle',
            'user',
        )

    def create(self, validated_data):
        return Social.objects.create(**validated_data)


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
    classement = serializers.ChoiceField(
        choices=Fanfic.CLASSEMENT_CHOICES, default='g')
    status = serializers.ChoiceField(
        choices=Fanfic.STATUS_CHOICES, default='brouillon')

    class Meta:
        model = Fanfic
        fields = (
            'id',
            'author',
            'picture',
            'title',
            'slug',
            'synopsis',
            'language',
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
            'link_fanfic',
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
        instance.subcategory = validated_data.get(
            'subcategory', instance.subcategory)
        instance.title = validated_data.get('title', instance.title)
        instance.credits = validated_data.get('credits', instance.credits)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.synopsis = validated_data.get('synopsis', instance.synopsis)
        instance.classement = validated_data.get(
            'classement', instance.classement)
        instance.genres = validated_data.get('genres', instance.genres)
        instance.status = validated_data.get('status', instance.status)
        instance.updated = timezone.now()
        instance.save()
        return instance


class FanficFormattedSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    subcategory = serializers.CharField()
    genres = serializers.CharField(source='get_genres_display')
    classement = serializers.CharField(source='get_classement_display')
    status = serializers.CharField(source='get_status_display')
    author = UserFanficSerializer(read_only=True)
    # users_like = UserFanficSerializer(read_only=True, many=True)
    recommended_fanfics = serializers.SerializerMethodField()
    most_liked_fanfics = FanficSerializer(many=True, read_only=True)
    newest_fanfics = FanficSerializer(many=True, read_only=True)

    class Meta:
        model = Fanfic
        fields = (
            'id',
            'author',
            'picture',
            'title',
            'slug',
            'synopsis',
            'language',
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
            'newest_fanfics',
            'most_liked_fanfics',
            'views',
            'fanfic_is_scraped',
            'link_fanfic',
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
        recommended_fanfics = r.suggest_fanfics_for([obj], 10)
        serializer = FanficSerializer(recommended_fanfics, many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    fanfics = FanficSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'fanfics',
            'password',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        create_notification(user, 'a créé un compte')
        mail_admins("Account creation", "An user has created an account.")
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Cette e-mail est déja utilisée.')
        return value
