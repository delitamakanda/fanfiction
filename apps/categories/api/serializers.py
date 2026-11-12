from rest_framework import serializers

from apps.categories.models import Category, EntityCategory, SubCategory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug", "description", "logic_value")
        read_only_fields = ("id",)
        extra_kwargs = {"slug": {"required": False}}


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = ("id", "name", "slug", "description", "category", "image")
        read_only_fields = fields


class EntityCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    subcategory = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = EntityCategory
        fields = ("id", "entity", "logic_value", "subcategory", "category")
        read_only_fields = fields
