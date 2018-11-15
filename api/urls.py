from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from rest_framework.documentation import include_docs_urls
from api import views
from api import views_fanfic
from api import views_post
from api import views_comment
from api import views_user
from api import api
from api import api_auth

urlpatterns = [
    path('fanfics', views_fanfic.FanficCreateView.as_view(), name='fanfic-create'),
    path('fanfics/v1', views_fanfic.FanficListRemasteredView.as_view(), name='fanfic-list-remastered'),
    path('fanfics/<int:pk>', views_fanfic.FanficDetailView.as_view(), name='fanfic-detail'),
    path('fanfics/v1/<str:slug>', views_fanfic.FanficListDetailView.as_view(), name='fanfic-list-detail'),
    path('fanfics/author/<str:username>', views_fanfic.FanficListByAuthor.as_view(), name='fanfic-by-user'),
    path('fanfics/v1/author/<str:username>', views_fanfic.FanficShowListByAuthorView.as_view(), name='fanfic-show-list-by-author'),
    path('fanfics/<str:category>/category', views_fanfic.FanficListByCategory.as_view(), name='fanfic-list-by-category'),
    path('fanfics/<str:subcategory>/subcategory', views_fanfic.FanficListBySubCategory.as_view(), name='fanfic-list-by-subcategory'),
    path('posts', views_post.PostList.as_view(), name='post-list'),
    path('posts/<str:slug>', views_post.PostDetail.as_view(), name='post-detail'),
    path('chapters/<int:fanfic>/list', views.ChapterListView.as_view(), name='chapter-list'),
    path('chapters/create', views.ChapterCreateView.as_view(), name='chapter-create'),
    path('chapters/<int:pk>', views.ChapterDetailView.as_view(), name='chapter-detail'),
    path('fanfics/genres', views.GenresListView.as_view(), name='genre-list'),
    path('category', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('subcategory', views.SubCategoryListView.as_view(), name='subcategory-list'),
    path('subcategory/<int:pk>', views.SubCategoryDetailView.as_view(), name='subcategory-detail'),
    path('comments', views_comment.CommentListView.as_view(), name='comment-list'),
    path('comments/new', views_comment.CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:fanfic>/fanfic', views_comment.CommentListByFanficView.as_view(), name='comment-list-by-fanfic'),
    path('comments/<int:pk>', views_comment.CommentDetailView.as_view(), name='comment-detail'),
    path('comments-by-chapter/new', views_comment.CommentByChapterCreateView.as_view(), name='comment-by-chapter-create'),
    path('comments/fanfic/<int:fanfic>/chapter/<int:chapter>/list', views_comment.CommentByChapterListByFanficAndChapterView.as_view(), name='comment-list-by-fanfic-and-chapter'),
    path('comments/fanfic/<int:fanfic>/list', views_comment.CommentByChapterListByFanficView.as_view(), name='comment-list-by-chapter'),
    path('users', views_user.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>', views_user.UserDetailView.as_view(), name='user-detail'),
    path('users/<str:user__username>/profile', views_user.AccountProfileListView.as_view(), name='user-account-profile'),
    path('users/<int:account>/socialaccount', views_user.SocialListView.as_view(), name='socialaccount-view'),
    path('users/<int:user__id>/edit/profile', views_user.AccountProfileUpdateView.as_view(), name='user-edit-account-profile'),
    path('users/social-account', views_user.SocialCreateView.as_view(), name='socialaccount-createview'),
    path('notifications', views.NotificationListView.as_view(), name='notifications'),
    path('contenttype/<int:pk>', views.ContentTypeView.as_view(), name='contenttype-detail'),
    path('user', api_auth.CheckoutUserView.as_view(), name='user'),
    path('signup', api_auth.UserCreateView.as_view(), name='signup'),
    path('login', api_auth.LoginView.as_view(), name='login'),
    path('logout', api_auth.LogoutView.as_view(), name='logout'),
    path('feedback', api.EmailFeedbackView.as_view(), name='feedback'),
    path('favorite', api.FavoritedFanficView.as_view(), name='favorite'),
    path('unfavorite', api.UnfavoritedFanficView.as_view(), name='unfavorite'),
    path('change-password', api_auth.ChangePasswordView.as_view(), name='change-password'),
    path('pages/<str:type>', views.FlatPagesByTypeView.as_view(), name='pages-by-type'),
    path('pages', views.FlatPagesView.as_view(), name='all-pages'),
    path('follow-stories', api.FollowStoriesView.as_view(), name='follow-stories'),
    path('follow-user', api.FollowUserView.as_view(), name='follow-user'),
    path('disable-account', api.DeleteAccountView.as_view(), name='disable-account'),
    path('contact-mail', api.ContactMailView.as_view(), name='contact-mail'),
    path('remove-photo/<int:pk>', api_auth.RemovePhotoFromAccount.as_view(), name='remove-photo'),
    path('docs', include_docs_urls(title='Fanfiction API', public=True)),
    path('', views.ApiRootView.as_view(), name=views.ApiRootView.name),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
