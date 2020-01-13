from django.urls import path

from fanfics.api import views as fanfic_views

urlpatterns = [
    path('genres/', fanfic_views.GenresListView.as_view(), name='genre-list'),
    path('fanfics/', fanfic_views.FanficCreateApiView.as_view(), name='fanfic-list'),
    path('fanfics/<str:username>', fanfic_views.FanficCreateApiView.as_view(), name='fanfic-list-by-author'),
    path('fanfics/<str:slug>/detail', fanfic_views.FanficDetailView.as_view(), name='fanfic-detail'),
]