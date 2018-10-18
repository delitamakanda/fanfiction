from django.contrib import admin

from django.utils.safestring import mark_safe

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from api.models import Fanfic
from api.models import Chapter
from api.models import Category
from api.models import SubCategory
from api.models import Comment
from api.models import CommentByChapter
from api.models import Post
from api.models import Tag
from api.models import FlatPages
from api.models import FollowStories
from api.models import FollowUser
from api.models import Lexique
from api.models import FoireAuxQuestions
from api.models import AccountProfile
from api.models import Social

from api.models import Board
from api.models import Topic
from api.models import Message

from api.models import Notification

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


@mark_safe
def fanfic_pdf(obj):
    if obj.status == "publié":
        return '<a href="{}" target="_blank">PDF</a>'.format(reverse('fanfic_pdf', args=[obj.id]))
    else:
        return ''

fanfic_pdf.short_description = 'Export PDF'
fanfic_pdf.allow_tags = True

@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'subcategory', 'created', 'total_likes', fanfic_pdf]
    list_filter = ['created', 'updated', 'status']
    search_fields = ['title', 'synopsis']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'fanfic', 'created']
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


class FlatPagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'created']
    search_fields = ['content', 'title']
    list_filter = ['updated', 'type']



@admin.register(FollowStories)
class FollowStoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(FollowUser)
class FollowUserAdmin(admin.ModelAdmin):
    pass


class SocialInline(admin.StackedInline):
    model = Social


class AccountProfileInline(admin.StackedInline):
	model = AccountProfile
	can_delete = False
	verbose_name_plural = 'account profile'


class UserAdmin(BaseUserAdmin):
	inlines = (AccountProfileInline, SocialInline,)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created',)
    list_filter = ('created',)
    search_fields = ('verb',)


admin.site.register(FlatPages, FlatPagesAdmin)
admin.site.register(Lexique)
admin.site.register(FoireAuxQuestions)
admin.site.register(CommentByChapter)
# admin.site.register(AccountProfile, AccountProfileAdmin)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Message)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Notification, NotificationAdmin)
