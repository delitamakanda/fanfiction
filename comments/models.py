from django.db import models
from django.contrib.auth.models import User
from fanfics.models import Fanfic
from chapters.models import Chapter

class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	fanfic = models.ForeignKey(Fanfic, related_name='comments', on_delete=models.CASCADE)
	chapter = models.ForeignKey(Chapter, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True, blank=True, null=True)
	active = models.BooleanField(default=True)
	in_reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='replies'  )

	class Meta:
		ordering = ('-created',)
		verbose_name = 'comment'
		verbose_name_plural = 'comments'

	def __str__(self):
		return 'Comment by {} on {}'.format(self.author.username, self.fanfic.title)
