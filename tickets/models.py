
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.Model):
	ROLE_CHOICES = [
		('user', 'User'),
		('agent', 'Agent'),
		('admin', 'Admin'),
	]
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Ticket(models.Model):
	STATUS_CHOICES = [
		('open', 'Open'),
		('assigned', 'Assigned'),
		('closed', 'Closed'),
		('breached', 'Breached'),
	]
	title = models.CharField(max_length=255)
	description = models.TextField()
	created_by = models.ForeignKey(User, related_name='created_tickets', on_delete=models.CASCADE)
	assigned_to = models.ForeignKey(User, related_name='assigned_tickets', on_delete=models.SET_NULL, null=True, blank=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	sla_deadline = models.DateTimeField()
	version = models.PositiveIntegerField(default=0)  # For optimistic locking

	def is_breached(self):
		return timezone.now() > self.sla_deadline and self.status != 'closed'

class Comment(models.Model):
	ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

class Timeline(models.Model):
	ticket = models.ForeignKey(Ticket, related_name='timeline', on_delete=models.CASCADE)
	action = models.CharField(max_length=255)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	timestamp = models.DateTimeField(auto_now_add=True)
