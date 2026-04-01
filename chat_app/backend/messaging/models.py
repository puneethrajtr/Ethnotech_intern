from django.conf import settings
from django.db import models


class DirectMessage(models.Model):
	sender = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='sent_messages',
		on_delete=models.CASCADE,
	)
	receiver = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='received_messages',
		on_delete=models.CASCADE,
	)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']


class Group(models.Model):
	name = models.CharField(max_length=255)
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		related_name='owned_groups',
		on_delete=models.CASCADE,
	)
	members = models.ManyToManyField(
		settings.AUTH_USER_MODEL,
		related_name='chat_groups',
	)
	created_at = models.DateTimeField(auto_now_add=True)


class GroupMessage(models.Model):
	group = models.ForeignKey(Group, related_name='messages', on_delete=models.CASCADE)
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['created_at']
