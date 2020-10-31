"""Question and Choice model for poll application."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Vote(models.Model):
    """Vote model for vote each user have."""

    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=True)
    # user = models.ManyToManyField(User)
    # question = models.ForeignKey(Question, null=True, on_delete=models.PROTECT)
    question_id = models.IntegerField(default=0)
    voted = models.BooleanField(default=False)
    selected_choice_id = models.IntegerField(default=0)

    def __str__(self):
        """Return: vote id."""
        return self.id

    def is_voted(self):
        """Return: True if vote is already voted."""
        return self.voted

    def get_or_new(quest_id, user):
        """Return: existing vote or create new vote for this user."""
        vote = Vote.objects.filter(question_id=quest_id, user=user)
        if not vote.exists():
            vote = Vote.objects.create(user=user, voted=False, question_id=question_id)
        else:
            vote = vote[:1].get()
        return vote

    def save_choice(self, choice_id):
        """Save current choice voted."""
        self.voted = True
        self.selected_choice_id = choice_id
        self.save()


class Question(models.Model):
    """Question model for ku polls."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    # end_date = models.DateTimeField('ending date', null=True, blank=True)
    end_date = models.DateTimeField('ending date')
    # vote = models.IntegerField(default=0)
    vote = models.ForeignKey(Vote, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        """Return question as string."""
        return self.question_text

    def was_published_recently(self):
        """Return true if question is published less than 1 day ago."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_poll_end(self):
        """Return true is time already pass question end date."""
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
    # vote = models.ForeignKey(Vote, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        """Return choice as string."""
        return self.choice_text

    def decrease_vote(self):
        """Decrease choice's value by one."""
        self.votes -= 1
        self.save()

    def increase_vote(self):
        """Increase choice's value by one."""
        self.votes += 1
        self.save()
