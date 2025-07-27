from django.urls import reverse
from multiselectfield import MultiSelectField

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.utils import timezone

from categories.models import Category, SubCategory


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publié')


class Fanfic(models.Model):
    GENRES_CHOICES = (
        ('RO', 'Romance'),
        ('SU', 'Surnaturel'),
        ('ER', 'Erotique'),
        ('DR', 'Drame'),
        ('AM', 'Amitié'),
        ('AC', 'Action-Aventure'),
        ('SC', 'School-Fic'),
        ('MY', 'Mystère'),
        ('GE', 'Général'),
        ('DCED', 'De cape et d\'épée'),
        ('LE', 'Lemon'),
        ('HU', 'Humour'),
        ('OS', 'One-Shot'),
        ('SUS', 'Suspense'),
        ('TH', 'Thriller'),
        ('HO', 'Horreur'),
        ('HF', 'Heroic Fantasy'),
        ('TR', 'Tragédie'),
        ('CO', 'Cross-Over'),
    )
    STATUS_CHOICES = (
        ('brouillon', 'Brouillon'),
        ('publié', 'Publié'),
    )
    CLASSEMENT_CHOICES = (
        ('g', 'G'),
        ('13', '13+'),
        ('r', 'R'),
        ('18', '18+'),
    )
    author = models.ForeignKey(
        User, related_name="fanfics", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True,
                            unique=True, blank=True, null=True)
    synopsis = models.CharField(max_length=1000, blank=True, default='')
    credits = models.CharField(max_length=255, blank=True, default='')
    picture = models.CharField(max_length=1000, blank=True, null=True)
    language = models.CharField(max_length=2, default='fr')
    description = models.CharField(max_length=1000, blank=True, default='')
    classement = models.CharField(
        max_length=2, choices=CLASSEMENT_CHOICES, default='g')
    genres = MultiSelectField(choices=GENRES_CHOICES, max_length=4)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    was_featured_in_home = models.BooleanField(default=False)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='brouillon')
    users_like = models.ManyToManyField(
        User, related_name='fanfics_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    objects = models.Manager()
    published = PublishedManager()
    category = models.ForeignKey(
        Category, related_name="categories", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(
        SubCategory, related_name="sub_categories", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    fanfic_is_scraped = models.BooleanField(default=False)
    link_fanfic = models.URLField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'fanfic'
        verbose_name_plural = 'fanfics'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Fanfic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    @staticmethod
    def most_liked_fanfics():
        return Fanfic.objects.filter(status='publié').order_by('-total_likes')[:10]

    @staticmethod
    def newest_fanfics(self):
        return Fanfic.objects.filter(status='publié').order_by('-publish')[:10]

    def get_absolute_url(self):
        return reverse('fanfic_detail', args=[self.id, self.slug])


class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fanfictions = models.ManyToManyField(Fanfic)
    generated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Recommendation for {self.user.username}'

    class Meta:
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'


class UserFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fanfiction = models.ForeignKey(Fanfic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User favorite'
        verbose_name_plural = 'User favorites'

    def __str__(self):
        return f'{self.user.username} favorite {self.fanfiction.title}'
