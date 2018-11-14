from django.contrib import admin

from helpcenter.models import Lexique
from helpcenter.models import FoireAuxQuestions
from helpcenter.models import Board
from helpcenter.models import Topic
from helpcenter.models import Message

# Register your models here.

admin.site.register(Lexique)
admin.site.register(FoireAuxQuestions)
admin.site.register(Board)
admin.site.register(Topic)
admin.site.register(Message)
