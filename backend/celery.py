from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
	'user_email_reminder_every_week': {
		'task': 'api.tasks.user_email_reminder',
		'schedule': crontab(hour=7, minute=30, day_of_week=1),
		'args': ()
	},
	'deactivate_inactive_user': {
		'task': 'api.tasks.deactivate_inactive_user',
		'schedule': crontab(hour=0, minute=0, day_of_month=1, month_of_year=1),
		'args': ()
	}
}

app.conf.timezone = 'UTC'
