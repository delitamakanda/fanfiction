from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api import views
from api import api

urlpatterns = [
    path('fanfics', views.FanficList.as_view(), name='fanfic-list'),
    path('fanfics/v1', views.FanficListRemastered.as_view(), name='fanfic-list-remastered'),
    path('fanfics/<int:pk>', views.FanficDetail.as_view(), name='fanfic-detail'),
    path('fanfics/v1/<int:pk>', views.FanficListDetail.as_view(), name='fanfic-list-detail'),
    path('fanfics/author/<str:username>', views.FanficListByAuthor.as_view(), name='fanfic-by-user'),
    path('fanfics/<str:category>/category', views.FanficListByCategory.as_view(), name='fanfic-list-by-category'),
    path('fanfics/<str:subcategory>/subcategory', views.FanficListBySubCategory.as_view(), name='fanfic-list-by-subcategory'),
    path('posts', views.PostList.as_view(), name='post-list'),
    path('posts/<int:pk>', views.PostDetail.as_view(), name='post-detail'),
    path('chapters', views.ChapterList.as_view(), name='chapter-list'),
    path('chapters/<int:pk>', views.ChapterDetail.as_view(), name='chapter-detail'),
    path('fanfics/genres', views.GenresList.as_view(), name='genre-list'),
    path('fanfics/classement', views.ClassementList.as_view(), name='classement-list'),
    path('fanfics/status', views.StatusList.as_view(), name='status-list'),
    path('category', views.CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>', views.CategoryDetail.as_view(), name='category-detail'),
    path('subcategory', views.SubCategoryList.as_view(), name='subcategory-list'),
    path('subcategory/<int:pk>', views.SubCategoryDetail.as_view(), name='subcategory-detail'),
    path('comments', views.CommentList.as_view(), name='comment-list'),
    path('comments/new', views.CommentCreate.as_view(), name='comment-create'),
    path('comments/<int:fanfic>/fanfic', views.CommentListByFanfic.as_view(), name='comment-list-by-fanfic'),
    path('comments/<int:pk>', views.CommentDetail.as_view(), name='comment-detail'),
    path('users', views.UserList.as_view(), name='user-list'),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('user', api.CheckoutUserView.as_view(), name='user'),
    path('signup', api.UserCreate.as_view(), name='signup'),
    path('login', api.LoginView.as_view(), name='login'),
    path('logout', api.LogoutView.as_view(), name='logout'),
    path('feedback', api.EmailFeedback.as_view(), name='feedback'),
    path('favorite', api.FavoritedFanfic.as_view(), name='favorite'),
    path('unfavorite', api.UnfavoritedFanfic.as_view(), name='unfavorite'),
    path('change-password', api.ChangePasswordView.as_view(), name='change-password'),
    path('mentions-legales', api.MentionsLegalesView.as_view(), name='mentions-legales'),
    path('cgu', api.CGUView.as_view(), name='cgu'),
    path('follow-stories', api.FollowStories.as_view(), name='follow-stories'),
    path('', views.ApiRoot.as_view(), name=views.ApiRoot.name),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
