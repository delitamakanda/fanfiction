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
