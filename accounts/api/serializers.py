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
from fanfics.models import Fanfic


class UserSerializer(serializers.ModelSerializer):

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

	@staticmethod
	def validate_email(value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError(
				'Cette e-mail est déja utilisée.')
		return value


class AccountProfileSerializer(serializers.ModelSerializer):
	photo = Base64ImageField(max_length=None, use_url=True,
							 allow_empty_file=True, allow_null=True, required=False)

	class Meta:
		model = AccountProfile
		fields = '__all__'

	def create(self, validated_data):
		create_notification(validated_data['user'], 'a crée un compte')
		return AccountProfile.objects.create(**validated_data)


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


class SocialSerializer(serializers.ModelSerializer):
	class Meta:
		model = Social
		fields = '__all__'

	def create(self, validated_data):
		return Social.objects.create(**validated_data)


class UserFanficSerializer(serializers.ModelSerializer):
	social = serializers.SerializerMethodField()
	fav_stories = serializers.SerializerMethodField()
	fav_authors = serializers.SerializerMethodField()

	# def get_social(self, obj):
	# 	social_acc = Social.objects.filter(user=obj)
	# 	serializer = SocialSerializer(social_acc, many=True)
	# 	return serializer.data
	#
	# def get_fav_stories(self, obj):
	# 	favorites_stories = FollowStories.objects.filter(from_user=obj)
	# 	#qs_favorites_stories = favorites_stories.objects.values_list(
	# 		#'to_fanfic')
	# 	fanfics = Fanfic.objects.filter(users__in=favorites_stories)
	# 	serializer = FanficSerializer(fanfics, many=True)
	# 	return serializer.data
	#
	# def get_fav_authors(self, obj):
	# 	favorites_authors = FollowUser.objects.filter(user_from=obj)
	# 	#qs_favorites_authors = favorites_authors.objects.values_list(
	# 		#'user_from')
	# 	users = User.objects.filter(rel_to_set__in=favorites_authors)
	# 	serializer = UserSerializer(users, many=True)
	# 	return serializer.data

	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
			'social',
			'fav_authors',
			'fav_stories',
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


class NotificationSerializer(serializers.HyperlinkedModelSerializer):
	user = UserSerializer(read_only=True)
	target = NotificationObjectRelatedField(read_only=True)

	class Meta:
		model = Notification
		fields = '__all__'
