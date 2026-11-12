from django.contrib import admin

from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["fanfic", "author", "created", "active"]
    list_filter = ["active", "created"]
    list_select_related = ["fanfic", "author"]
    search_fields = ["body", "author__username", "fanfic__title"]
    raw_id_fields = ["author", "fanfic", "chapter", "in_reply_to"]
    actions = ["deactivate"]

    @admin.action(description="Masquer les commentaires sélectionnés")
    def deactivate(self, request, queryset):
        queryset.update(active=False)
