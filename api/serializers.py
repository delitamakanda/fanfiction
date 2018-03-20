from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Fanfic
from api.models import Comment
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.models import Post
from api.models import Tag

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'slug',
            'content',
            'created',
            'tags',
        )

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description',)


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='id')

    class Meta:
        model = SubCategory
        fields = ('id', 'category', 'name', 'slug', 'image', 'description',)

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

    class Meta:
        model = Fanfic
        fields = ('id','author','title','slug','synopsis','credits','description','genres','classement','publish','created','updated','was_featured_in_home','status','likes','objects','published','category','subcategory',)


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
        fields = ('id','author','title','slug','synopsis','credits','description','genres','classement','publish','created','updated','was_featured_in_home','status','likes','objects','published','category','subcategory',)


    def create(self, validated_data):
        return Fanfic.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    fanfics = FanficSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'fanfics', 'password', 'email','is_active','is_staff', 'is_superuser', 'date_joined',)
        # read_only_fields = ('username', )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email = validated_data["email"],
            username = validated_data["username"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

      
class PasswordSerializer(serializers.Serializer):
  """
  Serializer for password change endpoint.
  """
  old_password = serializers.CharField(required=True)
  new_password = serializers.CharField(required=True)


class ChapterSerializer(serializers.ModelSerializer):
    # fanfic = serializers.SlugRelatedField(queryset=Fanfic.objects.all(), slug_field='id')

    class Meta:
        model = Chapter
        fields = ('id', 'fanfic', 'title', 'description', 'text', 'order', 'published',)


    def create(self, validated_data):
        return Chapter.objects.create(**validated_data)


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    fanfic = FanficSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'fanfic', 'name', 'email', 'body', 'created', 'active', 'in_reply_to',)


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
