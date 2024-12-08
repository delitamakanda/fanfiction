from django.db import models
from django.contrib.auth.models import User
from markdownx.models import MarkdownxField

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
		ordering = ['libelle']

	def __str__(self):
		return '{}: {}'.format(self.libelle, self.question)


"""
Lexique models
"""


class Lexique(models.Model):
	title = models.CharField(max_length=30, db_index=True)
	definition = models.TextField(max_length=500)
	created = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Lexique'
		verbose_name_plural = 'Lexiques'
		ordering = ['title']

	def __str__(self):
		return self.title
