from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class ApiRootTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api:root')

    def test_api_root_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_root_contains_endpoints(self):
        response = self.client.get(self.url)
        self.assertIn('faq', response.data)
        self.assertIn('health', response.data)
        self.assertIn('posts', response.data)
        self.assertIn('categories', response.data)


    def test_api_root_documentation_lins(self):
        response = self.client.get(self.url)
        self.assertIn('documentation', response.data)
        self.assertIn('swagger', response.data['documentation'])
        self.assertIn('redoc', response.data['documentation'])
