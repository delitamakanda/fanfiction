from django.urls import path, include
from help import views

urlpatterns = [
    path('browse/title', views.browse_by_title, name='browse'),
    path('browse/title/<str:initial>', views.browse_by_title, name='browse_by_title'),
]
