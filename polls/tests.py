import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    """unittest for Question model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for question whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for question whpse pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for question whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def create_question(question_text, days):
        """
        Create a question with the given 'question_text' and published
        the given number of 'days' offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)

    def test_is_poll_end_past_question(self):
        """is_poll_end return True if current time already pass question end_date and False otherwise."""
        pub_time = timezone.now() - datetime.timedelta(hours=23)
        end_time = timezone.now()
        question = Question(pub_date=pub_time, end_date=end_time)
        question2 = Question(pub_date=pub_time, end_date=end_time + datetime.timedelta(hours=2))
        self.assertTrue(question.is_poll_end())
        self.assertFalse(question2.is_poll_end())

    def test_is_published_when_past_published_date(self):
        """is_published() return True if current time already pass pub_date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23)
        end_time = timezone.now() + datetime.timedelta(hours=40)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertTrue(question.is_published())

    def test_is_published_before_published_date(self):
        """is_published() return False if current time is before pub_date."""
        pub_time = timezone.now() + datetime.timedelta(hours=23)
        end_time = timezone.now() + datetime.timedelta(hours=40)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(question.is_published())

    def test_is_published_when_pub_date_is_now(self):
        """is_published() return True when pub_date equal current time."""
        pub_time = timezone.now()
        end_time = timezone.now() + datetime.timedelta(hours=40)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertTrue(question.is_published())

    def test_can_vote_before_pub_date(self):
        """can_vote() return False when current time is before pub_date."""
        pub_time = timezone.now() + datetime.timedelta(hours=23)
        end_time = timezone.now() + datetime.timedelta(hours=40)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(question.can_vote())

    def test_can_vote_after_pub_date(self):
        """can_vote() return True if current time pass pub_date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23)
        end_time = timezone.now() + datetime.timedelta(hours=40)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertTrue(question.can_vote())

    def test_can_vote_after_end_date(self):
        """can_vote() return False if current time pass end_date."""
        pub_time = timezone.now() - datetime.timedelta(hours=23)
        end_time = timezone.now() - datetime.timedelta(hours=4)
        question = Question(pub_date=pub_time, end_date=end_time)
        self.assertFalse(question.can_vote())

    class QuestionIndexViewTests(TestCase):
        """unittest for the index page."""

        def test_no_question(self):
            """If no question exist, an appropriate message is displayed."""
            response = self.client.get(reverse('polls:index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_past_question(self):
            """Question with pub_date in the past are displayed on the index page."""
            create_question(question_text="Past question.", days=-30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context['latest_question_list'],
                                     ['<Question: Past question.>'])

        def test_future_question(self):
            """Question with pub_date in the future aren't displayed on the index page."""
            create_question(question_text="Future question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertContains(response, "No polls are available.")
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

        def test_future_question_and_past_question(self):
            """Even if both past and future question exist, only past questions are displayed."""
            create_question(question_text="Past question.", days=-30)
            create_question(question_text="Future question.", days=30)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'], ['<Question: Past question.>'])

        def test_two_past_question(self):
            """The questions index page may display nultiple questions."""
            create_question(question_text="Past question 1.", days=-30)
            create_question(question_text="Past question 2.", days=-5)
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(
                response.context['latest_question_list'],
                ['<Question: Past question 2.>', '<Question: Past question 1.>'])

    class QuestionDetailViewTests(TestCase):
        """unittest for detail page."""

        def test_future_question(self):
            """The detail view of a question with a pub_date in the future returns a 404 not found."""
            future_question = create_question(question_text='Future question.', days=5)
            url = reverse('polls:detail', args=(future_question.id,))
            response = self.client.get(url)
            self.assertEqual(response.status_code, 404)

        def test_past_question(self):
            """The detail view of a question with a pub_date in the past displays the question's text."""
            past_question = create_question(
                question_text='Past question.', days=-5)
            url = reverse('polls:detail', args=(past_question.id,))
            response = self.client.get(url)
            self.assertContains(response, past_question.question_text)
