from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.categories.models import Category, EntityCategory, SubCategory
from apps.core.testing import make_user


class CategoryApiTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Animes-Mangas")
        self.subcategory = SubCategory.objects.create(
            name="One Piece", category=self.category
        )
        EntityCategory.objects.create(subcategory=self.subcategory, entity="Luffy")

    def test_list_categories(self):
        response = self.client.get("/api/v1/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["slug"], "animes-mangas")

    def test_all_subcategories_used_by_the_front(self):
        response = self.client.get("/api/v1/categories/subcategory/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data["results"][0]
        self.assertEqual(result["slug"], "one-piece")
        self.assertEqual(result["category"]["slug"], "animes-mangas")

    def test_subcategories_of_a_category(self):
        response = self.client.get("/api/v1/categories/animes-mangas/subcategories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_subcategory_detail_and_entities(self):
        response = self.client.get("/api/v1/categories/animes-mangas/one-piece/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "One Piece")
        response = self.client.get(
            "/api/v1/categories/animes-mangas/one-piece/entities/"
        )
        self.assertEqual(response.data["results"][0]["entity"], "Luffy")

    def test_anonymous_and_regular_users_cannot_write(self):
        response = self.client.post("/api/v1/categories/", {"name": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.force_authenticate(make_user())
        response = self.client.delete("/api/v1/categories/animes-mangas/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Category.objects.filter(pk=self.category.pk).exists())

    def test_staff_can_create_a_category_without_slug(self):
        staff = get_user_model().objects.create_user("staff", is_staff=True)
        self.client.force_authenticate(staff)
        response = self.client.post("/api/v1/categories/", {"name": "Films-Séries TV"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["slug"], "films-series-tv")
