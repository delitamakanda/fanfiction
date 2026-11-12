from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import (
    AccountProfile,
    FollowStories,
    FollowUser,
    Notification,
    Social,
)

User = get_user_model()


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "verb", "target", "read", "created")
    list_filter = ("read", "created")
    list_select_related = ("user",)
    search_fields = ("verb", "user__username")


@admin.register(FollowStories)
class FollowStoriesAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_fanfic", "created")
    list_select_related = ("from_user", "to_fanfic")
    raw_id_fields = ("from_user", "to_fanfic")


@admin.register(FollowUser)
class FollowUserAdmin(admin.ModelAdmin):
    list_display = ("user_from", "user_to", "created")
    list_select_related = ("user_from", "user_to")
    raw_id_fields = ("user_from", "user_to")


class SocialInline(admin.StackedInline):
    model = Social
    extra = 0


class AccountProfileInline(admin.StackedInline):
    model = AccountProfile
    can_delete = False
    verbose_name_plural = "accounts profiles"


class UserAdmin(BaseUserAdmin):
    inlines = (AccountProfileInline, SocialInline)
    list_filter = (*BaseUserAdmin.list_filter, "accountprofile__reco_consent_given")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
