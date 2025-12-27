from rest_framework import serializers
from fanfics.models import Fanfic

class FanficListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fanfic
		fields = [
			'id', 'slug', 'category', 'subcategory', 'title', 'synopsis', 'author', 'total_likes', 'views', 'created',
		]
		read_only_fields = ['id', 'slug', 'total_likes', 'views', 'created', 'category', 'subcategory',]


class FanficDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fanfic
		fields = '__all__'
		read_only_fields = ['id', 'slug', 'total_likes', 'views', 'created', 'updated',]

class FanficCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Fanfic
		fields = ['title', 'synopsis', 'description', 'genres', 'classement', 'category', 'subcategory', 'language', 'picture']
