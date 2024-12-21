from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.contrib.contenttypes.models import ContentType
from django.core.mail import mail_admins

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.models import Social, AccountProfile, FollowStories, FollowUser, Notification

from api.customserializer import Base64ImageField

from api.utils import create_notification
from chapters.models import Chapter
from fanfics.api.serializers import FanficSerializer
from fanfics.models import Fanfic

def validate_password_confirmation(password1, password2):
	if password1 != password2:
		raise serializers.ValidationError('Passwords do not match.')
	return password1


class UserSerializer(serializers.ModelSerializer):
	password2 = serializers.CharField(required=True, write_only=True)
	password = serializers.CharField(write_only=True)
	email = serializers.EmailField(
		required=True,
		validators=[
			UniqueValidator(queryset=User.objects.all())
		])
	username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'first_name',
			'last_name',
			'password',
			'email',
			'is_active',
			'is_staff',
			'is_superuser',
			'date_joined',
			'password2',
		)
		extra_kwargs = {'password': {'write_only': True}}
		read_only_fields = ('date_joined',)

	def create(self, validated_data):
		user = User(
			email=validated_data["email"],
			username=validated_data["username"]
		)
		validate_password_confirmation(validated_data["password"], validated_data["password2"])
		user.set_password(validated_data["password"])
		user.save()
		create_notification(user, 'a créé un compte')
		mail_admins("Account creation", "An user has created an account.")
		return user


class AccountProfileSerializer(serializers.ModelSerializer):
	photo = Base64ImageField(max_length=None, use_url=True,
							 allow_empty_file=True, allow_null=True, required=False)
	social_network = serializers.SerializerMethodField()
	user_stories = serializers.SerializerMethodField()
	notifications = serializers.SerializerMethodField()
	user_follows_stories = serializers.SerializerMethodField()
	user_follows_authors = serializers.SerializerMethodField()
	user_favorites_stories = serializers.SerializerMethodField()
	user = UserSerializer(read_only=True)

	class Meta:
		model = AccountProfile
		fields = '__all__'

	def create(self, validated_data):
		create_notification(validated_data['user'], 'a crée un compte')
		return AccountProfile.objects.create(**validated_data)

	@staticmethod
	def get_user_follows_stories(obj):
		follows = FollowStories.objects.filter(from_user=obj.user).all()
		return [FanficSerializer(f.to_fanfic).data for f in follows]

	@staticmethod
	def get_user_follows_authors(obj):
		follows = FollowUser.objects.filter(user_from=obj.user).all()
		return [UserSerializer(f.user_to).data for f in follows]

	@staticmethod
	def get_user_favorites_stories(obj):
		fanfics_liked = Fanfic.objects.filter(users_like=obj.user).all()
		return [FanficSerializer(f).data for f in fanfics_liked]

	@staticmethod
	def get_notifications(obj):
		notifications = Notification.objects.filter(user=obj.user).all()
		return [NotificationSerializer(n).data for n in notifications]

	@staticmethod
	def get_user_stories(obj):
		fanfics = Fanfic.objects.filter(author=obj.user).all()
		stories = [FanficSerializer(f).data for f in fanfics]
		return stories

	@staticmethod
	def get_social_network(obj):
		social = Social.objects.filter(user=obj.user).all()
		if social:
			social_networks = [{'network': s.network, 'nichandle': s.nichandle} for s in social]
			return social_networks
		return None


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

	@staticmethod
	def validate_password2(self, attrs):
		if attrs['password'] != attrs['password2']:
			raise serializers.ValidationError(
				{'password': 'Passwords did not match'})
		return attrs

	@staticmethod
	def validate_email(self, attrs):
		if User.objects.filter(email=attrs).exists():
			raise serializers.ValidationError(
				{'email': 'Email already exists'})
		return attrs

	@staticmethod
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

	@staticmethod
	def validate_username(self, attrs):
		if User.objects.filter(username=attrs).exists():
			raise serializers.ValidationError(
				{'username': 'Username already exists'})
		return attrs


class SocialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Social
		fields = '__all__'

	def create(self, validated_data):
		return Social.objects.create(**validated_data)


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

class ContentTypeSerializer(serializers.ModelSerializer):

	class Meta:
		model = ContentType
		fields = '__all__'


class NotificationObjectRelatedField(serializers.RelatedField):

	def to_representation(self, value):
		if isinstance(value, User):
			return value.username
		elif isinstance(value, Chapter):
			return value.title
		elif isinstance(value, Fanfic):
			return value.title
		raise Exception('Unexpected type of object')


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

	def create(self, validated_data):
		notification = Notification.objects.create(**validated_data)
		notification.save()
		return notification
