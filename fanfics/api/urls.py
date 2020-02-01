from django.urls import path

from fanfics.api import views as fanfic_views

urlpatterns = [
    path('genres/', fanfic_views.GenresListView.as_view(), name='genre-list'),
    path('classement/', fanfic_views.ClassementListView.as_view(), name='classement-list'),
    path('status/', fanfic_views.StatusListView.as_view(), name='status-list'),
    path('fanfics/', fanfic_views.FanficCreateApiView.as_view(), name='fanfic-list'),
    path('fanfics/<str:username>', fanfic_views.FanficCreateApiView.as_view(), name='fanfic-list-by-author'),
    path('fanfics/<str:slug>/detail', fanfic_views.FanficDetailView.as_view(), name='fanfic-detail'),
    path('fanfics/<int:pk>/fanfic-detail', fanfic_views.FanficUpdateDetailView.as_view(), name='fanfic-update-detail'),
]