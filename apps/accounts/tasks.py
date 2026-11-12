import logging

from celery import shared_task

from apps.accounts import services

logger = logging.getLogger(__name__)

INACTIVITY_DAYS = 365


@shared_task(name="accounts.tasks.send_login_reminders")
def send_login_reminders() -> int:
    """E-mail users who have not logged in for two weeks."""
    sent = services.send_login_reminders(days=14)
    logger.info("Login reminders sent: %s", sent)
    return sent


@shared_task(name="accounts.tasks.deactivate_inactive_users")
def deactivate_inactive_users() -> int:
    """Deactivate users who have not logged in for a year."""
    count = services.deactivate_inactive_users(days=INACTIVITY_DAYS)
    logger.info("Inactive users deactivated: %s", count)
    return count
