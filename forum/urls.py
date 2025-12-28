from django.urls import path
from forum import views
from rest_framework import routers
from forum.api.views import (
MessageViewSet,
TopicViewSet,
BoardViewSet
)

router = routers.DefaultRouter()

router.register(r'boards', BoardViewSet, basename='board')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = router.urls + [
    path('', views.CommunitiesListView.as_view(), name='communities_view'),
    path('<int:pk>', views.communities_view_board_topics, name='board_topics'),
    path('<int:pk>/new', views.communities_view_new_topic, name='board_topics_new'),
    path('<int:pk>/topics/<int:topic_pk>', views.MessageListView.as_view(), name='board_topic_message'),
    path('<int:pk>/topics/<int:topic_pk>/reply', views.communities_view_topic_messages_reply, name='board_topic_message_reply'),
    path('<int:pk>/topics/<int:topic_pk>/message/<int:message_pk>/edit', views.MessageUpdateView.as_view(), name='edit_message'),
]
