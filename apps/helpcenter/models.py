from django.db import models
from markdownx.models import MarkdownxField


class FoireAuxQuestions(models.Model):
    LIBELLE_CHOICES = (
        ("fan", "Fanfictions"),
        ("sit", "Le site"),
    )
    libelle = models.CharField(max_length=3, choices=LIBELLE_CHOICES, default="fan")
    question = models.CharField(max_length=255, db_index=True)
    reponse = MarkdownxField()
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Foire aux questions"
        verbose_name_plural = "Foires aux questions"
        ordering = ["libelle"]
        indexes = [models.Index(fields=["question"])]

    def __str__(self):
        return f"{self.libelle}: {self.question}"


class Lexique(models.Model):
    title = models.CharField(max_length=30, db_index=True)
    definition = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lexique"
        verbose_name_plural = "Lexiques"
        ordering = ["title"]
        indexes = [models.Index(fields=["title"])]

    def __str__(self):
        return self.title
