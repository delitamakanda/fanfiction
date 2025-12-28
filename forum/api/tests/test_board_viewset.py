from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from forum.models import Board, Topic


User = get_user_model()

class BoardAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testuser123')
        self.board = Board.objects.create(name='Test Board', description='Test board for testing purposes')
        self.url = '/api/forum/boards/'

    def test_list_boards(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], self.board.name)

    def test_retrieve_board(self):
        response = self.client.get(f'{self.url}{self.board.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.board.name)

    def test_create_board_requires_authentication(self):
        response = self.client.post(self.url, {'name': 'New Board', 'description': 'New board for testing purposes'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_board_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {'name': 'New Board', 'description': 'New board for testing purposes'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Board')

    def test_board_topics_action(self):
        topic = Topic.objects.create(board=self.board, subject='Test Topic', starter=self.user)
        response = self.client.get(f'{self.url}{self.board.pk}/topics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subject'], topic.subject)



