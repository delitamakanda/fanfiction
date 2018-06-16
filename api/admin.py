from django.contrib import admin
from api.models import Fanfic
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.models import Comment
from api.models import Post
from api.models import Tag
from api.models import StaticPage
from api.models import FollowStories
from api.models import FollowUser

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
    list_display = ['title', 'category', 'subcategory', 'total_likes', 'created']
    list_filter = ['created', 'category', 'subcategory', 'status']
    search_fields = ['title', 'synopsis']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created']
    search_fields = ['created', 'body']
    list_filter = ['created', 'active']


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

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    pass

@admin.register(FollowStories)
class FollowStoriesAdmin(admin.ModelAdmin):
    pass

@admin.register(FollowUser)
class FollowUserAdmin(admin.ModelAdmin):
    pass
