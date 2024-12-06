from django.contrib import admin
from forum.models import Board, Topic, Message

admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Message)
