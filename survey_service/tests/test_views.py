from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from ..forms import SurveyForm
from ..models import Survey, Question, Answer, Color

User = get_user_model()


class RegistrationTestCase(TestCase):

    def test_register(self):
        url = reverse('survey_service:register')
        data = {'username': 'survey', 'password_1': '123', 'password_2': '123'}
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('registration/registration.html')

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')


class HomeViewTestCase(TestCase):

    def test_home_page(self):
        url = reverse('survey_service:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('survey_service/home.html')


class SurveyListView(TestCase):

    @classmethod
    def setUpTestData(cls):
        items = [Survey(title=f'survey {num}') for num in range(1, 11)]
        Survey.objects.bulk_create(items)

    def test_get_method(self):
        url = reverse('survey_service:all_surveys')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('survey_service/all_surveys.html')
        self.assertTrue(list(response.context_data['object_list']) == list(Survey.objects.all()))


class SurveyDetailViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user', password='123')
        self.survey = Survey.objects.create(title='survey')
        self.question = Question.objects.create(survey=self.survey, text='test text')
        self.correct_answer = Answer.objects.create(question=self.question, text='correct', correct=True)
        self.not_correct_answer = Answer.objects.create(question=self.question, text='false')

    def test_get_method(self):
        url = reverse('survey_service:detail_survey', kwargs={'pk': self.survey.pk})
        # none auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/survey/1/')
        # auth
        self.client.login(username='user', password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('survey_service/detail_survey.html')

    def test_post_method(self):
        url = reverse('survey_service:detail_survey', kwargs={'pk': self.survey.pk})
        self.client.login(username='user', password='123')
        # not correct
        data = {'question1': str(self.not_correct_answer.pk)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/survey_failed')
        # correct
        data = {'question1': str(self.correct_answer.pk)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/survey_passed')


class ProfileListViewTestCase(TestCase):

    def setUp(self) -> None:
        users = [User(username=f'user {num}', password='123') for num in range(1, 41)]
        User.objects.bulk_create(users)

    def test_get_method(self):
        url = reverse('survey_service:profile_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('survey_service/profile_list.html')
        self.assertEqual(response.context_data['is_paginated'], True)
        self.assertEqual(list(response.context_data['object_list']), list(User.objects.all()[:20]))


class ProfileDetailViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(username='user', password='123')

    def test_get_method(self):
        url = reverse('survey_service:profile', kwargs={'pk': self.user.pk})
        # none auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/profile/1/')
        # auth
        self.client.login(username='user', password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['color'], self.user.color)
        self.assertEqual(list(response.context_data['passed_surveys']), list(self.user.passed_surveys.all()))


class ColorListViewTestCase(TestCase):

    def setUp(self) -> None:
        colors = [Color(color=f'color {num}', price=num) for num in range(1, 4)]
        Color.objects.bulk_create(colors)
        User.objects.create_user(username='user', password='123')

    def test_get_method(self):
        url = reverse('survey_service:colors')
        # none auth
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/colors/')
        # auth
        self.client.login(username='user', password='123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context_data['object_list']), list(Color.objects.all()))


class BuyColorViewTestCase(TestCase):

    def setUp(self) -> None:
        colors = [Color(color=f'color {num}', price=num) for num in range(1, 4)]
        Color.objects.bulk_create(colors)
        self.user = User.objects.create_user(username='user', password='123', currency=2)

    def test_post_method(self):
        color = Color.objects.first()
        url = reverse('survey_service:buy_color', kwargs={'pk': color.pk})
        # none auth
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/buy_color/1/')
        # auth
        self.client.login(username='user', password='123')
        self.assertEqual(self.user.color, 'green')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/profile/1/')
        self.user.refresh_from_db()
        self.assertEqual(self.user.color, 'color 1')
        self.assertEqual(self.user.currency, 1)
        # color.price > user.currency
        color = Color.objects.last()
        url = reverse('survey_service:buy_color', kwargs={'pk': color.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/buy_failed/')