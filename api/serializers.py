from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Fanfic
from api.models import Comment
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.models import Post

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'slug',
            'content',
            'created',
        )

class FanficSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    subcategory = serializers.SlugRelatedField(queryset=SubCategory.objects.all(), slug_field='name')
    genres = serializers.ChoiceField(choices=Fanfic.GENRES_CHOICES, default='Général', source='get_genres_display')
    classement = serializers.ChoiceField(choices=Fanfic.CLASSEMENT_CHOICES, default='G', source='get_classement_display')
    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

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
            'likes',
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
        fields = ('id', 'username', 'fanfics', 'password', 'email',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description',)


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='id')

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'slug', 'image', 'description',)


class ChapterSerializer(serializers.ModelSerializer):
    fanfic = serializers.SlugRelatedField(queryset=Fanfic.objects.all(), slug_field='id')

    class Meta:
        model = Chapter
        fields = ('id', 'fanfic', 'title', 'description', 'text', 'order',)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    fanfic = FanficSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'fanfic', 'name', 'email', 'body', 'created', 'active', 'in_reply_to',)


"""
SerializerMethodField for request model options
"""
class OptionsSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()
    classement = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_genres(self, obj):
        return Fanfic.GENRES_CHOICES

    def get_classement(self, obj):
        return Fanfic.CLASSEMENT_CHOICES

    def get_status(self, obj):
        return Fanfic.STATUS_CHOICES

    class Meta:
        model = Fanfic
        fields = ('genres', 'classement', 'status',)
