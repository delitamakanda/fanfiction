from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from fanfics.models import Fanfic

class Notification(models.Model):
	user = models.ForeignKey(User, related_name='notifications', db_index=True, on_delete=models.CASCADE)
	verb = models.CharField(max_length=255)
	target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
	target_id = models.PositiveIntegerField(blank=True, null=True, db_index=True)
	read = models.BooleanField(default=False)
	target = GenericForeignKey('target_ct', 'target_id')
	created = models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = 'Notification'
		verbose_name_plural = 'Notifications'

	def __str__(self):
		return f'{self.user.username} - {self.verb}'
	def get_absolute_url(self):
		return f'/notification/{self.id}/'

	def mark_as_read(self):
		self.read = True
		self.save()


class AccountProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="accountprofile")
	date_of_birth = models.DateField(blank=True, null=True)
	photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
	location = models.CharField(max_length=30, blank=True)
	bio = models.TextField(blank=True)
	reco_consent_given = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Account profile'
		verbose_name_plural = 'Accounts profiles'

	def __str__(self):
		return  f'Profile for user {self.user.username}'

	def save(self, *args, **kwargs):
		super(AccountProfile, self).save(*args, **kwargs)

		if self.photo:
			photo = Image.open(self.photo)
			p_width, p_height = photo.size
			max_size = (1000,1000)

			if p_width > 1000:
				photo.thumbnail(max_size, Image.Resampling.LANCZOS)
				buffer = BytesIO()
				photo.save(buffer, format='JPEG', quality=90, optimize=True)
				buffer.seek(0)
				self.photo.save(self.photo.name, ContentFile(buffer.getvalue()), save=False)
				super(AccountProfile, self).save(*args, **kwargs)


class Social(models.Model):
	SOCIAL_TYPES = (
		('twitter', 'Twitter'),
		('facebook', 'Facebook'),
		('pinterest', 'Pinterest'),
		('instagram', 'Instagram'),
	)
	network = models.CharField(max_length=255, choices=SOCIAL_TYPES)
	nichandle = models.CharField(max_length=255)
	account = models.ForeignKey(AccountProfile, related_name="social_network", on_delete=models.CASCADE, db_index=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)

	class Meta:
		ordering = ('network',)
		verbose_name = 'Social account'
		verbose_name_plural = 'Social accounts'
		unique_together = ('network', 'account')


	def __str__(self):
		return 'Social network {} for user {}'.format(self.network, self.user.username)


class FollowUser(models.Model):
	user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE, db_index=True)
	user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE, db_index=True)
	created= models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = 'follow user'
		verbose_name_plural = 'follow users'
		unique_together = ('user_from', 'user_to')

	def __str__(self):
		return '{} follows {}'.format(self.user_from, self.user_to)


class FollowStories(models.Model):
	from_user = models.ForeignKey(User, related_name='fanfic', on_delete=models.CASCADE, db_index=True)
	to_fanfic = models.ForeignKey(Fanfic, related_name='users', on_delete=models.CASCADE, db_index=True)
	created= models.DateTimeField(auto_now_add=True, db_index=True)

	class Meta:
		ordering = ('-created',)
		verbose_name = 'follow story'
		verbose_name_plural = 'follow stories'
		unique_together = ('from_user', 'to_fanfic')

	def __str__(self):
		return '{} follows {}'.format(self.from_user, self.to_fanfic)

# add to User models dynamically
User.add_to_class('following', models.ManyToManyField('self', through=FollowUser, related_name='followers', symmetrical=False))
