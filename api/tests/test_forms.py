from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from helpcenter.views import communities_view_new_topic
from api.models import Board, Topic, Message
from api.helpcenter.forms import NewTopicForm

class NewTopicFormTests(TestCase):
    def setUp(self):
        Board.objects.create(name='Anime-Mangas', description='bla bla bla.')
        User.objects.create_user(id=1, username='homer simpson', email='homer.simpson@springface.com', password='test')

    def test_csrf(self):
        url = reverse('board_topics_new', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')


    # def test_new_topic_valid_post_data(self):
    #     url = reverse('board_topics_new', kwargs={'pk': 1})
    #     data = {
    #         'subject': 'test test',
    #         'text': 'text text text message'
    #     }
    #     response = self.client.post(url, data)
    #     self.assertTrue(Topic.objects.exists())
    #     self.assertTrue(Message.objects.exists())

    def test_new_topic_invalid_post_data(self):
        url = reverse('board_topics_new', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)


    def test_new_topic_invalid_post_data_empty_fields(self):
        url = reverse('board_topics_new', kwargs={'pk': 1})
        data = {
            'subject': '',
            'text': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Message.objects.exists())


    def test_contains_form(self):  # <- new test
        url = reverse('board_topics_new', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    def test_new_topic_invalid_post_data(self):  # <- updated this one
        url = reverse('board_topics_new', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)
