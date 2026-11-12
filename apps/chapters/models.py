from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone

from apps.core.choices import PublicationStatus
from apps.core.fields import OrderField
from apps.fanfics.models import Fanfic


class ChapterQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=PublicationStatus.PUBLISHED)

    def visible_to(self, user):
        """Published chapters of published fanfics, plus everything ``user`` wrote."""
        public = Q(status=PublicationStatus.PUBLISHED) & Q(
            fanfic__status=PublicationStatus.PUBLISHED
        )
        if user is None or not user.is_authenticated:
            return self.filter(public)
        return self.filter(public | Q(author=user))


class Chapter(models.Model):
    Status = PublicationStatus
    STATUS_CHOICES = PublicationStatus.choices

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="chapters",
        on_delete=models.CASCADE,
        help_text="Author of the chapter",
    )
    fanfic = models.ForeignKey(
        Fanfic,
        related_name="chapters",
        on_delete=models.CASCADE,
        help_text="Fanfic the chapter belongs to",
    )
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default="")
    text = models.TextField()
    order = OrderField(blank=True, for_fields=["fanfic"])
    status = models.CharField(
        max_length=10,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        db_index=True,
    )
    published = models.DateTimeField(blank=True, null=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)

    objects = ChapterQuerySet.as_manager()

    class Meta:
        ordering = ["order"]
        indexes = [
            models.Index(fields=["fanfic", "status"]),
            models.Index(fields=["author", "status"]),
            models.Index(fields=["published"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "fanfic"],
                name="unique_chapter_order_per_fanfic",
                condition=models.Q(order__isnull=False),
            ),
        ]
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        if self.order:
            return f"{self.order}. {self.title}"
        return self.title

    def save(self, *args, **kwargs):
        # The publication date follows the status.
        if self.is_published and not self.published:
            self.published = timezone.now()
        if self.is_draft:
            self.published = None
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("api:chapters:chapter-detail", kwargs={"pk": self.pk})

    def clean(self):
        if not self.title or not self.title.strip():
            raise ValidationError({"title": "Title cannot be empty"})
        if not self.text or not self.text.strip():
            raise ValidationError({"text": "Text cannot be empty"})
        if self.is_published and not self.published:
            raise ValidationError(
                {
                    "published": "Published date cannot be empty when status is set to Publié"
                }
            )
        if self.is_draft and self.published:
            raise ValidationError({"published": "A draft cannot have a published date"})

    @property
    def is_published(self) -> bool:
        return self.status == PublicationStatus.PUBLISHED

    @property
    def is_draft(self) -> bool:
        return self.status == PublicationStatus.DRAFT

    def publish(self):
        self.status = PublicationStatus.PUBLISHED
        self.save()

    def unpublish(self):
        self.status = PublicationStatus.DRAFT
        self.save()
