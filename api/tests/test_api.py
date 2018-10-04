from django.test import TestCase
from django.urls import reverse
from django.utils.six import BytesIO
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api.serializers import CommentSerializer
from api.serializers import FanficListSerializer
from api.serializers import FanficSerializer

from api.models import Fanfic
from api.models import Comment
from api.models import Category
from api.models import SubCategory

from api import views
from api import views_fanfic
from api import views_post

# Create your tests here.

class TestPost(APITestCase):
    """
    Tests for post
    """

    def setUp(self):
        self.user = self.setup_user()
        self.factory = APIRequestFactory()
        self.view = views_post.PostList.as_view()
        self.uri = '/api/posts'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='test@email.com',
            password='test'
        )

    def test_post_list(self):
        request = self.factory.get(self.uri)
        request.user = self.user
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                        'Expected Response Code 200, received {0} instead.'
                        .format(response.status_code))


class TestFanfic(APITestCase):
    """
    Tests for fanfics
    """

    def setUp(self):
        self.user = self.setup_user()
        self.client = APIClient()
        self.view = views_fanfic.FanficCreateView.as_view()
        self.uri = '/api/fanfics'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='test@email.com',
            password='test'
        )

    def test_list(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200,
                        'Expected Response Code 200, received {0} instead.'
                        .format(response.status_code))


class TestCategory(APITestCase):
    """
    Tests for categories
    """

    def setUp(self):
        self.user = self.setup_user()
        self.client = APIClient()
        self.view = views.CategoryList.as_view()
        self.uri = '/api/category'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='test@email.com',
            password='test'
        )

    def test_create(self):
        self.client.login(username='test', password='test')
        params = {
            "name": "Animes-Mangas",
            "slug": "animers-mangas"
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201,
                        'Expected Response Code 201, received {0} instead.'
                        .format(response.status_code))
