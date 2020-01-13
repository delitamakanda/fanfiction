from django.urls import path
from accounts.api import views as views_user

urlpatterns = [    
    path('users/<str:user__username>/account', views_user.UserFanficDetailView.as_view(), name='user-list'),
    path('users/<int:pk>', views_user.UserDetailView.as_view(), name='user-detail'),

    path('users/<str:user__username>/profile', views_user.AccountProfileDetailView.as_view(), name='user-edit-account-profile'),

    path('users/<int:account>/socialaccount', views_user.SocialListApiView.as_view(), name='socialaccount-view'),
    path('users/social-account', views_user.SocialListApiView.as_view(), name='socialaccount-createview'),
]