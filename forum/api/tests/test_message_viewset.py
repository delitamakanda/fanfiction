from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from forum.models import Message, Board, Topic

User = get_user_model()

class MessageAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testuser123')
        self.board = Board.objects.create(name='Test Board', description='Test board for testing purposes')
        self.topic = Topic.objects.create(board=self.board, subject='Test Topic', starter=self.user)
        self.message = Message.objects.create(topic=self.topic, text='Test Message', created_by=self.user)
        self.url = '/api/forum/messages/'

    def test_list_messages(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['text'], self.message.text)

    def test_retrieve_message(self):
        response = self.client.get(f'{self.url}{self.message.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.message.text)

    def test_create_message_requires_authentication(self):
        response = self.client.post(self.url, {'text': 'New Message', 'topic': self.topic.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_message_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'text': 'New Message', 'topic': self.topic.pk, 'created_by': self.user.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 2)

    def test_message_author_is_current_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'text': 'New Message', 'topic': self.topic.pk, 'created_by': self.user.pk})
        self.assertEqual(response.data['created_by'], self.user.pk)

    def test_update_message_by_creator(self):
        """Test that the message creator can update their own message"""
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(f'{self.url}{self.message.pk}/', {'text': 'Updated Message'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertEqual(self.message.text, 'Updated Message')

    def test_update_message_by_non_creator(self):
        """Test that non-creator authenticated users cannot update messages"""
        other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='other123')
        self.client.force_authenticate(user=other_user)
        response = self.client.patch(f'{self.url}{self.message.pk}/', {'text': 'Hacked Message'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.message.refresh_from_db()
        self.assertEqual(self.message.text, 'Test Message')

    def test_delete_message_by_creator(self):
        """Test that the message creator can delete their own message"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'{self.url}{self.message.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Message.objects.count(), 0)

    def test_delete_message_by_non_creator(self):
        """Test that non-creator authenticated users cannot delete messages"""
        other_user = User.objects.create_user(username='otheruser', email='other@example.com', password='other123')
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(f'{self.url}{self.message.pk}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Message.objects.count(), 1)




