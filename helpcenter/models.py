import math

from django.db import models
from django.utils.text import Truncator

from django.contrib.auth.models import User

from django.utils.safestring import mark_safe
from django.template.defaultfilters import slugify, pluralize

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


# Create your models here.
"""
Models for html pages
"""

class FoireAuxQuestions(models.Model):
    LIBELLE_CHOICES = (
        ('fan', 'Fanfictions'),
        ('sit', 'Le site'),
    )
    libelle = models.CharField(max_length=3, choices=LIBELLE_CHOICES, default='fan')
    question = models.CharField(max_length=64)
    reponse = MarkdownxField()

    class Meta:
        verbose_name = 'Foire aux questions'
        verbose_name_plural = 'Foires aux questions'

    def __str__(self):
        return '{}: {}'.format(self.libelle, self.question)



"""
Lexique models
"""
class Lexique(models.Model):
    title = models.CharField(max_length=30, db_index=True)
    definition = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


"""
Models for communities views
"""
class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=400)

    def __str__(self):
        return self.name

    def get_messages_count(self):
        return Message.objects.filter(topic__board=self).count()

    def get_last_message(self):
        return Message.objects.filter(topic__board=self).order_by('-created_at').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics', on_delete=models.CASCADE)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def get_page_count(self):
        count = self.messages.count()
        pages = count / 2
        return math.ceil(pages)

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1,5)
        return range(1, count + 1)

    def get_last_ten_messages(self):
        return self.messages.order_by('-created_at')[:10]


class Message(models.Model):
    text = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    updated_by = models.ForeignKey(User, null=True, related_name='+', on_delete=models.CASCADE)

    def __str__(self):
        truncated_text = Truncator(self.text)
        return truncated_text.chars(30)

    def get_text_as_markdownify(self):
        return mark_safe(markdownify(self.text))
