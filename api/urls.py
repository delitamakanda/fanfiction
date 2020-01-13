from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from rest_framework.documentation import include_docs_urls
from api import views
from api import api as api_core
from api import api_auth

urlpatterns = [
    path('user', api_auth.CheckoutUserView.as_view(), name='user'),
    path('signup', api_auth.UserCreateView.as_view(), name='signup'),
    path('login', api_auth.LoginView.as_view(), name='login'),
    path('logout', api_auth.LogoutView.as_view(), name='logout'),
    path('social_sign_up', api_auth.SocialSignUp.as_view(), name="social_sign_up"),
    path('change-password', api_auth.ChangePasswordView.as_view(), name='change-password'),
    path('remove-photo/<int:pk>', api_auth.RemovePhotoFromAccount.as_view(), name='remove-photo'),

    path('feedback', api_core.EmailFeedbackView.as_view(), name='feedback'),
    path('favorite', api_core.FavoritedFanficView.as_view(), name='favorite'),
    path('unfavorite', api_core.UnfavoritedFanficView.as_view(), name='unfavorite'),
    path('follow-stories', api_core.FollowStoriesView.as_view(), name='follow-stories'),
    path('follow-user', api_core.FollowUserView.as_view(), name='follow-user'),
    path('disable-account', api_core.DeleteAccountView.as_view(), name='disable-account'),
    path('contact-mail', api_core.ContactMailView.as_view(), name='contact-mail'),
    
    path('pages/<str:type>', views.FlatPagesByTypeView.as_view(), name='pages-by-type'),
    path('page/<str:type>/html', views.FlatPagesHTMLByTypeView.as_view(), name='pages-html-by-type'),
    path('pages', views.FlatPagesView.as_view(), name='all-pages'),
    path('notifications', views.NotificationListView.as_view(), name='notifications'),
    path('contenttype/<int:pk>', views.ContentTypeView.as_view(), name='contenttype-detail'),
    

    path('fanfics/', include('fanfics.api.urls')),
    path('chapters/', include('chapters.api.urls')),
    path('reviews/', include('comments.api.urls')),
    path('help/', include('helpcenter.api.urls')),
    path('news/', include('posts.api.urls')),
    path('auth/', include('accounts.api.urls')),
    path('categories/', include('categories.api.urls')),

    path('docs', include_docs_urls(title='Fanfiction API', public=True)),
    path('', views.ApiRootView.as_view(), name=views.ApiRootView.name),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
