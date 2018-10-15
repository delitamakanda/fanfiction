from django.urls import path, include
from api.helpcenter import views

urlpatterns = [
    path('browse/title', views.browse_by_title, name='browse'),
    path('browse/title/<str:initial>', views.browse_by_title, name='browse_by_title'),
    path('search', views.SearchSubmitView.as_view(), name='search'),
    path('search-ajax-submit', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
    path('faq', views.foire_aux_questions_view, name='foire_aux_questions'),
    path('forum', views.communities_view, name='communities_view'),
	path('fanfic/<int:fanfic_id>/pdf', views.fanfic_pdf, name='fanfic_pdf'),
]
