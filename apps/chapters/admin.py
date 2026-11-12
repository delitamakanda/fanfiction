from django.contrib import admin

from apps.chapters.models import Chapter


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "fanfic",
        "author",
        "order",
        "status",
        "published",
        "updated",
    ]
    list_filter = ["status", "published", "created", "updated"]
    list_select_related = ["fanfic", "author"]
    search_fields = ["title", "text", "author__username", "fanfic__title"]
    raw_id_fields = ["author", "fanfic"]
    ordering = ["fanfic", "order"]
