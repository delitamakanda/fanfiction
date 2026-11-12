from django.contrib import admin

from apps.helpcenter.models import FoireAuxQuestions, Lexique


@admin.register(Lexique)
class LexiqueAdmin(admin.ModelAdmin):
    list_display = ["title", "definition", "created", "updated"]
    search_fields = ["title", "definition"]
    list_filter = ["created", "updated"]


@admin.register(FoireAuxQuestions)
class FoireAuxQuestionsAdmin(admin.ModelAdmin):
    list_display = ["libelle", "question", "order"]
    list_editable = ["order"]
    search_fields = ["question", "reponse"]
    list_filter = ["libelle"]
