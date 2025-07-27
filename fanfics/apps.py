from django.apps import AppConfig
import json


class FanficsConfig(AppConfig):
    name = 'fanfics'
    verbose_name = 'Fanfics API'

    def ready(self):
        from django_celery_beat.models import PeriodicTask, IntervalSchedule
        def setup_recos_refresh():
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=1,
                period=IntervalSchedule.DAYS,
            )

            PeriodicTask.objects.update_or_create(
                name='Refresh recos for All Users',
                defaults={
                    'task': 'fanfics.tasks.refresh_recos_for_all_users',
                    'interval': schedule,
                    'args': json.dumps([]),
                }
            )
        setup_recos_refresh()
