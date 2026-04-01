from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils import timezone

from messaging.models import DirectMessage, Group, GroupMessage

User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        self.chat_type = self.scope['url_route']['kwargs'].get('chat_type')
        self.target_id = int(self.scope['url_route']['kwargs'].get('target_id'))

        if self.chat_type == 'private':
            self.group_name = self._private_group_name(self.user.id, self.target_id)
        elif self.chat_type == 'group':
            is_member = await self._is_group_member(self.target_id, self.user.id)
            if not is_member:
                await self.close()
                return
            self.group_name = f"group_{self.target_id}"
        else:
            await self.close()
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        await self._set_user_online(self.user.id)

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        if self.user and not self.user.is_anonymous:
            await self._set_user_offline(self.user.id)

    async def receive_json(self, content, **kwargs):
        message_text = (content.get('content') or '').strip()
        if not message_text:
            return

        if self.chat_type == 'private':
            await self._save_private_message(self.user.id, self.target_id, message_text)
            payload = {
                'type': 'private_message',
                'sender_id': self.user.id,
                'receiver_id': self.target_id,
                'content': message_text,
            }
        else:
            await self._save_group_message(self.user.id, self.target_id, message_text)
            payload = {
                'type': 'group_message',
                'sender_id': self.user.id,
                'group_id': self.target_id,
                'content': message_text,
            }

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat.message',
                'payload': payload,
            },
        )

    async def chat_message(self, event):
        await self.send_json(event['payload'])

    def _private_group_name(self, user_id, other_user_id):
        first, second = sorted([user_id, other_user_id])
        return f"private_{first}_{second}"

    @database_sync_to_async
    def _save_private_message(self, sender_id, receiver_id, content):
        DirectMessage.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
        )

    @database_sync_to_async
    def _save_group_message(self, sender_id, group_id, content):
        GroupMessage.objects.create(
            sender_id=sender_id,
            group_id=group_id,
            content=content,
        )

    @database_sync_to_async
    def _is_group_member(self, group_id, user_id):
        return Group.objects.filter(id=group_id, members__id=user_id).exists()

    @database_sync_to_async
    def _set_user_online(self, user_id):
        User.objects.filter(id=user_id).update(is_online=True, last_seen=None)

    @database_sync_to_async
    def _set_user_offline(self, user_id):
        User.objects.filter(id=user_id).update(is_online=False, last_seen=timezone.now())


class PresenceConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        if not self.user or self.user.is_anonymous:
            await self.close()
            return

        await self.channel_layer.group_add('presence', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('presence', self.channel_name)

    async def presence_update(self, event):
        await self.send_json(event['payload'])
