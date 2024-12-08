from django.urls import path

from fanfics.api.views import (
    GenresListView,
    ClassementListView,
    StatusListView,
    FanficCreateApiView,
    FanficListApiView,
    FanficDetailView,
    FanficUpdateDetailView,
)

from fanfics.views import fanfic_detail

urlpatterns = [
path('genres/', GenresListView.as_view(), name='genre-list'),
    path('classement/', ClassementListView.as_view(), name='classement-list'),
    path('status/', StatusListView.as_view(), name='status-list'),
    path('', FanficListApiView.as_view(), name='fanfic-list'),
    path('fanfics-create/', FanficCreateApiView.as_view(), name='fanfic-create'),
    path('fanfics/<str:author>/',
         FanficListApiView.as_view(), name='fanfic-list-by-author'),
    path('fanfics/<str:slug>/detail/',
         FanficDetailView.as_view(), name='fanfic-detail'),
    path('fanfics/<int:pk>/fanfic-detail/',
         FanficUpdateDetailView.as_view(), name='fanfic-update-detail'),
	path('fanfic/<int:id>/<str:slug>/', fanfic_detail, name='fanfic_detail'),
]
