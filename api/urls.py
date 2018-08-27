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
    path('fanfics/genres', views.GenresList.as_view(), name='genre-list'),
    path('fanfics/classement', views.ClassementList.as_view(), name='classement-list'),
    path('fanfics/status', views.StatusList.as_view(), name='status-list'),
    path('category', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='category-detail'),
    path('subcategory', views.SubCategoryList.as_view(), name='subcategory-list'),
    path('subcategory/<int:pk>', views.SubCategoryDetail.as_view(), name='subcategory-detail'),
    path('comments', views_comment.CommentList.as_view(), name='comment-list'),
    path('comments/new', views_comment.CommentCreate.as_view(), name='comment-create'),
    path('comments/<int:fanfic>/fanfic', views_comment.CommentListByFanfic.as_view(), name='comment-list-by-fanfic'),
    path('comments/<int:pk>', views_comment.CommentDetail.as_view(), name='comment-detail'),
    path('users', views_user.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views_user.UserDetail.as_view(), name='user-detail'),
    path('user', api_auth.CheckoutUserView.as_view(), name='user'),
    path('signup', api_auth.UserCreate.as_view(), name='signup'),
    path('login', api_auth.LoginView.as_view(), name='login'),
    path('logout', api_auth.LogoutView.as_view(), name='logout'),
    path('feedback', api.EmailFeedback.as_view(), name='feedback'),
    path('favorite', api.FavoritedFanfic.as_view(), name='favorite'),
    path('unfavorite', api.UnfavoritedFanfic.as_view(), name='unfavorite'),
    path('change-password', api_auth.ChangePasswordView.as_view(), name='change-password'),
    path('pages/<str:type>', views.FlatPagesByTypeView.as_view(), name='pages-by-type'),
    path('pages', views.FlatPagesView.as_view(), name='all-pages'),
    path('follow-stories', api.FollowStoriesView.as_view(), name='follow-stories'),
    path('follow-user', api.FollowUserView.as_view(), name='follow-user'),
    path('disable-account', api.DeleteAccountView.as_view(), name='disable-account'),
    path('contact-mail', api.ContactMail.as_view(), name='contact-mail'),
    path('docs', include_docs_urls(title='Fanfiction API', public=True)),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
