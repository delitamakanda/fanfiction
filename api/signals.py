from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from fanfics.models import Fanfic
from accounts.models import AccountProfile

@receiver(m2m_changed, sender=Fanfic.users_like.through)
def users_like_changed(sender, instance, **kwargs):
	instance.total_likes = instance.users_like.count()
	instance.save()

@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
	if created:
		profile = AccountProfile(user=instance)
		profile.save()
