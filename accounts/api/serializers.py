from django.core.mail import mail_admins
from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import Social, AccountProfile, FollowStories, FollowUser
from fanfics.models import Fanfic

from fanfics.api.serializers import FanficSerializer

from api.customserializer import Base64ImageField

from api.utils import create_notification


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
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        create_notification(user, 'a créé un compte')
        mail_admins("Account creation", "An user has created an account.")
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Cette e-mail est déja utilisée.')
        return value

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class AccountProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # photo =  serializers.ImageField(max_length=None, use_url=True)
    photo =  Base64ImageField(max_length=None, use_url=True, allow_empty_file=True, allow_null=True, required=False)

    class Meta:
        model = AccountProfile
        fields = (
            'id',
            'user',
            'date_of_birth',
            'photo',
            'bio',
        )

    def create(self, validated_data):
        create_notification(validated_data['user'], 'a crée un compte')
        return AccountProfile.objects.create(**validated_data)


class DeleteProfilePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountProfile
        fields = ('photo',)

    def update(self, instance, validated_data):
        #instance.photo = None
        instance.photo.delete()
        instance.save()
        return instance


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


class SocialSignUpSerializer(serializers.ModelSerializer):
    client_id = serializers.SerializerMethodField()
    client_secret = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'username', 'client_id', 'client_secret')
        read_only_fields = ('username',)

    def get_client_id(self, obj):
        return obj.application_set.first().client_id

    def get_client_secret(self, obj):
        return obj.application_set.first().client_secret


class FollowUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowUser
        fields = (
            'id',
            'user_from',
            'user_to',
            'created'
        )

    def create(self, validated_data):
        create_notification(validated_data['user_from'], 'a commencé à suivre', validated_data['user_to'])
        return FollowUser.objects.create(**validated_data)


class FollowStoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowStories
        fields = (
            'id',
            'from_user',
            'to_fanfic',
            'created'
        )

    def create(self, validated_data):
        create_notification(validated_data['from_user'], 'a commencé à suivre', validated_data['to_fanfic'])
        return FollowStories.objects.create(**validated_data)
