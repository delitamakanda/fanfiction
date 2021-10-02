from django.core.mail import mail_admins
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Social, AccountProfile, FollowStories, FollowUser
from fanfics.models import Fanfic

from fanfics.api.serializers import FanficSerializer, UserSerializer, SocialSerializer

from api.customserializer import Base64ImageField

from api.utils import create_notification


class AccountProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    social = serializers.SerializerMethodField(read_only=True)
    # photo =  serializers.ImageField(max_length=None, use_url=True)
    photo = Base64ImageField(max_length=None, use_url=True,
                             allow_empty_file=True, allow_null=True, required=False)

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
            'created',
        )

    def create(self, validated_data):
        create_notification(
            validated_data['user_from'], 'a commencé à suivre', validated_data['user_to'])
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
        create_notification(
            validated_data['from_user'], 'a commencé à suivre', validated_data['to_fanfic'])
        return FollowStories.objects.create(**validated_data)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'password2', 'first_name', 'last_name')
        write_only_fields = ('password',)
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Passwords did not match'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
