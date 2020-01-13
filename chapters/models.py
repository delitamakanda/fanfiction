from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from api.fields import OrderField

from fanfics.models import Fanfic

class Chapter(models.Model):
    STATUS_CHOICES = (
        ('brouillon', 'Brouillon'),
        ('publié', 'Publié'),
    )
    author = models.ForeignKey(User, related_name="chapter", on_delete=models.CASCADE)
    fanfic = models.ForeignKey(Fanfic, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default='')
    text = models.TextField()
    order = OrderField(blank=True, for_fields=['fanfic'])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='publié')
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)
