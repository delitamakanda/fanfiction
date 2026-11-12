from django.contrib import admin

from apps.categories.models import Category, EntityCategory, SubCategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "category"]
    list_filter = ["category"]
    list_select_related = ["category"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(EntityCategory)
class EntityCategoryAdmin(admin.ModelAdmin):
    list_display = ["entity", "subcategory"]
    list_select_related = ["subcategory"]
    search_fields = ["entity"]
