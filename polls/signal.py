"""Logger function for log in, log out, and log in failed."""
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

log = logging.getLogger(__name__)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, **kwargs):
    """Log in callback for logger."""
    ip = request.META.get('REMOTE_ADDR')

    log.info("IP: %s Username: %s Logged in", ip, request.user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, **kwargs):
    """Log out callback for logger."""
    ip = request.META.get('REMOTE_ADDR')

    log.info("IP: %s Username: %s Logged out", ip, request.user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    """Log in failed callback for logger."""
    ip = request.META.get('REMOTE_ADDR')

    log.info("IP: %s Username: %s Failed to Log in", ip, credentials['username'])
