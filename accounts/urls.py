from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from rest_framework.routers import DefaultRouter

from accounts.api.views import (
	SocialCreateApiView,
	SocialDestroyApiView,
	SignupView,
FanficLikeAPIView,
	FollowUserView,
	PostFollowAuthor,
	UnFollowAuthor,
	FollowStoriesView,
	DeleteAccountView,
	FollowAuthorDeleteView,
	FollowStoriesDeleteView,
	CheckoutUserView,
	LogoutView,
	ChangePasswordView,
	ContactMailView,
	NotificationListView,
	PasswordResetView,
	PasswordResetConfirmView,
)

app_name = 'accounts'

routers = DefaultRouter()

AUTHENTICATION_ROUTES = [
	path('password_reset/',
		 auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')),
		 name='password_reset'),
	path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset/<uidb64>/<token>/',
		 auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')),
		 name='password_reset_confirm'),
	path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

PROFILE_ROUTES = []

FOLLOW_ROUTES = []

urlpatterns = [
	path('social/', SocialCreateApiView.as_view(), name='socialaccount-create'),
	path('social/<int:pk>/',
		 SocialDestroyApiView.as_view(), name='socialaccount-update-destroy'),
	path('signup/', SignupView.as_view(), name="sign_up"),
	path('like/', FanficLikeAPIView.as_view(), name='like-fanfic-api'),
	path('follow-stories/<str:username>/', FollowStoriesView.as_view(), name='follow-stories'),
	path('follow-user/<str:username>/', FollowUserView.as_view(), name='follow-user'),
	path('unfollow-user/<str:user_from__username>/', UnFollowAuthor.as_view(), name='unfollow-user'),
	path('follow-user/', PostFollowAuthor.as_view(), name='post-follow-user'),
	path('story-followed/<int:to_fanfic>/', FollowStoriesDeleteView.as_view()),
	path('author-followed/<int:user_to>/', FollowAuthorDeleteView.as_view()),

	path('disable/', DeleteAccountView.as_view(), name='disable-account'),
	path('user/', CheckoutUserView.as_view(), name='user'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('change-password/', ChangePasswordView.as_view(),
		 name='change-password'),
	path('contact-mail/', ContactMailView.as_view(), name='contact-mail'),
	path('notifications/', NotificationListView.as_view(), name='notifications'),
	path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
	path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]

urlpatterns += routers.urls
urlpatterns += AUTHENTICATION_ROUTES
