from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('request: {0!r}'.format(self.request))
	
@app.conf.beat_schedule = {
	'user_email_reminder_every_week': {
		'task': 'api.tasks.user_email_reminder',
		'schedule': 30.0, # todo
		'args': ()
	}
}
