import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.urlresolvers import reverse

from .models import Question, Choice


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_a_past_question(self):
        create_question(question_text='Past question.',days=-30)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


class QuestionIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('detail',args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response,past_question.question_text)

class QuestionTests(TestCase):
    def test_question_question_text(self):
        q = Question(question_text="teste1", pub_date=timezone.now())
        self.assertEqual(q.question_text, "teste1")

    def test_question_pub_date(self):
        now = timezone.now()
        q = Question(question_text="teste2", pub_date=now)
        self.assertEqual(q.pub_date, now)

class ChoiceTests(TestCase):
    q = Question(question_text="teste3", pub_date=timezone.now())

    def test_choice_question(self):
        c = Choice(question=q, choice_text="choice1", votes=10)
        self.assertEqual(c.question, q)

    def test_choice_choice_text(self):
        c = Choice(question=q, choice_text="choice2", votes=10)
        self.assertEqual(c.choice_text, "choice2")

    def test_choice_votes(self):
        c = Choice(question=q, choice_text="choice3", votes=10)
        self.assertEqual(c.votes, 10)
