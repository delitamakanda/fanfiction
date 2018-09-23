from django.test import TestCase
from django.urls import reverse
from django.utils.six import BytesIO
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from api.serializers import CommentSerializer
from api.serializers import FanficListSerializer
from api.serializers import FanficSerializer

from api.models import Fanfic
from api.models import Comment

from api import views
from api import views_fanfic

# Create your tests here.

class TestFanficList(APITestCase):
    """
    Tests for fanfics
    """

    def setUp(self):
        self.user = self.setup_user()
        self.factory = APIRequestFactory()
        self.view = views_fanfic.FanficListRemasteredView.as_view()
        self.uri = '/api/fanfics/v1/'

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='test@email.com',
            password='test'
        )

    def test_fanfic_list(self):
        request = self.factory.get(self.uri)
        response = self.view(request)
        self.assertEqual(response.status_code, 200,
                        'Expected Response Code 200, received {0} instead.'
                        .format(response.status_code))
