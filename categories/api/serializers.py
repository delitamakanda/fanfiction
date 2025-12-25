from rest_framework import serializers

from categories.models import Category, SubCategory, EntityCategory

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'slug')


class SubCategorySerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)

	class Meta:
		model = SubCategory
		fields = '__all__'


class EntityCategorySerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)
	subcategory = SubCategorySerializer(read_only=True)

	class Meta:
		model = EntityCategory
		fields = '__all__'
