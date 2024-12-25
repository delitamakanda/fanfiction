from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from rest_framework.routers import DefaultRouter

from accounts.api.views import (
    UserFanficDetailView,
    UserDetailView,
    AccountProfileDetailView,
    SocialListApiView,
    SocialDestroyApiView,
    GroupListView,
    SignupView,
    FavoritedFanficView,
    UnfavoritedFanficView,
    FollowUserView,
    postFollowAuthor,
    unFollowAuthor,
    FollowStoriesView,
    DeleteAccountView,
    FollowAuthorDeleteView,
    FollowStoriesDeleteView,
CheckoutUserView,
    UserCreateView,
    LoginView,
    LogoutView,
    SocialSignUp,
    ChangePasswordView,
    RemovePhotoFromAccount,
	ContactMailView,
	ContentTypeView,
	NotificationListView,
PasswordResetView,
)

routers = DefaultRouter()

urlpatterns = [
path('users/<str:username>/account/',
         UserFanficDetailView.as_view(), name='user-list'),
    path('users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('users/<str:user__username>/profile/',
         AccountProfileDetailView.as_view(), name='user-edit-account-profile'),
    path('users/<int:account>/socialaccount/',
         SocialListApiView.as_view(), name='socialaccount-view'),
    path('users/social-account/', SocialListApiView.as_view(),
         name='socialaccount-createview'),
    path('users/social-account/<int:pk>/delete/',
         SocialDestroyApiView.as_view(), name='socialaccount-destroy'),
    path('groups/', GroupListView.as_view()),
    path('sign_up/', SignupView.as_view(), name="sign_up"),
	path('favorite/', FavoritedFanficView.as_view(), name='favorite'),
    path('unfavorite/', UnfavoritedFanficView.as_view(), name='unfavorite'),
    path('follow-stories/<str:username>/', FollowStoriesView.as_view(), name='follow-stories'),
    path('follow-user/<str:username>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow-user/<str:user_from__username>/', unFollowAuthor.as_view(), name='unfollow-user'),
    path('follow-user/', postFollowAuthor.as_view(), name='post-follow-user'),

    path('story-followed/<int:to_fanfic>/', FollowStoriesDeleteView.as_view()),
    path('author-followed/<int:user_to>/', FollowAuthorDeleteView.as_view()),

    path('disable-account/', DeleteAccountView.as_view(), name='disable-account'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('old-logout/', auth_views.LogoutView.as_view(), {'next_page': reverse_lazy('index')}, name='logout_auth'),
path('user/', CheckoutUserView.as_view(), name='user'),
	path('signup/', UserCreateView.as_view(), name='signup'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('social_sign_up/', SocialSignUp.as_view(), name="social_sign_up"),
	path('change-password/', ChangePasswordView.as_view(),
		 name='change-password'),
	path('remove-photo/<int:pk>/',
		 RemovePhotoFromAccount.as_view(), name='remove-photo'),
path('contact-mail/', ContactMailView.as_view(), name='contact-mail'),
	path('notifications/', NotificationListView.as_view(), name='notifications'),
	path('contenttype/<int:pk>/',
		 ContentTypeView.as_view(), name='contenttype-detail'),
	path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
]

urlpatterns += routers.urls
