"""Unittest for poll application."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from polls.models import Question


def create_question(question_text, days):
    """
    Create a question with the given 'question_text' and published.

    The given number of 'days' offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    end_time = timezone.now() + datetime.timedelta(days=days + 20)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=end_time)


class DetailTests(TestCase):
    """unittest for detail page."""

    def setUp(self):
        """Unittest for user authentication."""
        self.user = get_user_model().objects.create_user(
            username="Sarah",
            email="sarah@email.com",
            password="S4r48"
        )

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 not found."""
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question's text."""
        past_question = create_question(
            question_text='Past question.', days=-5)
        self.client.login(username="Sarah", password="S4r48")
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
