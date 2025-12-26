from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from fanfics.models import Fanfic

@receiver(m2m_changed, sender=Fanfic.users_like.through)
def users_like_changed(sender, instance, **kwargs):
	instance.total_likes = instance.users_like.count()
	instance.save()
