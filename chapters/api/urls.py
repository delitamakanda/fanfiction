from django.urls import path
from chapters.api import views as chapter_views

urlpatterns = [
    path('chapters/<int:fanfic>/list', chapter_views.ChapterCreateApiView.as_view(), name='chapter-list-by-fanfic'),
    path('chapters/create', chapter_views.ChapterCreateApiView.as_view(), name='chapter-list'),
    path('chapters/<int:pk>', chapter_views.ChapterDetailView.as_view(), name='chapter-detail'),
]