from celery import task
from django.template.loader import get_template, render_to_string
from django.core.mail import send_mail
from django.core.mail import send_mass_mail

from api.models import Fanfic
from api.models import Chapter
from api.models import Comment

@task
def fanfic_created(fanfic_id):
    """
    Task to send an e-mail notification when a fanfic is successfully created.
    """
    fanfic = Fanfic.objects.get(id=fanfic_id)
    subject = 'Fanfiction id# {} - {}'.format(fanfic.id, fanfic.title)
    template = get_template('mail/fanfic_created_notification.txt')
    context = {'fanfic': fanfic}
    msg_text = template.render(context)
    msg_html = render_to_string('mail/fanfic_created_notification.html', context)
    # message = 'Cher {},\n\nVotre fanfiction {} a été créer avec succès. Son identifiant est le numéro #{}.'.format(fanfic.author.username, fanfic.title, fanfic.id)
    mail_sent = send_mail(subject, msg_text, "no-reply@fanfiction.com", [fanfic.author.email], html_message=msg_html)

    return mail_sent
