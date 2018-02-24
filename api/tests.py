from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Fanfic
from api import views
# Create your tests here.

class FanficTests(APITestCase):

    def post_fanfic(self, title):
        url = reverse('fanfic-list')
        data = {'title': title}
        response = self.client.post(url, data, format='json')
        return response

    # def test_post_and_get_fanfic(self):
    #     """
    #     Ensure we can create a new Fanfic and then retrieve it
    #     """
    #     new_fanfic = 'A Story'
    #     response = self.post_fanfic(new_fanfic)
    #     print("ID {0}".format(Fanfic.objects.get().id))
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert Fanfic.objects.count() == 1
    #     assert Fanfic.objects.get().title == new_fanfic
