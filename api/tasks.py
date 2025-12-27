from __future__ import absolute_import, unicode_literals
from django.core import management

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
