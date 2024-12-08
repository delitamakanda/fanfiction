from django.contrib import admin
from chapters.models import Chapter

class ChapterAdmin(admin.ModelAdmin):
	list_display = ['title', 'fanfic', 'author', 'status', 'published', 'created', 'updated']
	search_fields = ['title', 'text', 'author__username', 'fanfic__title']
	list_filter = ['status', 'published', 'created', 'updated']
	prepopulated_fields = {'title': ('title',)}
	ordering = ['fanfic', 'order']

admin.site.register(Chapter, ChapterAdmin)
