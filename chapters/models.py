from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

from api.fields import OrderField

from fanfics.models import Fanfic

class Chapter(models.Model):
    STATUS_CHOICES = (
        ('brouillon', 'Brouillon'),
        ('publié', 'Publié'),
    )
    author = models.ForeignKey(User, related_name="chapters", on_delete=models.CASCADE, help_text='Author of the chapter')
    fanfic = models.ForeignKey(Fanfic, related_name="chapters", on_delete=models.CASCADE, help_text='Fanfic the chapter belongs to'  )
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default='')
    text = models.TextField()
    order = OrderField(blank=True, for_fields=['fanfic'])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='brouillon', db_index=True)
    published = models.DateTimeField(blank=False, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['order']
        indexes = [
            models.Index(fields=['fanfic', 'status']),
            models.Index(fields=['author', 'status']),
            models.Index(fields=['published']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['order', 'fanfic'], name='unique_chapter_order_per_fanfic', condition=models.Q(order__isnull=False)),
        ]
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

    def __str__(self):
        if self.order:
            return '{}. {}'.format(self.order, self.title)
        return self.title

    def get_absolute_url(self):
        return reverse('chapters:chapter-detail', args=[str(self.id)])

    def clean(self):
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Title cannot be empty'})

        if not self.text or not self.text.strip():
            raise ValidationError({'text': 'Text cannot be empty'})

        if self.status == 'publié' and not self.published:
            raise ValidationError({'published': 'Published date cannot be empty when status is set to Publié'})

        if self.status == 'brouillon' and not self.published:
            raise ValidationError({'published': 'Published date cannot be empty when status is set to Brouillon'})

    def save(self, *args, **kwargs):
        if self.status == 'publié' and not self.published:
            self.published = timezone.now()

        if self.status == 'brouillon' and self.published:
            self.published = None

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == 'publié'

    @property
    def is_draft(self):
        return self.status == 'brouillon'

    def publish(self):
        self.status = 'publié'
        self.save()

    def unpublish(self):
        self.status = 'brouillon'
        self.save()
