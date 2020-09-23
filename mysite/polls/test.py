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


def create_question(question_text, days):
    """
        Create a question with the given 'question_text' and published
        the given number of 'days' offset to now (negative for questions published
        in the past, positive for questions that have yet to be published).
        """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time + datetime.timedelta(days=334))


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
        q2 = Question.objects.create(question_text="Hello?",
                                     pub_date=self.past, end_date=(self.future + datetime.timedelta(days=2)))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: Hello?>'])

    def test_future_question(self):
            """
            Test future question must not be display.
            """         
            q = Question.objects.create(question_text="Hello?",
                             pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
            response = self.client.get(reverse('polls:index'))
            self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        """
        Test index with both future and past question. Only past question will be display.
        """
        q = Question.objects.create(question_text="Hi?",
                     pub_date=self.future, end_date=self.future + datetime.timedelta(days=2))
        q2 = Question.objects.create(question_text="Hello?",
                                         pub_date=self.past, end_date=self.future + datetime.timedelta(days=2))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Hello?>'])

    def test_two_published_poll(self):
        q = Question.objects.create(question_text="Hi?",
                                    pub_date=self.past, end_date=self.future + datetime.timedelta(days=2))
        q2 = Question.objects.create(question_text="Hello?",
                                     pub_date=self.past, end_date=self.future + datetime.timedelta(days=2))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [
                                 '<Question: Hi?>', '<Question: Hello?>'])

    def test_redirect_root_url(self):
        """
        root url should redirect to polls index.
        """                         
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        pollURL = reverse('polls:index')
        self.assertRedirects(response, pollURL)

    def test_poll_index(self):
        q = Question.objects.create(question_text="Hi?",
                                    pub_date=self.past, end_date=self.future + datetime.timedelta(days=2))
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'polls/index.html')
        self.assertIn(str.encode(q.question_text), response.content)

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        """
        Detail view with future question should return 404 not found.
        """
        fu = Question.objects.create(question_text="Hi?", pub_date=timezone.now() + datetime.timedelta(days=1), end_date=timezone.now() + datetime.timedelta(days=2))
        url = reverse('polls:detail', args=(fu.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        q = Question.objects.create(question_text="Hi?", pub_date=timezone.now(
        ) - datetime.timedelta(days=1), end_date=timezone.now() + datetime.timedelta(days=2))
        url = reverse('polls:detail', args=(q.id,))
        response = self.client.get(url)
        self.assertContains(response, q.question_text)
    
    def test_ended_question(self):
        q = Question.objects.create(question_text="Hi?", pub_date=timezone.now(
        ) - datetime.timedelta(days=2), end_date=timezone.now() - datetime.timedelta(days=1))
        url = reverse('polls:detail', args=(q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('polls:index'))
        self.assertIn(response.content, str.encode("ended"))

    def test_detail_with_wrong_question_id(self):
        response = self.client.get(reverse('polls:detail', args=("1",)))
        self.assertEqual(response.status_code, 404)

    def test_post_in_detail(self):
        q = Question.objects.create(question_text="Hi?", pub_date=timezone.now(
        ) - datetime.timedelta(days=1), end_date=timezone.now() + datetime.timedelta(days=2))
        c = Choice.objects.create(choice_text="Nope", question=q)
        c1 = Choice.objects.create(choice_text="Sure", question=q)
        a = self.client.get('polls:results', args=(q.id,))
        self.assertEqual(a.status_code, 404)
        response = self.client.post('/polls/{q.id}/', {'choice': '2'})
        self.assertEqual(response.status_code, 404)
        # self.assertRedirects(a, response)
