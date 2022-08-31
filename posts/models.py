from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from markdownx.models import MarkdownxField

CATEGORY_POST = (
    ('TU', 'Tutorial'),
    ('AR', 'Article'),
    ('IN', 'Information'),
)

class Tag(models.Model):
    word = models.CharField(max_length=35, db_index=True)
    slug = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

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
    category = models.CharField(max_length=2, choices=CATEGORY_POST, default='AR')

    class Meta:
        ordering = ('created',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return 'Blog post by {} on {}'.format(self.user, self.title)
