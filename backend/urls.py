"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_page
from markdownx import urls as markdownx

from rest_framework_simplejwt import views as jwt_views
from rest_framework.documentation import include_docs_urls

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
    FollowStoriesView,
    DeleteAccountView,
    FollowAuthorDeleteView,
    FollowStoriesDeleteView,
)

from helpcenter.api.views import (
    FoireAuxQuestionsApiView,
    LexiqueApiView,
)

from categories.api.views import (
    CategoryDetailView,
    CategoryListView,
    SubCategoryDetailView,
    SubCategoryListView,
)

from posts.api.views import (
    PostCreateAPIView,
    PostDetailAPIView,
    PostListAPIView,
    PostUpdateAPIView,
    TagListAPIView,
)

from fanfics.api.views import (
    GenresListView,
    ClassementListView,
    StatusListView,
    FanficCreateApiView,
    FanficListApiView,
    FanficDetailView,
    FanficUpdateDetailView,
)

from comments.api.views import (
    CommentCreateApiView,
    CommentListApiView,
)

from chapters.api.views import (
    ChapterCreateApiView,
    ChapterDetailView
)

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
    BrowseFanfictionListView,
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
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('help/', include(('helpcenter.urls', 'helpcenter'), namespace='helpcenter')),
    path('posts/', include(('posts.urls', 'posts'), namespace='posts')),
    path('offline.html', (TemplateView.as_view(template_name="offline.html")), name='offline.html'),
    # path('', cache_page(60 * 5)(TemplateView.as_view(
    #     template_name='frontend/index.html')), name='index'),
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='index'),
    path('service-worker.js', (TemplateView.as_view(template_name="pwa/service-worker.js", content_type='application/javascript', )), name='service-worker.js'),
]

urlpatterns += [
    path('api/', ApiRootView.as_view(), name=ApiRootView.name),
    path('api/docs/', include_docs_urls(title='Fanfiction API', public=False)),

    path('api/user/', CheckoutUserView.as_view(), name='user'),
    path('api/signup/', UserCreateView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/social_sign_up/', SocialSignUp.as_view(), name="social_sign_up"),
    path('api/change-password/', ChangePasswordView.as_view(),
         name='change-password'),
    path('api/remove-photo/<int:pk>/',
         RemovePhotoFromAccount.as_view(), name='remove-photo'),

    path('api/share/', ShareFanficAPIView.as_view(), name='share'),

    path('api/feedback/', EmailFeedbackView.as_view(), name='feedback'),
    path('api/favorite/', FavoritedFanficView.as_view(), name='favorite'),
    path('api/unfavorite/', UnfavoritedFanficView.as_view(), name='unfavorite'),
    path('api/follow-stories/<str:username>/', FollowStoriesView.as_view(), name='follow-stories'),
    path('api/follow-user/<str:username>/', FollowUserView.as_view(), name='follow-user'),

    path('api/story-followed/<int:to_fanfic>/', FollowStoriesDeleteView.as_view()),
    path('api/author-followed/<int:user_to>/', FollowAuthorDeleteView.as_view()),

    path('api/disable-account/', DeleteAccountView.as_view(), name='disable-account'),
    path('api/contact-mail/', ContactMailView.as_view(), name='contact-mail'),
    path('api/pages/<str:type>/',
         FlatPagesByTypeView.as_view(), name='pages-by-type'),
    path('api/pages/<str:type>/html/',
         FlatPagesHTMLByTypeView.as_view(), name='pages-html-by-type'),
    path('api/pages/', FlatPagesView.as_view(), name='all-pages'),
    path('api/notifications/', NotificationListView.as_view(), name='notifications'),
    path('api/contenttype/<int:pk>/',
         ContentTypeView.as_view(), name='contenttype-detail'),
    path('api/browse-fanfics/',
         BrowseFanfictionListView.as_view(), name='browse-fanfics'),

    path('api/users/<str:username>/account/',
         UserFanficDetailView.as_view(), name='user-list'),
    path('api/users/<str:username>/', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<str:user__username>/profile/',
         AccountProfileDetailView.as_view(), name='user-edit-account-profile'),
    path('api/users/<int:account>/socialaccount/',
         SocialListApiView.as_view(), name='socialaccount-view'),
    path('api/users/social-account/', SocialListApiView.as_view(),
         name='socialaccount-createview'),
    path('api/users/social-account/<int:pk>/delete/',
         SocialDestroyApiView.as_view(), name='socialaccount-destroy'),
    path('api/groups/', GroupListView.as_view()),
    path('api/sign_up/', SignupView.as_view(), name="sign_up"),

    path('api/faq/', FoireAuxQuestionsApiView.as_view(), name='faq'),
    path('api/lexique/', LexiqueApiView.as_view(), name='lexique'),

    path('api/category/', CategoryListView.as_view(), name='category-list'),
    path('api/category/<int:pk>/',
         CategoryDetailView.as_view(), name='category-detail'),
    path('api/subcategory/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('api/subcategory/<int:pk>/',
         SubCategoryDetailView.as_view(), name='subcategory-detail'),

    path('api/tags/', TagListAPIView.as_view(), name='tag-list'),
    path('api/posts/', PostListAPIView.as_view(), name='post-list'),
    path('api/posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('api/posts/<int:pk>/update/',
         PostUpdateAPIView.as_view(), name='post-update'),
    path('api/posts/<int:pk>/remove/',
         PostUpdateAPIView.as_view(), name='post-delete'),
    path('api/posts/<str:slug>/', PostDetailAPIView.as_view(), name='post-detail'),

    path('api/genres/', GenresListView.as_view(), name='genre-list'),
    path('api/classement/', ClassementListView.as_view(), name='classement-list'),
    path('api/status/', StatusListView.as_view(), name='status-list'),
    path('api/fanfics/', FanficListApiView.as_view(), name='fanfic-list'),
    path('api/fanfics-create/', FanficCreateApiView.as_view(), name='fanfic-create'),
    path('api/fanfics/<str:author>/',
         FanficListApiView.as_view(), name='fanfic-list-by-author'),
    path('api/fanfics/<str:slug>/detail/',
         FanficDetailView.as_view(), name='fanfic-detail'),
    path('api/fanfics/<int:pk>/fanfic-detail/',
         FanficUpdateDetailView.as_view(), name='fanfic-update-detail'),

    path('api/comments/', CommentCreateApiView.as_view(), name='comment-create'),
    path('api/comments-list/', CommentListApiView.as_view(), name='comment-list'),

    path('api/chapters/<int:fanfic>/list/',
         ChapterCreateApiView.as_view(), name='chapter-list-by-fanfic'),
    path('api/chapters/create/', ChapterCreateApiView.as_view(), name='chapter-list'),
    path('api/chapters/<int:pk>/',
         ChapterDetailView.as_view(), name='chapter-detail'),

     path('api/token', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('api/refresh-token', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('markdownx/', include(markdownx)),
    # path('api/oauth2-social/', include('rest_framework_social_oauth2.urls')),
    path('api/oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
