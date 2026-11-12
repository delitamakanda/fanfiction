from django.contrib import admin

from apps.posts.models import Post, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["word", "created_at"]
    search_fields = ["word"]
    prepopulated_fields = {"slug": ("word",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "category", "created"]
    list_filter = ["category", "created", "tags"]
    list_select_related = ["user"]
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ["tags"]
