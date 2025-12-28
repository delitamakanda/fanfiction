from django.urls import path
from rest_framework.routers import DefaultRouter

from helpcenter import views

from helpcenter.api.views import (
    FoireAuxQuestionsApiView,
    LexiqueApiView,
FlatPageApiView,
)

app_name = 'helpcenter'

router = DefaultRouter()

router.register(r'lexique', LexiqueApiView, basename='lexique')
router.register(r'faq', FoireAuxQuestionsApiView, basename='faq')
router.register(r'pages', FlatPageApiView, basename='pages')

urlpatterns = router.urls + [
    path('browse/title', views.browse_by_title, name='browse'),
    path('browse/title/<str:initial>', views.browse_by_title, name='browse_by_title'),
    path('search', views.SearchSubmitView.as_view(), name='search'),
    path('search-ajax-submit', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
    path('foire-aux-questions', views.foire_aux_questions_view, name='foire_aux_questions'),
]
