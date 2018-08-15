from django.db import models

# Create your models here.
class Lexique(models.Model):
    title = models.CharField(max_length=30, db_index=True)
    definition = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
