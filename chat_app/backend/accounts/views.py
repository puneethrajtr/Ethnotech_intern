from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = RegisterSerializer
	permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
	queryset = User.objects.all().order_by('username')
	serializer_class = UserSerializer


class UserStatusView(APIView):
	def get(self, request, user_id):
		user = get_object_or_404(User, pk=user_id)
		serializer = UserSerializer(user)
		return Response(serializer.data)


class UserPresenceView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request):
		user = request.user
		if user.is_anonymous:
			token = request.data.get('token')
			if token:
				jwt_auth = JWTAuthentication()
				try:
					validated_token = jwt_auth.get_validated_token(token)
					user = jwt_auth.get_user(validated_token)
				except Exception:
					return Response({'detail': 'Invalid token.'}, status=401)
			else:
				return Response({'detail': 'Authentication required.'}, status=401)

		action = request.data.get('action')
		if action == 'online':
			User.objects.filter(id=user.id).update(
				is_online=True,
				last_seen=None,
			)
			self._broadcast_presence(user.id, True, None)
			return Response({'detail': 'Presence updated.'})
		if action == 'offline':
			last_seen = timezone.now()
			User.objects.filter(id=user.id).update(
				is_online=False,
				last_seen=last_seen,
			)
			self._broadcast_presence(user.id, False, last_seen)
			return Response({'detail': 'Presence updated.'})
		return Response(
			{'detail': 'action must be online or offline.'},
			status=status.HTTP_400_BAD_REQUEST,
		)

	def _broadcast_presence(self, user_id, is_online, last_seen):
		channel_layer = get_channel_layer()
		async_to_sync(channel_layer.group_send)(
			'presence',
			{
				'type': 'presence.update',
				'payload': {
					'type': 'presence_update',
					'user_id': user_id,
					'is_online': is_online,
					'last_seen': last_seen.isoformat() if last_seen else None,
				},
			},
		)
