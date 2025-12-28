from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from fanfics.models import Fanfic, Recommendation
from chapters.models import Chapter

@mark_safe
def fanfic_view_pdf(obj):
    if obj.status == "publié" and obj.fanfic_is_scraped == False:
        return '<a href="{}" target="_blank">PDF</a>'.format(reverse('api:fanfics:fanfic_pdf', args=[obj.id]))
    else:
        return ''

fanfic_view_pdf.short_description = 'Export PDF'
fanfic_view_pdf.allow_tags = True

class ChapterInline(admin.StackedInline):
    model = Chapter

@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'subcategory', 'created', 'total_likes', fanfic_view_pdf]
    list_filter = ['created', 'updated', 'status']
    search_fields = ['title', 'synopsis']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline, ]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'generated_at']
    list_filter = ('generated_at',)
    search_fields = ('user__username',)
    filter_horizontal = ('fanfictions',)

    def has_module_permission(self, request):
        return request.user.is_superuser
