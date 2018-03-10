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
    genres = serializers.ChoiceField(choices=Fanfic.GENRES_CHOICES, source='get_genres_display')
    classement = serializers.ChoiceField(choices=Fanfic.CLASSEMENT_CHOICES,source='get_classement_display')
    # author = serializers.ReadOnlyField(source='author.username')
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
            'classement',
            'genres',
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
