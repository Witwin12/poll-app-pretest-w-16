import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_was_published_recently_with_present_question(self):
        """
        was_published_recently() returns True for a question with a pub_date
        very close to now.
        """
        time = timezone.now()
        present_question = Question(pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question2, question1],
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
class WarmHotQuestionTests(TestCase):
    def create_question_with_votes(self, question_text, days, votes_list):
        """
        Create a question with choices, each having a specific number of votes.
        """
        question = create_question(question_text=question_text, days=days)
        for votes in votes_list:
            question.choice_set.create(choice_text="Choice", votes=votes)
        return question

    def test_warm_question(self):
        """
        A question with total votes between 10 and 50 should be categorized as warm.
        """
        question = self.create_question_with_votes("Warm Question", days=-1, votes_list=[30])
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        self.assertTrue(10 < total_votes <= 50)

    def test_hot_question(self):
        """
        A question with total votes greater than 50 should be categorized as hot.
        """
        question = self.create_question_with_votes("Hot Question", days=-1, votes_list=[60])
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        self.assertTrue(total_votes > 50)

    def test_cold_question(self):
        """
        A question with total votes less than or equal to 10 should not be warm or hot.
        """
        question = self.create_question_with_votes("Cold Question", days=-1, votes_list=[5])
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        self.assertTrue(total_votes <= 10)

    def test_mixed_votes_warm(self):
        """
        A question with multiple choices where the total votes fall in the warm range.
        """
        question = self.create_question_with_votes("Mixed Warm Question", days=-1, votes_list=[10, 20, 5])
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        self.assertTrue(10 < total_votes <= 50)

    def test_mixed_votes_hot(self):
        """
        A question with multiple choices where the total votes fall in the hot range.
        """
        question = self.create_question_with_votes("Mixed Hot Question", days=-1, votes_list=[25, 30, 10])
        total_votes = sum(choice.votes for choice in question.choice_set.all())
        self.assertTrue(total_votes > 50)
