from django.urls import path
from chapters.api.views import (
     ChapterListApiView,
     ChapterCreateApiView,
     ChapterDetailView
)

urlpatterns = [
path('<int:fanfic>/list/',
         ChapterListApiView.as_view(), name='chapter-list-by-fanfic'),
    path('create/', ChapterCreateApiView.as_view(), name='chapter-create'),
    path('<int:pk>/',
         ChapterDetailView.as_view(), name='chapter-detail'),
]
