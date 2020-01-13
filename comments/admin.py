from django.contrib import admin

from comments.models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'fanfic', 'created']
    search_fields = ['created', 'body']
    list_filter = ['created', 'active']
