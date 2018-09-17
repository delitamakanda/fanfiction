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

# Create your tests here.

class FanficTests(APITestCase):
  """
  Tests for fanfics
  """
  pass
