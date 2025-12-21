from django.db import models
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    description = models.TextField(blank=True, default='')
    logic_value = models.CharField(max_length=60, blank=True, default='')

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class EntityCategory(models.Model):
    category = models.ForeignKey(Category, related_name="entity_categories", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name="entity_subcategories", on_delete=models.CASCADE)
    entity = models.CharField(max_length=200, db_index=True)
    logic_value = models.CharField(max_length=60, blank=True, default='')

    class Meta:
        ordering = ('entity',)

    def __str__(self):
        return self.entity
