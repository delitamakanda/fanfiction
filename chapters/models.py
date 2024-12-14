from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from api.fields import OrderField

from fanfics.models import Fanfic

class Chapter(models.Model):
	STATUS_CHOICES = (
		('brouillon', 'Brouillon'),
		('publié', 'Publié'),
	)
	author = models.ForeignKey(User, related_name="chapter", on_delete=models.CASCADE)
	fanfic = models.ForeignKey(Fanfic, related_name="chapters", on_delete=models.CASCADE)
	title = models.CharField(max_length=200, db_index=True)
	description = models.TextField(blank=True, default='')
	text = models.TextField()
	order = OrderField(blank=True, for_fields=['fanfic'])
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='brouillon')
	published = models.DateTimeField(blank=False, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, blank=True, null=True)

	class Meta:
		ordering = ['order']

	def __str__(self):
		return '{}. {}'.format(self.order, self.title)

	def get_absolute_url(self):
		return reverse('chapter-detail', args=[str(self.id)])

	def save(self, *args, **kwargs):
		if self.status == 'publié' and self.published is None:
			self.published = timezone.now()
		self.updated = timezone.now()
		super(Chapter, self).save(*args, **kwargs)
