"""Poll app config."""
from django.apps import AppConfig
import polls.signal


class PollsConfig(AppConfig):
    """Polls application config."""

    name = 'polls'
