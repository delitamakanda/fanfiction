from django.urls import path, include
from helpcenter import views

urlpatterns = [
    path('browse/title', views.browse_by_title, name='browse'),
    path('browse/title/<str:initial>', views.browse_by_title, name='browse_by_title'),
    path('search', views.SearchSubmitView.as_view(), name='search'),
    path('search-ajax-submit', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
    path('foire-aux-questions', views.foire_aux_questions_view, name='foire_aux_questions'),
    path('fanfic/<int:fanfic_id>/pdf', views.fanfic_pdf, name='fanfic_pdf'),
]
