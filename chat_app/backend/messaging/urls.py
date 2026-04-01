from django.urls import path

from messaging.views import (
    GroupCreateView,
    GroupListView,
    GroupMemberUpdateView,
    GroupMessageView,
    PrivateMessageHistoryView,
    PrivateMessageSendView,
)

urlpatterns = [
    path('messages/private/', PrivateMessageSendView.as_view(), name='private_message_send'),
    path(
        'messages/private/history/<int:user_id>/',
        PrivateMessageHistoryView.as_view(),
        name='private_message_history',
    ),
    path('groups/list/', GroupListView.as_view(), name='group_list'),
    path('groups/', GroupCreateView.as_view(), name='group_create'),
    path('groups/<int:group_id>/members/', GroupMemberUpdateView.as_view(), name='group_members'),
    path('groups/<int:group_id>/messages/', GroupMessageView.as_view(), name='group_messages'),
]
