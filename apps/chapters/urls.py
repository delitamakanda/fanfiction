from django.urls import path

from apps.chapters.api import views

app_name = "chapters"

urlpatterns = [
    path(
        "<int:fanfic>/list/",
        views.ChapterListApiView.as_view(),
        name="chapter-list-by-fanfic",
    ),
    path("create/", views.ChapterCreateApiView.as_view(), name="chapter-create"),
    path("<int:pk>/", views.ChapterDetailView.as_view(), name="chapter-detail"),
    path("generate", views.GenerateSummaryView.as_view(), name="generate"),
    path("styles", views.SummaryStylesView.as_view(), name="styles-prompts"),
    path("<int:fanfic>/autosave", views.AutosaveChapterView.as_view(), name="autosave"),
]
