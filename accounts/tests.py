from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from accounts.models import FollowUser, Notification

URL = '/api/v1/accounts/notifications/'


class NotificationCursorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create_user('reader', password='x')
        cls.author = User.objects.create_user('author', password='x')
        cls.stranger = User.objects.create_user('stranger', password='x')
        FollowUser.objects.create(user_from=cls.reader, user_to=cls.author)
        for i in range(25):
            Notification.objects.create(user=cls.author, verb=f'v{i}')
        Notification.objects.create(user=cls.stranger, verb='hidden')

    def client_for(self, user):
        client = APIClient()
        client.force_authenticate(user)
        return client

    def test_requires_authentication(self):
        self.assertIn(APIClient().get(URL).status_code, (401, 403))

    def test_cursor_pages_have_no_duplicates_nor_gaps(self):
        client = self.client_for(self.reader)
        first = client.get(URL)
        self.assertEqual(first.status_code, 200)
        self.assertNotIn('count', first.data)
        self.assertEqual(len(first.data['results']), 20)
        ids = [n['id'] for n in first.data['results']]

        # A new notification between two pages must not shift the next page.
        Notification.objects.create(user=self.author, verb='late')
        second = client.get(first.data['next'])
        self.assertEqual(second.status_code, 200)
        ids += [n['id'] for n in second.data['results']]
        self.assertEqual(len(ids), 25)
        self.assertEqual(len(set(ids)), 25)
        self.assertIsNone(second.data['next'])

    def test_user_does_not_see_other_notifications(self):
        response = self.client_for(self.stranger).get(URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'], [])

    def test_invalid_cursor_is_404(self):
        self.assertEqual(self.client_for(self.reader).get(URL, {'cursor': 'zzz'}).status_code, 404)
