from rest_framework import serializers

from categories.models import Category, SubCategory

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
