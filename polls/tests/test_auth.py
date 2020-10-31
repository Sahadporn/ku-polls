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


class AuthTests(TestCase):
    """Unittest for user authentication."""

    def setUp(self):
        """Set up new user for unittest."""
        self.user = get_user_model().objects.create_user(
            username="Sarah",
            email="sarah@email.com",
            password="S4r48",
            first_name="sarah"
        )

    def test_login_to_index_page(self):
        """Test user should be able to login to index page."""
        self.client.login(username="Sarah", password="S4r48")
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)

    def test_unauthenticated_user_in_datil_page(self):
        """Test unauthenticated user should not be able to direct to detail page."""
        past_question = create_question(
            question_text='Past question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        login = "/accounts/login/?next=/" + f"{past_question.id}" + "/"
        self.assertRedirects(response, login)

    def test_login_to_detail_page(self):
        """Test user log in should be able to direct to detail page."""
        past_question = create_question(
            question_text='Past question.', days=-5)
        self.client.login(username="Sarah", password="S4r48")
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_to_results_page(self):
        """Test already logged in user should be able to view result page."""
        past_question = create_question(
            question_text='Past question.', days=-5)
        self.client.login(username="Sarah", password="S4r48")
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_user_in_result_page(self):
        """Test unauthenticated user should be allowed to view result page."""
        past_question = create_question(
            question_text='Past question.', days=-5)
        url = reverse('polls:results', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
