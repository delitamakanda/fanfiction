from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class SluggedModel(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(SluggedModel):
    description = models.TextField(blank=True, default='')
    logic_value = models.CharField(max_length=60, blank=True, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('categories:category-detail', kwargs={'slug': self.slug})


class SubCategory(SluggedModel):
    category = models.ForeignKey(Category, related_name="category", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'sous-categorie'
        verbose_name_plural = 'sous-categories'

    def get_absolute_url(self):
        return reverse('categories:subcategory-detail', kwargs={'slug': self.slug})


class EntityCategory(models.Model):
    subcategory = models.ForeignKey(SubCategory, related_name="entity_subcategories", on_delete=models.CASCADE)
    entity = models.CharField(max_length=200, db_index=True)
    logic_value = models.CharField(max_length=60, blank=True, default='')

    class Meta:
        ordering = ('entity',)

    @property
    def category(self):
        return self.subcategory.category

    def __str__(self):
        return self.entity
