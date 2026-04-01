from django.contrib.auth import get_user_model
from rest_framework import serializers

from messaging.models import DirectMessage, Group, GroupMessage

User = get_user_model()


class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']


class GroupSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
    )
    members_details = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'owner', 'members', 'members_details', 'created_at']
        read_only_fields = ['id', 'owner', 'created_at']

    def get_members_details(self, obj):
        return [
            {
                'id': member.id,
                'username': member.username,
                'is_online': member.is_online,
                'last_seen': member.last_seen,
            }
            for member in obj.members.all()
        ]


class GroupMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMessage
        fields = ['id', 'group', 'sender', 'content', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']
