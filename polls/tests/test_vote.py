"""Unittest for poll application."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model

from polls.models import Question, Choice, Vote


def create_question(question_text, days, vote):
    """
    Create a question with the given 'question_text' and published.

    The given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = timezone.now() + datetime.timedelta(days=days + 20)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)


class VoteTests(TestCase):
    """Unittest for Vote model."""

    def setUp(self):
        """Set up user, question, and choice for unittest."""
        self.user = get_user_model().objects.create_user(
            username="Sarah",
            email="sarah@email.com",
            password="S4r48",
            first_name="sarah"
        )
        self.question = create_question("Two choices", -5)
        self.choiceA = Choice.objects.create(question=self.question, choice_text="choice A", vote=0)
        self.choiceB = Choice.objects.create(question=self.question, choice_text="choice B", vote=0)

    def test_first_vote(self):
        """Test question choice should increase by one when user voted."""
        self.client.login(username="Sarah", password="S4r48")
        vote = Vote.get_or_new(self.question.id, self.user)
        self.question.vote = vote
        self.choiceA.increase_vote()
        self.question.vote.save_choice(self.choiceA.id)
        self.assertTrue(vote.voted)
        self.assertEqual(self.choiceA.votes, 1)

    def test_same_user_vote_same_question(self):
        """Test choice value should change by one if the same user vote in the same question."""
        self.client.login(username="Sarah", password="S4r48")
        vote = Vote.get_or_new(self.question.id, self.user)
        self.question.vote = vote
        self.choiceA.increase_vote()
        self.question.vote.save_choice(self.choiceA.id)
        self.assertTrue(vote.voted)

        self.choiceB.increase_vote()
        self.choiceA.decrease_vote()
        self.assertEqual(self.choiceA, 0)
        self.assertEqual(self.choiceB, 1)

    def test_two_user_vote_on_the_same_question(self):
        """Test second user vote should not effect the first user vote."""
        self.client.login(username="Sarah", password="S4r48")
        vote = Vote.get_or_new(self.question.id, self.user)
        self.choiceA.increase_vote()
        vote.save_choice(self.choiceA.id)
        self.assertTrue(vote.voted)

        user1 = get_user_model().objects.create_user(
            username="John",
            email="john@email.com",
            password="J0hn",
            first_name="john"
        )
        self.client.login(username="John", password="J0hn")
        vote_john = Vote.get_or_new(self.question.id, user1)
        self.choiceA.increase_vote()
        vote_john.save_choice(self.choiceA.id)
        self.assertTrue(vote_john.voted)
        self.assertEqual(self.choiceA.votes, 2)
        self.choiceB.increase_vote()
        self.choiceA.decrease_vote()
        vote_john.save_choice(self.choiceB.id)
        self.assertEqual(self.choiceA, 1)
        self.assertEqual(self.choiceB, 1)
