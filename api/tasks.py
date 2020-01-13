from __future__ import absolute_import, unicode_literals

from celery.decorators import task
from celery.utils.log import get_task_logger

from django.template.loader import get_template, render_to_string
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from django.core import management

from fanfics.models import Fanfic
from chapters.models import Chapter
from comments.models import Comment
from accounts.models import FollowStories, FollowUser

logger = get_task_logger(__name__)

@task()
def fanfic_created(fanfic_id):
    """
    Task to send an e-mail notification when a fanfic is successfully created.
    """
    logger.info('******** CALLING ASYNC TASK WITH CELERY **********')
    
    fanfic = Fanfic.objects.get(id=fanfic_id)
    subject = 'Fanfiction id# {} - {}'.format(fanfic.id, fanfic.title)
    template = get_template('mail/fanfic_created_notification.txt')
    context = {'fanfic': fanfic}
    msg_text = template.render(context)
    msg_html = render_to_string('mail/fanfic_created_notification.html', context)
    # message = 'Cher {},\n\nVotre fanfiction {} a été créer avec succès. Son identifiant est le numéro #{}.'.format(fanfic.author.username, fanfic.title, fanfic.id)
    mail_sent = send_mail(subject, msg_text, "no-reply@fanfiction.com", [fanfic.author.email], html_message=msg_html)

    return mail_sent


@task()
def chapter_created(chapter_id):
    chapter = Chapter.objects.get(id=chapter_id)
    subject = 'Fanfiction : nouveau chapitre publié sur {}'.format(chapter.fanfic.title)
    template = get_template('mail/chapter_created_notification.txt')
    context = {'chapter': chapter}
    msg_text = template.render(context)
    msg_html = render_to_string('mail/chapter_created_notification.html', context)
    mail_sent = send_mail(subject, msg_text, "no-reply@fanfiction.com", [chapter.fanfic.author.email], html_message=msg_html)

    return mail_sent

@task()
def user_email_reminder():
	try:
		"""
		envoie un email aux users ne s'étant pas connecté depuis 2 semaines
		"""
		management.call_command("email_reminder", verbosity=0)
	except:
		print("error")
		
		
@task()
def deactivate_inactive_user():
	try:
		"""
		desactive les users non connectés pendant 1 an
		"""
		management.call_command("deactivateuser", "1year", verbosity=0)
	except:
		print("error")
