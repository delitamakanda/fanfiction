from PIL import Image

from django.db import models
from django.conf import settings

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

from markdownx.models import MarkdownxField

# Create your models here.
class AccountProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ('user',)
        verbose_name = 'Account profile'
        verbose_name_plural = 'Accounts profiles'

    def save(self, *args, **kwargs):
        super(AccountProfile, self).save(*args, **kwargs)

        if self.photo:
            photo = Image.open(self.photo)
            p_width, p_height = photo.size
            max_size = (1000,1000)

            if p_width > 1000:
                photo.thumbnail(max_size, Image.ANTIALIAS)
                photo.save(self.photo.path)


    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Social(models.Model):
    SOCIAL_TYPES = (
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('pinterest', 'Pinterest'),
        ('instagram', 'Instagram'),
    )
    network = models.CharField(max_length=255, choices=SOCIAL_TYPES)
    nichandle = models.CharField(max_length=255)
    account = models.ForeignKey(AccountProfile, related_name="social_network", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ('network',)
        verbose_name = 'Social account'
        verbose_name_plural = 'Social accounts'


    def __str__(self):
        return 'Social network {} for user {}'.format(self.network, self.user.username)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='publié')


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True, default='')
    logic_value = models.CharField(max_length=60, blank=True, default='')

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
    updated = models.DateTimeField(auto_now=True)
    was_featured_in_home = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='brouillon')
    users_like = models.ManyToManyField(User, related_name='fanfics_liked', blank=True)
    total_likes = models.PositiveIntegerField(db_index=True, default=0)
    objects = models.Manager()
    published = PublishedManager()
    category = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="sub_categories", on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'fanfic'
        verbose_name_plural = 'fanfics'


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Fanfic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class FollowUser(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'follow user'
        verbose_name_plural = 'follow users'

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)


class FollowStories(models.Model):
    from_user = models.ForeignKey(User, related_name='fanfic', on_delete=models.CASCADE)
    to_fanfic = models.ForeignKey(Fanfic, related_name='users', on_delete=models.CASCADE)
    created= models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'follow story'
        verbose_name_plural = 'follow stories'

    def __str__(self):
        return '{} follows {}'.format(self.from_user, self.to_fanfic)


class Chapter(models.Model):
    author = models.ForeignKey(User, related_name="chapter", on_delete=models.CASCADE)
    fanfic = models.ForeignKey(Fanfic, related_name="chapters", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True, default='')
    text = models.TextField()
    order = OrderField(blank=True, for_fields=['fanfic'])
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class Comment(models.Model):
    fanfic = models.ForeignKey(Fanfic, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80, db_index=True)
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


class CommentByChapter(Comment):
    chapter = models.ForeignKey(Chapter, related_name='comments_by_chapters', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)
        verbose_name = 'comment by chapter'
        verbose_name_plural = 'comments by chapters'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.chapter)


class Tag(models.Model):
    word = models.CharField(max_length=35, db_index=True)
    slug = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.word)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.word


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, db_index=True)
    header = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    content = MarkdownxField()
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return 'Blog post by {} on {}'.format(self.user, self.title)


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




class Lexique(models.Model):
    title = models.CharField(max_length=30, db_index=True)
    definition = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
