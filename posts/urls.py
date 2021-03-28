from django.urls import path
from posts import views

urlpatterns = [
    path('list', views.PostsListView.as_view(), name='list-posts'),
    path('fake', views.generate_fake_data, name='generate_fake_data'),
]
