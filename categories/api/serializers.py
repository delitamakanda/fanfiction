from rest_framework import serializers

from categories.models import Category, SubCategory, EntityCategory

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ('id', 'name', 'slug', 'description',)


class SubCategorySerializer(serializers.ModelSerializer):
	category = CategorySerializer(read_only=True)

	class Meta:
		model = SubCategory
		fields = (
			'id', 'name','slug', 'description', 'category', 'image',
		)


class EntityCategorySerializer(serializers.ModelSerializer):
	category = serializers.StringRelatedField(read_only=True)
	subcategory = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = EntityCategory
		fields = (
			'id', 'entity', 'logic_value', 'subcategory', 'category',
		)
