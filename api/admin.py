from django.contrib import admin
from api.models import Fanfic, Chapter, Category, SubCategory, Comment, Post

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ChapterInline(admin.StackedInline):
    model = Chapter


@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created']
    list_filter = ['created', 'category']
    search_fields = ['title', 'synopsis']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created']
    search_fields = ['created', 'body']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'created']
    search_fields = ['created', 'content']
    prepopulated_fields = {'slug': ('title',)}
