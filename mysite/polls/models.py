import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question model for ku polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # end_date = models.DateTimeField('ending date', null=True, blank=True)
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """Return true if question is published less than 1 day ago."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_poll_end(self):
        """Return true is time already pass question end date."""
        # now = timezone.now()
        # if (self.end_date == False):
        #     return ""
        return self.end_date <= timezone.now()

    def is_published(self):
        """Return true if time pass question question published date."""
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """Return true if question already pass it's published date and still not pass it's end date."""
        if (self.is_published() and not self.is_poll_end()):
            return True
        return False

    # modify column view in admin - see list_display
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    is_poll_end.admin_order_field = 'end_date'
    is_poll_end.boolean = True
    is_poll_end.short_description = 'Poll ended?'


class Choice(models.Model):
    """Choice model for choices in each question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
