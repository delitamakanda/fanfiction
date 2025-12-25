from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

class SystemInfoAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:system')
        self.user = get_user_model().objects.create_superuser(username="testuser", email="testuser@example.com", password="testuser123")

    def test_system_info_requires_admin_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_system_info_with_admin_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('status', response.data)
        self.assertIn('timestamp', response.data)
        self.assertIn('uptime_server', response.data)
        self.assertIn('python', response.data)

    def test_system_info_contains_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertIn('uptime_server', response.data)

    def test_system_info_contains_database_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertIn('database', response.data)
        self.assertIn('connected', response.data['database'])
