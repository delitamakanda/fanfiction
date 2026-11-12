from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from rest_framework import status
from rest_framework.test import APITestCase

from apps.helpcenter.models import FoireAuxQuestions, Lexique


class HelpCenterApiTests(APITestCase):
    def setUp(self):
        FoireAuxQuestions.objects.create(
            libelle="sit", question="Comment ?", reponse="**Ainsi**"
        )
        Lexique.objects.create(title="Drabble", definition="Texte de 100 mots")
        Lexique.objects.create(title="Fandom", definition="Communauté de fans")

    def test_faq(self):
        response = self.client.get("/api/v1/help/faq/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["libelle"], "Le site")

    def test_lexique_search(self):
        response = self.client.get("/api/v1/help/lexique/", {"q": "fans"})
        self.assertEqual([w["title"] for w in response.data["results"]], ["Fandom"])

    def test_read_only(self):
        response = self.client.post(
            "/api/v1/help/lexique/", {"title": "x", "definition": "y"}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_flatpages(self):
        page = FlatPage.objects.create(
            url="/legal/", title="Mentions légales", content="..."
        )
        page.sites.add(Site.objects.get_current())
        response = self.client.get("/api/v1/help/pages/")
        self.assertEqual(response.data["results"][0]["title"], "Mentions légales")

    def test_server_rendered_pages(self):
        response = self.client.get("/api/v1/help/foire-aux-questions")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "<strong>Ainsi</strong>", html=True)
        response = self.client.get("/api/v1/help/browse/title/D")
        self.assertContains(response, "Drabble")
        self.assertNotContains(response, "Fandom")
        response = self.client.post(
            "/api/v1/help/search-ajax-submit", {"search": "fan"}
        )
        self.assertContains(response, "Fandom")
