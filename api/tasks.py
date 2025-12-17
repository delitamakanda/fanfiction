from __future__ import absolute_import, unicode_literals

from django.template.loader import get_template, render_to_string
from django.core.mail import send_mail
from django.core.mail import send_mass_mail
from django.core import management

from fanfics.models import Fanfic
from chapters.models import Chapter
from accounts.models import FollowStories, FollowUser
from django.contrib.auth.models import User

def fanfic_created(fanfic_id):
    """
    Task to send an e-mail notification when a fanfic is successfully created.
    """
    fanfic = Fanfic.objects.get(id=fanfic_id, status='publié')

    """
    get all followers of the author
    """
    followers = FollowUser.objects.filter(user_to=fanfic.author).values_list('user_from', flat=True)
    users = User.objects.filter(id__in=followers).values_list('email', flat=True)
    emaillists = []
    for email in users:
        emaillists.append(str(email))
    subject = 'Fanfiction id# {} - {}'.format(fanfic.id, fanfic.title)
    template = get_template('mail/fanfic_created_notification.txt')
    context = {'fanfic': fanfic}
    msg_text = template.render(context)
    msg_html = render_to_string('mail/fanfic_created_notification.html', context)
    # message = 'Cher {},\n\nVotre fanfiction {} a été créer avec succès. Son identifiant est le numéro #{}.'.format(fanfic.author.username, fanfic.title, fanfic.id)

    send_mail(subject, msg_text, "no-reply@fanfiction.com", [fanfic.author.email], html_message=msg_html)
    message = (subject, f'{fanfic.author.username} a publié une nouvelle story', "no-reply@fanfiction.com", emaillists)

    mail_sent = send_mass_mail((message,), fail_silently=False)

    return mail_sent


def chapter_created(chapter_id):
    chapter = Chapter.objects.get(id=chapter_id, status='publié')
    followers = FollowStories.objects.filter(to_fanfic=chapter.fanfic).values_list('from_user', flat=True)
    users = User.objects.filter(id__in=followers).values_list('email', flat=True)
    emaillists = []
    for email in users:
        emaillists.append(str(email))
    subject = 'Fanfiction : nouveau chapitre publié sur {}'.format(chapter.fanfic.title)
    template = get_template('mail/chapter_created_notification.txt')
    context = {'chapter': chapter}
    msg_text = template.render(context)
    msg_html = render_to_string('mail/chapter_created_notification.html', context)

    send_mail(subject, msg_text, "no-reply@fanfiction.com", [chapter.fanfic.author.email], html_message=msg_html)
    message = (subject, f'{chapter.author.username} a publié un nouveau chapitre pour {chapter.fanfic.title}', "no-reply@fanfiction.com", emaillists)

    mail_sent = send_mass_mail((message,), fail_silently=False)

    return mail_sent

def user_email_reminder():
    try:
        """
        envoie un email aux users ne s'étant pas connecté depuis 2 semaines
        """
        management.call_command("email_reminder", verbosity=0)
    except:
        print("error")


def deactivate_inactive_user():
    try:
        """
        desactive les users non connectés pendant 1 an
        """
        management.call_command("deactivateuser", "1year", verbosity=0)
    except:
        print("error")
