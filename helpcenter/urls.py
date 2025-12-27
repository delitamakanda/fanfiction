from django.urls import path
from rest_framework.routers import DefaultRouter

from helpcenter import views

from helpcenter.api.views import (
    FoireAuxQuestionsApiView,
    LexiqueApiView,
FlatPageApiView,
FlatPagesHTMLByIDView,
)

app_name = 'helpcenter'

routers = DefaultRouter()

routers.register(r'lexique', LexiqueApiView, basename='lexique')
routers.register(r'faq', FoireAuxQuestionsApiView, basename='faq')
routers.register(r'pages', FlatPageApiView, basename='pages')

urlpatterns = routers.urls
urlpatterns += [
    path('browse/title', views.browse_by_title, name='browse'),
    path('browse/title/<str:initial>', views.browse_by_title, name='browse_by_title'),
    path('search', views.SearchSubmitView.as_view(), name='search'),
    path('search-ajax-submit', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
    path('foire-aux-questions', views.foire_aux_questions_view, name='foire_aux_questions'),
	path('flatpages/<int:id>', FlatPagesHTMLByIDView.as_view(), name='flatpage'),
]
