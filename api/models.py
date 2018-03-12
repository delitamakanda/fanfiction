from django.db import models
from django.core.validators import URLValidator
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from api.fields import OrderField
from multiselectfield import MultiSelectField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.template.defaultfilters import slugify

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'sous-categorie'
        verbose_name_plural = 'sous-categories'

    def __str__(self):
        return self.name


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
        ('SU', 'Suspense'),
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
    description = models.CharField(max_length=250, blank=True, default='')
    classement = models.CharField(max_length=2, choices=CLASSEMENT_CHOICES, default='g')
    genres = MultiSelectField(choices=GENRES_CHOICES, max_choices=5, max_length=3)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    was_featured_in_home = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    likes = models.PositiveIntegerField(default=0)
    objects = models.Manager()
    published = PublishedManager()
    category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="sub_categories", on_delete=models.CASCADE)

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'fanfic'
        verbose_name_plural = 'fanfics'

    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Chapter(models.Model):
    fanfic = models.ForeignKey(Fanfic, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    text = models.TextField()
    order = OrderField(blank=True, for_fields=['fanfic'])

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Fanfic, self).save(*args, **kwargs)

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Comment(models.Model):
    fanfic = models.ForeignKey(Fanfic, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    in_reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.fanfic)


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return 'Blog post by {} on {}'.format(self.user, self.title)
