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
from rest_framework.documentation import include_docs_urls

from accounts.api.views import (
    UserFanficDetailView,
    UserDetailView,
    AccountProfileDetailView,
    SocialListApiView,
    SocialDestroyApiView,
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('help/', include(('helpcenter.urls', 'helpcenter'), namespace='helpcenter')),
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='index'),
]

urlpatterns += [    
    path('api/', ApiRootView.as_view(), name=ApiRootView.name),
    path('api/docs/', include_docs_urls(title='Fanfiction API', public=False)),

    path('api/users/<str:user__username>/account', UserFanficDetailView.as_view(), name='user-list'),
    path('api/users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('api/users/<str:user__username>/profile', AccountProfileDetailView.as_view(), name='user-edit-account-profile'),
    path('api/users/<int:account>/socialaccount', SocialListApiView.as_view(), name='socialaccount-view'),
    path('api/users/social-account', SocialListApiView.as_view(), name='socialaccount-createview'),
    path('api/users/social-account/<int:pk>/delete', SocialDestroyApiView.as_view(), name='socialaccount-destroy'),

    path('api/faq/', FoireAuxQuestionsApiView.as_view(), name='faq'),
    path('api/lexique/', LexiqueApiView.as_view(), name='lexique'),

    path('api/category/', CategoryListView.as_view(), name='category-list'),
    path('api/category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('api/subcategory/', SubCategoryListView.as_view(), name='subcategory-list'),
    path('api/subcategory/<int:pk>/', SubCategoryDetailView.as_view(), name='subcategory-detail'),

    path('api/tags/', TagListAPIView.as_view(), name='tag-list'),
    path('api/posts/', PostListAPIView.as_view(), name='post-list'),
    path('api/posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('api/posts/<int:pk>/update/', PostUpdateAPIView.as_view(), name='post-update'),
    path('api/posts/<int:pk>/remove/', PostUpdateAPIView.as_view(), name='post-delete'),
    path('api/posts/<str:slug>/', PostDetailAPIView.as_view(), name='post-detail'),

    path('api/genres/', GenresListView.as_view(), name='genre-list'),
    path('api/classement/', ClassementListView.as_view(), name='classement-list'),
    path('api/status/', StatusListView.as_view(), name='status-list'),
    path('api/fanfics/', FanficCreateApiView.as_view(), name='fanfic-list'),
    path('api/fanfics/<str:username>/', FanficCreateApiView.as_view(), name='fanfic-list-by-author'),
    path('api/fanfics/<str:slug>/detail/', FanficDetailView.as_view(), name='fanfic-detail'),
    path('api/fanfics/<int:pk>/fanfic-detail/', FanficUpdateDetailView.as_view(), name='fanfic-update-detail'),

    path('api/comments/', CommentCreateApiView.as_view(), name='comment-create'),
    path('api/comments-list/', CommentListApiView.as_view(), name='comment-list'),

    path('api/chapters/<int:fanfic>/list/', ChapterCreateApiView.as_view(), name='chapter-list-by-fanfic'),
    path('api/chapters/create/', ChapterCreateApiView.as_view(), name='chapter-list'),
    path('api/chapters/<int:pk>/', ChapterDetailView.as_view(), name='chapter-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('markdownx/', include('markdownx.urls')),
    path('oauth2-social/', include('rest_framework_social_oauth2.urls')),
    path('oauth2/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
