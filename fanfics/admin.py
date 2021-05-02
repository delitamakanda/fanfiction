from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from fanfics.models import Fanfic
from chapters.models import Chapter

@mark_safe
def fanfic_pdf(obj):
    if obj.status == "publié" and obj.fanfic_is_scraped == False:
        return '<a href="{}" target="_blank">PDF</a>'.format(reverse('helpcenter:fanfic_pdf', args=[obj.id]))
    else:
        return ''

fanfic_pdf.short_description = 'Export PDF'
fanfic_pdf.allow_tags = True

class ChapterInline(admin.StackedInline):
    model = Chapter

@admin.register(Fanfic)
class FanficAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'subcategory', 'created', 'total_likes', fanfic_pdf]
    list_filter = ['created', 'updated', 'status']
    search_fields = ['title', 'synopsis']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ChapterInline, ]
