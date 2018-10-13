from celery import task
from django.core.mail import send_mail
from django.core.mail import send_mass_mail

from api.models import Fanfic
from api.models import Chapter
from api.models import Comment

@task
def fanfic_created(fanfic_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    fanfic = Fanfic.objects.get(id=fanfic_id)
    subject = 'Fanfic id# {}'.format(fanfic.id)
    message = 'Cher {},\n\nVotre fanfiction a été créer avec succès. Son identifiant est le numéro {}.'.format(fanfic.author.username, fanfic.id)
    mail_sent = send_mail(subject, message, "no-reply@fanfiction.com", [fanfic.author.email])

    return mail_sent
