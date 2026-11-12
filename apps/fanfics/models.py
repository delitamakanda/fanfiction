from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from multiselectfield import MultiSelectField

from apps.categories.models import Category, SubCategory
from apps.core.choices import PublicationStatus


class FanficQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=PublicationStatus.PUBLISHED)

    def visible_to(self, user):
        """Published fanfics, plus the drafts of ``user``."""
        if user is None or not user.is_authenticated:
            return self.published()
        return self.filter(Q(status=PublicationStatus.PUBLISHED) | Q(author=user))

    def with_related(self):
        return self.select_related("author", "category", "subcategory")


class PublishedManager(models.Manager.from_queryset(FanficQuerySet)):
    def get_queryset(self):
        return super().get_queryset().published()


class Fanfic(models.Model):
    Status = PublicationStatus

    GENRES_CHOICES = (
        ("RO", "Romance"),
        ("SU", "Surnaturel"),
        ("ER", "Erotique"),
        ("DR", "Drame"),
        ("AM", "Amitié"),
        ("AC", "Action-Aventure"),
        ("SC", "School-Fic"),
        ("MY", "Mystère"),
        ("GE", "Général"),
        ("DCED", "De cape et d'épée"),
        ("LE", "Lemon"),
        ("HU", "Humour"),
        ("OS", "One-Shot"),
        ("SUS", "Suspense"),
        ("TH", "Thriller"),
        ("HO", "Horreur"),
        ("HF", "Heroic Fantasy"),
        ("TR", "Tragédie"),
        ("CO", "Cross-Over"),
    )
    STATUS_CHOICES = PublicationStatus.choices
    CLASSEMENT_CHOICES = (
        ("g", "G"),
        ("13", "13+"),
        ("r", "R"),
        ("18", "18+"),
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="fanfics",
        on_delete=models.CASCADE,
        db_index=True,
    )
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(
        max_length=255, db_index=True, unique=True, blank=True, null=True
    )
    synopsis = models.CharField(max_length=1000, blank=True, default="")
    credits = models.CharField(max_length=255, blank=True, default="")
    picture = models.CharField(max_length=1000, blank=True, null=True)
    language = models.CharField(max_length=2, default="fr")
    description = models.CharField(max_length=1000, blank=True, default="")
    classement = models.CharField(max_length=2, choices=CLASSEMENT_CHOICES, default="g")
    genres = MultiSelectField(choices=GENRES_CHOICES, max_length=4)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    was_featured_in_home = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
        db_index=True,
    )
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="fanfics_liked", blank=True
    )
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    category = models.ForeignKey(
        Category, related_name="categories", on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        SubCategory, related_name="sub_categories", on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False, db_index=True)
    views = models.PositiveIntegerField(default=0)
    fanfic_is_scraped = models.BooleanField(default=False)
    link_fanfic = models.URLField(max_length=255, blank=True, null=True)

    objects = FanficQuerySet.as_manager()
    published = PublishedManager()

    class Meta:
        ordering = ("-publish",)
        verbose_name = "fanfic"
        verbose_name_plural = "fanfics"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._unique_slug()
        super().save(*args, **kwargs)

    def _unique_slug(self) -> str:
        base = slugify(self.title)[:240] or "fanfic"
        slug, suffix = base, 2
        while Fanfic.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{suffix}"
            suffix += 1
        return slug

    @property
    def is_published(self) -> bool:
        return self.status == PublicationStatus.PUBLISHED


class Recommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True
    )
    fanfictions = models.ManyToManyField(Fanfic)
    generated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        verbose_name = "Recommendation"
        verbose_name_plural = "Recommendations"
        indexes = [models.Index(fields=["user", "-generated_at"])]

    def __str__(self):
        return f"Recommendation for {self.user}"


class UserFavorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fanfiction = models.ForeignKey(Fanfic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User favorite"
        verbose_name_plural = "User favorites"
        unique_together = ("user", "fanfiction")
        indexes = [models.Index(fields=["user", "created_at"])]

    def __str__(self):
        return f"{self.user} favorite {self.fanfiction}"
