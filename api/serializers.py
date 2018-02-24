from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Fanfic
from api.models import Comment
from api.models import Chapter
from api.models import Category
from api.models import SubCategory

class FanficSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name')
    subcategory = serializers.SlugRelatedField(queryset=SubCategory.objects.all(), slug_field='name')
    genres = serializers.ChoiceField(choices=Fanfic.GENRES_CHOICES, source='get_genres_display')
    classement = serializers.ChoiceField(choices=Fanfic.CLASSEMENT_CHOICES,source='get_classement_display')
    author = serializers.ReadOnlyField(source='author.username')

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

class UserSerializer(serializers.HyperlinkedModelSerializer):
    fanfics = FanficSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'fanfics',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description',)


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'slug', 'image', 'description',)


class ChapterSerializer(serializers.ModelSerializer):
    fanfic = FanficSerializer()
    
    class Meta:
        model = Chapter
        fields = ('id', 'fanfic', 'title', 'description', 'text', 'order',)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    fanfic = FanficSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'fanfic', 'name', 'email', 'body', 'created', 'active', 'in_reply_to',)
