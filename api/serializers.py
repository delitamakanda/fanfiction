from rest_framework import serializers

from django.utils import timezone
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from rest_framework.fields import CurrentUserDefault

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
from api.models import Notification

from django.contrib.contenttypes.models import ContentType

from api.utils import create_notification
from api.fields import GenericRelatedField
from api.customserializer import Base64ImageField

class FollowUserSerializer(serializers.ModelSerializer):
    # user_to = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

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
    author = UserFanficSerializer(read_only=True)
    # author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
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


class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'date_joined',
        )

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


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
        create_notification(user, 'a créé un compte')
        mail_admins("Account creation", "An user has created an account.")
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Cette e-mail est déja utilisée.')
        return value



class AccountProfileCreateSerializer(serializers.ModelSerializer):
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
        return AccountProfile.objects.create(**validated_data)


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


class DeleteProfilePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = AccountProfile
        fields = ('photo',)

    def update(self, instance, validated_data):
        instance.photo = None
        instance.save()
        return instance


class SocialSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Social
        fields = (
            'id',
            'account',
            'network',
            'nichandle',
            'user',
        )


class SocialCreateSerializer(serializers.ModelSerializer):

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


class ChapterSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Fanfic.STATUS_CHOICES, default='publié')

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
          'status',
          'published',
        )


    def create(self, validated_data):
        fanfic = validated_data['fanfic']
        if fanfic.status == 'publié' and validated_data['status'] == 'publié':
            fanfic.updated = timezone.now()
            fanfic.save()
        return Chapter.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if instance.fanfic.status == 'publié' and instance.status == 'publié':
            instance.fanfic.updated = timezone.now()
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.text = validated_data.get('text', instance.text)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance



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


"""
Serializer for password change endpoint
"""
class ChangePasswordSerializer(serializers.Serializer):


    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
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
    # target = GenericRelatedField(related_models=(Fanfic, User, Chapter))
    user = UserFanficSerializer(read_only=True)
    target = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'verb',
            'target_ct',
            'target_id',
            'target',
            'created',
        )

    def get_target_ct(self, obj):
        return Fanfic.objects.all()
