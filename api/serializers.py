from rest_framework import serializers
from api.models import Fanfic, Comment, Chapter, Category, SubCategory

class FanficSerializer(serializers.ModelSerializer):
    class Meta:
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
        )
