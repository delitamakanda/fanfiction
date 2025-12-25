from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class HealthAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:health')

    def test_health_endpoint_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check_returns_ok_status(self):
        response = self.client.get(self.url)
        self.assertEqual(response.data['status'], 'ok')

    def test_health_check_contains_timestamp(self):
        response = self.client.get(self.url)
        self.assertIn('timestamp', response.data)

    def test_health_check_contains_service(self):
        response = self.client.get(self.url)
        self.assertIn('service', response.data)
        self.assertEqual(response.data['service'], 'fanfiction-api')


class DetailedHealthAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:health-detailed')

    def test_detailed_health_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_detailed_health_with_admin_permissions(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        self.client.force_authenticate(user=admin_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('checks', response.data)
        self.assertIn('database', response.data['checks'])
