from rest_framework.test import APIClient, APITestCase
from forum.models import Topic, Board, Message
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class TopicAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testuser123')
        self.board = Board.objects.create(name='Test Board', description='Test board for testing purposes')
        self.topic = Topic.objects.create(board=self.board, subject='Test Topic', starter=self.user)
        self.url = '/api/forum/topics/'

    def test_list_topics(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_topic(self):
        response = self.client.get(f'{self.url}{self.topic.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['subject'], self.topic.subject)

    def test_create_topic_requires_authentication(self):
        response = self.client.post(self.url, {'subject': 'New Topic', 'board': self.board.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_topic_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'subject': 'New Topic', 'board': self.board.pk, 'starter': self.user.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 2)

    def test_update_topic_requires_authentication(self):
        response = self.client.put(f'{self.url}{self.topic.pk}/', {'subject': 'Updated Topic'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_topic_messages_action(self):
        message = Message.objects.create(topic=self.topic, text='Test Message', created_by=self.user)
        response = self.client.get(f'{self.url}{self.topic.pk}/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['text'], message.text)




