from django.urls import path

from api.views import (
    ApiRootView,
)

from api.api import (
    EmailFeedbackView,
    ContactMailView,
    FlatPagesView,
    FlatPagesByTypeView,
    FlatPagesHTMLByTypeView,
    ContentTypeView,
    NotificationListView,
)

from api.api_fanfic import (
    ShareFanficAPIView,
)

from api.api_auth import (
    CheckoutUserView,
    UserCreateView,
    LoginView,
    LogoutView,
    SocialSignUp,
    ChangePasswordView,
    RemovePhotoFromAccount,
)

urlpatterns = [
	path('', ApiRootView.as_view(), name=ApiRootView.name),

	path('user/', CheckoutUserView.as_view(), name='user'),
	path('signup/', UserCreateView.as_view(), name='signup'),
	path('login/', LoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('social_sign_up/', SocialSignUp.as_view(), name="social_sign_up"),
	path('change-password/', ChangePasswordView.as_view(),
		 name='change-password'),
	path('remove-photo/<int:pk>/',
		 RemovePhotoFromAccount.as_view(), name='remove-photo'),

	path('share/', ShareFanficAPIView.as_view(), name='share'),

	path('feedback/', EmailFeedbackView.as_view(), name='feedback'),

	path('contact-mail/', ContactMailView.as_view(), name='contact-mail'),
	path('pages/<str:type>/',
		 FlatPagesByTypeView.as_view(), name='pages-by-type'),
	path('pages/<str:type>/html/',
		 FlatPagesHTMLByTypeView.as_view(), name='pages-html-by-type'),
	path('pages/', FlatPagesView.as_view(), name='all-pages'),
	path('notifications/', NotificationListView.as_view(), name='notifications'),
	path('contenttype/<int:pk>/',
		 ContentTypeView.as_view(), name='contenttype-detail'),
]
