import math
from datetime import datetime, timedelta
from PIL import Image

from django.db import models
from django.conf import settings
from django.utils.text import Truncator

from django.core.validators import URLValidator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.safestring import mark_safe

from markdownx.models import MarkdownxField


class FlatPages(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = MarkdownxField()
    type = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'flat page'
        verbose_name_plural = 'flat pages'

    def __str__(self):
        return '{}'.format(self.title)


class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', db_index=True, on_delete=models.CASCADE)
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
