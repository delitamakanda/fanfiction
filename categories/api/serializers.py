from rest_framework import serializers

from categories.models import Category, SubCategory

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='id')

    class Meta:
        model = SubCategory
        fields = '__all__'
