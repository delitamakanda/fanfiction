from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from accounts.models import FollowStories, FollowUser, AccountProfile, Social, Notification


class NotificationAdmin(admin.ModelAdmin):
	list_display = ('user', 'verb', 'target', 'created',)
	list_filter = ('created',)
	search_fields = ('verb',)

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
	verbose_name_plural = 'accounts profiles'
	list_filter = ('reco_consent_given',)


class UserAdmin(BaseUserAdmin):
	inlines = (
		AccountProfileInline,
		SocialInline,
	)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Notification, NotificationAdmin)
