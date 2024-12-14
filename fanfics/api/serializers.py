from django.utils import timezone
from django.db import IntegrityError
from django.contrib.auth.models import User

from rest_framework import serializers, fields

from accounts.models import FollowStories, FollowUser, Social
from fanfics.models import Fanfic
from chapters.models import Chapter

from chapters.api.serializers import ChapterSerializer

from django.core.mail import mail_admins
from api.utils import create_notification


class TemplateSerializer(serializers.ModelSerializer):
	def create(self, validated_data):
		try:
			return self.Meta.model.objects.create(**validated_data)
		except IntegrityError as e:
			raise serializers.ValidationError(str(e))


class CustomMultipleChoiceField(fields.MultipleChoiceField):
	def to_representation(self, value):
		return list(super().to_representation(value))


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
	fav_stories = serializers.SerializerMethodField()
	fav_authors = serializers.SerializerMethodField()

	def get_social(self, obj):
		social_acc = Social.objects.filter(user=obj)
		serializer = SocialSerializer(social_acc, many=True)
		return serializer.data

	def get_fav_stories(self, obj):
		favorites_stories = FollowStories.objects.filter(from_user=obj)
		#qs_favorites_stories = favorites_stories.objects.values_list(
			#'to_fanfic')
		fanfics = Fanfic.objects.filter(users__in=favorites_stories)
		serializer = FanficSerializer(fanfics, many=True)
		return serializer.data

	def get_fav_authors(self, obj):
		favorites_authors = FollowUser.objects.filter(user_from=obj)
		#qs_favorites_authors = favorites_authors.objects.values_list(
			#'user_from')
		users = User.objects.filter(rel_to_set__in=favorites_authors)
		serializer = UserSerializer(users, many=True)
		return serializer.data

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


class FanficSerializer(TemplateSerializer):
	genres = serializers.MultipleChoiceField(choices=Fanfic.GENRES_CHOICES)
	classement = serializers.ChoiceField(
		choices=Fanfic.CLASSEMENT_CHOICES)
	status = serializers.ChoiceField(
		choices=Fanfic.STATUS_CHOICES)
	category = serializers.CharField()
	subcategory = serializers.CharField()
	author = serializers.CharField(source='author.username')
	chapters_count = serializers.SerializerMethodField()

	class Meta:
		model = Fanfic
		fields = '__all__'
		lookup_field = 'slug'

	@staticmethod
	def get_chapters_count(obj):
		all_published_chapters = Chapter.objects.filter(
			fanfic=obj, status='publié')
		return len(ChapterSerializer(all_published_chapters, many=True).data)


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

	def validate_email(self, value):
		if User.objects.filter(email=value).exists():
			raise serializers.ValidationError(
				'Cette e-mail est déja utilisée.')
		return value
