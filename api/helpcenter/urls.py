from django.urls import path, include
from api.helpcenter import views

urlpatterns = [
    path('browse/title', views.browse_by_title, name='browse'),
    path('browse/title/<str:initial>', views.browse_by_title, name='browse_by_title'),
    path('search', views.SearchSubmitView.as_view(), name='search'),
    path('search-ajax-submit', views.SearchAjaxSubmitView.as_view(), name='search-ajax-submit'),
    path('faq', views.foire_aux_questions_view, name='foire_aux_questions'),
    path('forum', views.CommunitiesListView.as_view(), name='communities_view'),
    path('forum/<int:pk>', views.communities_view_board_topics, name='board_topics'),
    path('forum/<int:pk>/new', views.communities_view_new_topic, name='board_topics_new'),
    path('forum/<int:pk>/topics/<int:topic_pk>', views.MessageListView.as_view(), name='board_topic_message'),
    path('forum/<int:pk>/topics/<int:topic_pk>/reply', views.communities_view_topic_messages_reply, name='board_topic_message_reply'),
    path('forum/<int:pk>/topics/<int:topic_pk>/message/<int:message_pk>/edit', views.MessageUpdateView.as_view(), name='edit_message'),
    path('fanfic/<int:fanfic_id>/pdf', views.fanfic_pdf, name='fanfic_pdf'),
]
