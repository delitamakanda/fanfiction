from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.testing import make_user
from apps.posts.models import Post, Tag

URL = "/api/v1/posts/"


class PostApiTests(APITestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user("redac", is_staff=True)
        self.post = Post.objects.create(
            user=self.staff, title="Nouveautés", content="# Hello"
        )
        self.post.tags.add(Tag.objects.create(word="news"))

    def test_list_and_detail_shape_used_by_the_front(self):
        response = self.client.get(URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post = response.data["results"][0]
        self.assertEqual(post["username_author"], "redac")
        self.assertEqual(post["tags"], ["news"])
        response = self.client.get(f"{URL}{self.post.slug}/")
        self.assertEqual(response.data["title"], "Nouveautés")

    def test_create_with_tags(self):
        self.client.force_authenticate(make_user())
        response = self.client.post(
            URL,
            {
                "title": "Mon tuto",
                "content": "...",
                "category": "TU",
                "tags": ["aide", "news"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sorted(response.data["tags"]), ["aide", "news"])
        self.assertEqual(Tag.objects.count(), 2)

    def test_permissions(self):
        response = self.client.post(URL, {"title": "Anonyme", "content": "x"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(make_user())
        response = self.client.patch(f"{URL}{self.post.slug}/", {"title": "Piraté"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(self.staff)
        response = self.client.patch(f"{URL}{self.post.slug}/", {"title": "Corrigé"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_validation(self):
        self.client.force_authenticate(make_user())
        response = self.client.post(URL, {"title": "", "content": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
