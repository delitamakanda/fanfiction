from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.accounts.api import views

app_name = "accounts"

urlpatterns = [
    # Authentication (JWT)
    path("signup/", views.SignupView.as_view(), name="sign_up"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("password-reset/", views.PasswordResetView.as_view(), name="password-reset"),
    path(
        "password-reset/<uidb64>/<token>/",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    # Current user
    path("user/", views.CheckoutUserView.as_view(), name="user"),
    path("consent/", views.AcceptRecoConsentView.as_view(), name="accept-reco-consent"),
    path("disable/", views.DeleteAccountView.as_view(), name="disable-account"),
    path("social/", views.SocialCreateApiView.as_view(), name="socialaccount-create"),
    path(
        "social/<int:pk>/",
        views.SocialDestroyApiView.as_view(),
        name="socialaccount-update-destroy",
    ),
    # Social features
    path("like/", views.FanficLikeAPIView.as_view(), name="like-fanfic-api"),
    path("follow-author/", views.FollowAuthorAPIView.as_view(), name="follow-author"),
    path("follow-story/", views.FollowStoriesAPIView.as_view(), name="follow-story"),
    path("notifications/", views.NotificationListView.as_view(), name="notifications"),
    path("contact-mail/", views.ContactMailView.as_view(), name="contact-mail"),
    # Server-rendered password reset pages (django.contrib.auth)
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("api:accounts:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password_reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("api:accounts:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
