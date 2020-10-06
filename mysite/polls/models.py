import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    # end_date = models.DateTimeField('ending date', null=True, blank=True)
    end_date = models.DateTimeField('ending date')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_poll_end(self):
        # now = timezone.now()
        # if (self.end_date == False):
        #     return ""
        return self.end_date <= timezone.now()

    def is_published(self):
        return timezone.now() >= self.pub_date
    
    def can_vote(self):
        if self.is_published() and not self.is_poll_end():
            return True
        return False
    
    def total_votes(self):
        # sum = 0
        # for choice in self.choice_set.all():
        #     sum += choice.votes
        # return sum
        votes = self.choice_set.aggregate(models.Sum('votes'))
        return votes['votes__sum']
    
    def reset_votes(self):
        for choice in self.choice_set.all():
            choice.votes = 0
            choice.save()
    
    # modify column view in admin - see list_display
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    is_poll_end.admin_order_field = 'end_date'
    is_poll_end.boolean = True
    is_poll_end.short_description = 'Poll ended?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)

    def __str__(self):
        return self.choice_text
