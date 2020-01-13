from django.db import models

from fanfics.models import Fanfic
from chapters.models import Chapter

class Comment(models.Model):
    fanfic = models.ForeignKey(Fanfic, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=80, db_index=True)
    email = models.EmailField(blank=True, null=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    in_reply_to = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name='comments_by_chapters', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.fanfic)
