from django.contrib import admin

from posts.models import Post, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['word', 'created_at']
    prepopulated_fields = {'slug': ('word',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created',]
    search_fields = ['created', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ['created', 'tags']
