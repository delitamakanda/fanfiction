from django.contrib import admin

from apps.forum.models import Board, Message, Topic


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    search_fields = ["name"]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["subject", "board", "starter", "views", "last_updated"]
    list_filter = ["board"]
    list_select_related = ["board", "starter"]
    search_fields = ["subject"]
    raw_id_fields = ["starter"]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["__str__", "topic", "created_by", "created_at"]
    list_select_related = ["topic", "created_by"]
    search_fields = ["text"]
    raw_id_fields = ["created_by", "updated_by", "topic"]
