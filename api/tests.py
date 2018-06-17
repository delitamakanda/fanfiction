from django.test import TestCase
from django.urls import reverse
from django.utils.six import BytesIO
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from api.serializers import CommentSerializer
from api.models import Fanfic
from api.models import Comment
from api import views

# Create your tests here.

# class FanficTests(APITestCase):
#
#     def post_fanfic(self, title):
#         url = reverse('fanfic-list')
#         data = {'title': title}
#         response = self.client.post(url, data, format='json')
#         return response
#
#     def test_post_and_get_fanfic(self):
#          """
#          Ensure we can create a new Fanfic and then retrieve it
#          """
#          new_fanfic = 'A Story'
#          response = self.post_fanfic(new_fanfic)
#          print("ID {0}".format(Fanfic.objects.get().id))
#          assert response.status_code == status.HTTP_201_CREATED
#          assert Fanfic.objects.count() == 1
#          assert Fanfic.objects.get().title == new_fanfic
#
#
# class CommentSerializerTests(TestCase):
#   @classmethod
#   def setUpTestData(cls):
#     cls.c = Comment(author="test", email="test@test.com", body="test body")
#     cls.c.save()
