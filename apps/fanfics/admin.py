from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from apps.chapters.models import Chapter
from apps.fanfics.models import Fanfic, Recommendation, UserFavorite


class ChapterInline(admin.StackedInline):
    model = Chapter
    extra = 0
    fields = ("title", "order", "status", "description", "text")


@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "author",
        "status",
        "category",
        "subcategory",
        "created",
        "total_likes",
        "pdf_link",
    ]
    list_filter = ["status", "completed", "created", "updated", "category"]
    list_select_related = ["author", "category", "subcategory"]
    search_fields = ["title", "synopsis", "author__username"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    filter_horizontal = ["users_like"]
    inlines = [ChapterInline]

    @admin.display(description="Export PDF")
    def pdf_link(self, obj):
        if not obj.is_published or obj.fanfic_is_scraped:
            return ""
        url = reverse("api:fanfics:fanfic_pdf", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">PDF</a>', url)


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ["user", "generated_at"]
    list_filter = ["generated_at"]
    search_fields = ["user__username"]
    filter_horizontal = ["fanfictions"]

    def has_module_permission(self, request):
        return request.user.is_superuser


@admin.register(UserFavorite)
class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "fanfiction", "created_at"]
    list_select_related = ["user", "fanfiction"]
    raw_id_fields = ["user", "fanfiction"]
