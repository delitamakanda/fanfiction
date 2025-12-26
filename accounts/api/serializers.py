from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import mail_admins
from drf_spectacular.utils import extend_schema_field

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Social, AccountProfile, FollowStories, FollowUser, Notification

from api.customserializer import Base64ImageField

from api.utils.notification import create_notification
from chapters.models import Chapter
from fanfics.api.serializers import FanficSerializer
from fanfics.models import Fanfic


def validate_password_confirmation(password1, password2):
    if password1 != password2:
        raise serializers.ValidationError('Passwords do not match.')
    return password1


class NotificationObjectRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, User):
            return value.username
        elif isinstance(value, Chapter):
            return value.title
        elif isinstance(value, Fanfic):
            return value.title
        raise Exception('Unexpected type of object')



class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = '__all__'

    def create(self, validated_data):
        return Social.objects.create(**validated_data)


class AccountProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountProfile
        fields = (
            'id', 'bio', 'photo', 'date_of_birth', 'location',
        )
        read_only_fields = ('id',)

    @staticmethod
    def validate_photo(self, value):
        if value and value.size > (5 * 1024 * 1024):
            raise serializers.ValidationError('Image file too large. Maximum size is 5MB.')
        return value

class UserSerializer(serializers.ModelSerializer):
    profile = AccountProfileSerializer(source='accountprofile', read_only=False, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'date_joined',
            'profile',
        )
        read_only_fields = ('id', 'username', 'email',)
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        user = self.instance
        if User.objects.filter(email=value).exclude(id=user.id).exists():
            raise serializers.ValidationError('Email address already exists.')
        return value

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('accountprofile', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.accountprofile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    target = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'target': {'read_only': True},
        }

class DeleteProfilePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountProfile
        fields = ('photo',)

    def update(self, instance, validated_data):
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

    @staticmethod
    def get_client_id(obj):
        return obj.application_set.first().client_id

    @staticmethod
    def get_client_secret(obj):
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
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'password2',)
        write_only_fields = ('password',)
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True}
        }

    @staticmethod
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Passwords did not match'})
        return data

    @staticmethod
    def validate_username(self, attrs):
        if User.objects.filter(username=attrs).exists():
            raise serializers.ValidationError(
                {'username': 'Username already exists'})

    @staticmethod
    def validate_email(self, attrs):
        if User.objects.filter(email=attrs).exists():
            raise serializers.ValidationError(
                {'email': 'Email already exists'})
        return attrs

    @staticmethod
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserFanficSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
        )


"""
Serializer for password change endpoint
"""


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(value):
        validate_password(value)
        return value


"""
Notification serializer
"""

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ('email',)

    @staticmethod
    def validate_email(value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email does not exist')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        return {'token': token, 'user': user}


class ContactMailSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    message = serializers.CharField(required=True)

    class Meta:
        fields = ('name', 'email','message')
