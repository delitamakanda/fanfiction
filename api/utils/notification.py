import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from accounts.models import Notification


def create_notification(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)

    filter_kwargs = {
        'user_id': user.id,
        'verb': verb,
        'created__gte': last_minute,
        'unread': True,
        'hidden': False,
        'archived': False,
    }

    if target:
        filter_kwargs['target_ct'] = ContentType.objects.get_for_model(target),
        filter_kwargs['target_id'] = target.id,

    notification, created = Notification.objects.get_or_create(
        defaults={'user': user, 'verb': verb, 'target': target},
        **filter_kwargs,
    )

    return created

