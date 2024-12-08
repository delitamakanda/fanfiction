from django.contrib import admin

from helpcenter.models import Lexique
from helpcenter.models import FoireAuxQuestions

class LexiqueAdmin(admin.ModelAdmin):
	list_display = ['title', 'definition', 'created', 'updated']
	search_fields = ['title', 'definition']
	list_filter = ['created', 'updated']
	prepopulated_fields = {'title': ('title',)}


class FoireAuxQuestionsAdmin(admin.ModelAdmin):
	list_display = ['libelle', 'question', 'reponse']
	search_fields = ['question', 'reponse']
	list_filter = ['libelle']
	prepopulated_fields = {'question': ('question',)}

admin.site.register(Lexique, LexiqueAdmin)
admin.site.register(FoireAuxQuestions, FoireAuxQuestionsAdmin)
