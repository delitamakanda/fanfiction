from django.core.mail import mail_admins
from django.contrib.auth.models import User

from rest_framework import serializers

from accounts.models import Social, AccountProfile, FollowStories, FollowUser
from fanfics.models import Fanfic

from fanfics.api.serializers import FanficSerializer, UserSerializer, SocialSerializer

from api.customserializer import Base64ImageField

from api.utils import create_notification

class AccountProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    social = serializers.SerializerMethodField()
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
            'social',
        )

    def create(self, validated_data):
        create_notification(validated_data['user'], 'a crée un compte')
        return AccountProfile.objects.create(**validated_data)

    def get_social(self, obj):
        social_acc = Social.objects.filter(user=obj.user)
        serializer = SocialSerializer(social_acc, many=True)
        return serializer.data


class DeleteProfilePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountProfile
        fields = ('photo',)

    def update(self, instance, validated_data):
        #instance.photo = None
        instance.photo.delete()
        instance.save()
        return instance


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
