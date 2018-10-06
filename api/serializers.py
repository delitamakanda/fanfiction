from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from api.models import Fanfic
from api.models import Comment
from api.models import CommentByChapter
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.models import Post
from api.models import Tag
from api.models import FlatPages
from api.models import FollowStories
from api.models import FollowUser
from api.models import AccountProfile
from api.models import Social


class FollowUserSerializer(serializers.ModelSerializer):
    user_to = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = FollowUser
        fields = (
            'id',
            'user_from',
            'user_to',
            'created'
        )


class FollowStoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FollowStories
        fields = (
            'id',
            'from_user',
            'to_fanfic',
            'created'
        )



class FlatPagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = FlatPages
        fields = (
            'id',
            'title',
            'content',
            'type',
            'created',
            'updated'
        )




class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = (
            'id',
            'word',
            'slug',
            'created_at',
        )


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'header',
            'title',
            'slug',
            'content',
            'created',
            'tags',
        )
        lookup_field = 'slug'

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = (
          'id',
          'name',
          'slug',
          'description',
          'logic_value',
        )


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='id')

    class Meta:
        model = SubCategory
        fields = (
          'id',
          'category',
          'name',
          'slug',
          'image',
          'description',
        )

"""
Display list of users who liked the fanfic
"""
class UserFanficSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
          'id',
          'username',
        )


"""
Serializer for GET method
"""

class FanficListSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    subcategory = serializers.CharField()
    genres = serializers.CharField()
    classement = serializers.CharField(source='get_classement_display')
    status = serializers.CharField(source='get_status_display')
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    users_like = UserFanficSerializer(read_only=True, many=True)

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
        )
        lookup_field = 'slug'


    def get_genres(self, obj):
        return obj.get_genres_display()

    def get_classement(self, obj):
        return obj.get_classement_display()

    def get_status(self, obj):
        return obj.get_status_display()

"""
Serializer for PUT/POST/DELETE method
"""

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
        )


    def create(self, validated_data):
        return Fanfic.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    fanfics = FanficSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
          'id',
          'username',
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
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Cette e-mail est déja utilisée.')
        return value


class AccountProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

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
        return AccountProfile.objects.create(**validated_data)


class SocialSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Social
        fields = (
            'id',
            'account',
            'network',
            'nichandle',
            'user',
        )



class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = (
          'id',
          'author',
          'fanfic',
          'title',
          'description',
          'text',
          'order',
          'published',
        )


    def create(self, validated_data):
        return Chapter.objects.create(**validated_data)


class SectionCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
          'id',
          'fanfic',
          'name',
          'email',
          'body',
          'created',
          'active',
          'in_reply_to',
        )


class CommentSerializer(serializers.ModelSerializer):
    fanfic = FanficSerializer()
    in_reply_to = SectionCommentSerializer()

    class Meta:
        model = Comment
        fields = (
          'id',
          'fanfic',
          'name',
          'email',
          'body',
          'created',
          'active',
          'in_reply_to',
        )


class CommentByChapterSerializer(serializers.ModelSerializer):
    fanfic = FanficSerializer()
    chapter = ChapterSerializer()
    in_reply_to = SectionCommentSerializer()

    class Meta:
        model = CommentByChapter
        fields = (
            'id',
            'fanfic',
            'chapter',
            'name',
            'email',
            'body',
            'created',
            'active',
            'in_reply_to',
        )


class CommentByChapterCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentByChapter
        fields = (
            'id',
            'fanfic',
            'chapter',
            'name',
            'email',
            'body',
            'created',
            'active',
            'in_reply_to',
        )


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = (
          'id',
          'fanfic',
          'name',
          'email',
          'body',
          'created',
          'active',
          'in_reply_to',
        )


"""
SerializerMethodField for request model options
"""

class GenresSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    def get_genres(self, obj):
        return Fanfic.GENRES_CHOICES

    class Meta:
        model = Fanfic
        fields = ('genres',)


class ClassementSerializer(serializers.ModelSerializer):
    classement = serializers.SerializerMethodField()

    def get_classement(self, obj):
        return Fanfic.CLASSEMENT_CHOICES

    class Meta:
        model = Fanfic
        fields = ('classement',)


class StatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return Fanfic.STATUS_CHOICES

    class Meta:
        model = Fanfic
        fields = ('status',)


"""
Serializer for password change endpoint
"""
class ChangePasswordSerializer(serializers.Serializer):


    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value
