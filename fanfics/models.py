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
        ('RO','Romance'),
        ('SU','Surnaturel'),
        ('ER','Erotique'),
        ('DR','Drame'),
        ('AM','Amitié'),
        ('AC','Action-Aventure'),
        ('SC','School-Fic'),
        ('MY','Mystère'),
        ('GE','Général'),
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
    author = models.ForeignKey(User, related_name="fanfics", on_delete=models.CASCADE)
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, blank=True, null=True)
    synopsis = models.CharField(max_length=250, blank=True, default='')
    credits = models.CharField(max_length=250, blank=True, default='')
    description = models.CharField(max_length=500, blank=True, default='')
    classement = models.CharField(max_length=2, choices=CLASSEMENT_CHOICES, default='g')
    genres = MultiSelectField(choices=GENRES_CHOICES)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(blank=True, null=True)
    was_featured_in_home = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='brouillon')
    users_like = models.ManyToManyField(User, related_name='fanfics_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    objects = models.Manager()
    published = PublishedManager()
    category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="sub_categories", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)

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

class Genres(models.Model):
    name = models.CharField(choices=Fanfic.GENRES_CHOICES, default='RO', max_length=4)

    class Meta:
        ordering = ('name',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def __str__(self):
        return self.name