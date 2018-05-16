from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('password_reset/', auth_views.password_reset, name='password_reset'),
    path('^password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    path('^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', auth_views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]
