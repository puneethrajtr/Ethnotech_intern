from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from messaging.models import DirectMessage, Group, GroupMessage
from messaging.serializers import (
	DirectMessageSerializer,
	GroupMessageSerializer,
	GroupSerializer,
)

User = get_user_model()


class PrivateMessageSendView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		receiver_id = request.data.get('receiver_id')
		content = request.data.get('content', '').strip()

		if not receiver_id or not content:
			return Response(
				{'detail': 'receiver_id and content are required.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		receiver = get_object_or_404(User, pk=receiver_id)
		message = DirectMessage.objects.create(
			sender=request.user,
			receiver=receiver,
			content=content,
		)
		serializer = DirectMessageSerializer(message)
		return Response(serializer.data, status=status.HTTP_201_CREATED)


class PrivateMessageHistoryView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, user_id):
		messages = DirectMessage.objects.filter(
			Q(sender=request.user, receiver_id=user_id)
			| Q(sender_id=user_id, receiver=request.user)
		).order_by('created_at')
		serializer = DirectMessageSerializer(messages, many=True)
		return Response(serializer.data)


class GroupCreateView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		serializer = GroupSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		group = serializer.save(owner=request.user)
		group.members.add(request.user)
		return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupListView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		groups = Group.objects.filter(members=request.user).order_by('name')
		serializer = GroupSerializer(groups, many=True)
		return Response(serializer.data)


class GroupMemberUpdateView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, group_id):
		action = request.data.get('action')
		user_id = request.data.get('user_id')

		if action not in {'add', 'remove'} or not user_id:
			return Response(
				{'detail': 'action must be add/remove and user_id is required.'},
				status=status.HTTP_400_BAD_REQUEST,
			)

		group = get_object_or_404(Group, pk=group_id)
		if not group.members.filter(pk=request.user.id).exists():
			return Response({'detail': 'Only group members can manage members.'}, status=403)

		user = get_object_or_404(User, pk=user_id)
		if action == 'add':
			group.members.add(user)
		else:
			group.members.remove(user)

		return Response({'detail': 'Member updated.'})


class GroupMessageView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, group_id):
		group = get_object_or_404(Group, pk=group_id)
		if not group.members.filter(pk=request.user.id).exists():
			return Response({'detail': 'Not a member of this group.'}, status=403)

		messages = GroupMessage.objects.filter(group=group).order_by('created_at')
		serializer = GroupMessageSerializer(messages, many=True)
		return Response(serializer.data)

	def post(self, request, group_id):
		group = get_object_or_404(Group, pk=group_id)
		if not group.members.filter(pk=request.user.id).exists():
			return Response({'detail': 'Not a member of this group.'}, status=403)

		content = request.data.get('content', '').strip()
		if not content:
			return Response({'detail': 'content is required.'}, status=400)

		message = GroupMessage.objects.create(
			group=group,
			sender=request.user,
			content=content,
		)
		serializer = GroupMessageSerializer(message)
		return Response(serializer.data, status=status.HTTP_201_CREATED)
