from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def setup_rec_refresh_task():
	schedule, _ = IntervalSchedule.objects.get_or_create(
		    every=1,
            period=IntervalSchedule.DAYS,
	)

	PeriodicTask.objects.get_or_create(
		    name='refresh_recos_for_all_users',
            defaults={
				'task': 'fanfics.tasks.refresh_recos_for_all_users',
				'interval': schedule,
				'args': json.dumps([])
			},
	)


	PeriodicTask.objects.get_or_create(
		name='purge_recs_from_opted_out_users',
		defaults={
            'task': 'fanfics.tasks.purge_recs_from_opted_out_users',
            'interval': schedule,
            'args': json.dumps([])
        },
	)
