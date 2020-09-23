from django.test import TestCase
from django.utils import timezone
import datetime
from .models import Question, Choice
from django.urls import reverse

# class QuestionModelTest(TestCase):

#     def setUp(self):
#         self.now = timezone.now()
#         self.past = self.now - datetime.timedelta(days=34)
#         self.future = self.now + datetime.timedelta(days=34)

#     def test_was_published_recently_with_recent_question(self):
#         """
#         was_published_recently() work corrctly with recent question.
#         """
#         q = Question(question_text="1+1=?", pub_date=self.now - datetime.timedelta(hours=2), end_date=self.future)
#         self.assertTrue(q.was_published_recently())

#     def test_was_published_recently_with_just_published_question(self):
#         """
#         Test was_published_recently() with question that just published now.
#         """
#         q = Question(question_text="Hello?", pub_date=self.now, end_date=self.future)
#         self.assertTrue(q.was_published_recently())
    
#     def test_was_published_recently_with_future_question(self):
#         """
#         Test was_published_recently() with future question.
#         """
#         q = Question(question_text="Hello?", pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
#         self.assertFalse(q.was_published_recently())

#     def test_was_published_recently_with_old_question(self):
#         """
#         Test was_published_recently() with old question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.future)
#         self.assertFalse(q.was_published_recently())

#     def test_was_published_question_with_ended_question(self):
#         """
#         Test was_published_recentky() with already ended question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.past + datetime.timedelta(days=3))
#         self.assertFalse(q.was_published_recently())

#     def test_is_poll_end_with_ended_question(self):
#         """
#         Test is_poll_ended() with already ended question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.now - datetime.timedelta(days=3))
#         self.assertTrue(q.is_poll_end())
    
#     def test_is_poll_end_with_not_end_question(self):
#         """
#         Test is_poll_end() with still on going question.
#         """
#         q = Question(question_text="Hello?", pub_date=self.past, end_date=self.future)
#         self.assertFalse(q.is_poll_end())

#     def test_is_poll_end_with_future_question(self):
#         """
#         Test is_poll_end() with still not published question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.future, end_date=self.future + datetime.timedelta(days=3))
#         self.assertFalse(q.is_poll_end())

#     def test_is_poll_end_question_that_end_now(self):
#         """
#         Test is_poll_end() with question that just end.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.now)
#         self.assertTrue(q.is_poll_end())

#     def test_is_published_with_old_question(self):
#         """
#         Test is_published() with old question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.future)
#         self.assertTrue(q.is_published())

#     def test_is_published_with_future_question(self):
#         """
#         Test is-published() with future question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
#         self.assertFalse(q.is_published())

#     def test_is_published_with_just_published_question(self):
#         """
#         Test is_published() with just published question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.now, end_date=self.future)
#         self.assertTrue(q.is_published())

#     def test_is_published_with_ended_question(self):
#         """
#         Test is_published() with already ended question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.past + datetime.timedelta(days=2))
#         self.assertTrue(q.is_published())
    
#     def test_can_vote_with_old_question(self):
#         """
#         Test can_vote() with old question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.future)
#         self.assertTrue(q.can_vote())

#     def test_can_vote_with_future_question(self):
#         """
#         Test can_vote() with future question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
#         self.assertFalse(q.can_vote())

#     def test_can_vote_with_ended_question(self):
#         """
#         Test can_vote() with ended question.
#         """
#         q = Question(question_text="Hello?",
#                      pub_date=self.past, end_date=self.past + datetime.timedelta(days=2))
#         self.assertFalse(q.can_vote())

class QuestionIndexViewTest(TestCase):

    def setUp(self):
        self.now = timezone.now()
        self.past = self.now - datetime.timedelta(days=34)
        self.future = self.now + datetime.timedelta(days=34)

    def test_index_with_no_poll(self):
            """
            If there is no question, Index must display a message.
            """
            response = self.client.get(reverse('polls:index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'No polls are available.')
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
            """
            Test is there is an already published question must be display on index page.
            """
            response = self.client.get(reverse('polls:index'))
            q = Question.objects.create(question_text="Hello?",
                         pub_date=self.now, end_date=self.future)
            self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Hello?>'])

    def test_future_question(self):
            """
            Test future question must not be display.
            """         
            response = self.client.get(reverse('polls:index'))
            q = Question.objects.create(question_text="Hello?",
                             pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        Test index with both future and past question. Only past question will be display.
        """
        response = self.client.get(reverse('polls:index'))
        q = Question.objects.create(question_text="Hi?",
                     pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
        q2 = Question.objects.create(question_text="Hello?",
                                         pub_date=self.past, end_date=self.future + datetime.timedelta(days=2))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Hello?>'])
