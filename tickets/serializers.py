from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Role, Ticket, Comment, Timeline

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RoleSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Role
        fields = ['user', 'role']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'parent', 'replies']
    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all(), many=True).data

class TimelineSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Timeline
        fields = ['id', 'action', 'user', 'timestamp']

class TicketSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    timeline = TimelineSerializer(many=True, read_only=True)
    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'created_by', 'assigned_to', 'status',
            'created_at', 'updated_at', 'sla_deadline', 'version', 'comments', 'timeline'
        ]
