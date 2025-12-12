"""
通知序列化器
"""
from rest_framework import serializers
from apps.notifications.models import Notification


class NotificationSerializer(serializers.Serializer):
    """通知序列化器"""
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    type = serializers.CharField(max_length=50)
    is_read = serializers.BooleanField(read_only=True)
    read_at = serializers.CharField(read_only=True)
    data = serializers.DictField(read_only=True)
    priority = serializers.IntegerField(read_only=True)
    link = serializers.URLField(read_only=True, allow_blank=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """转换为字典"""
        data = super().to_representation(instance)
        if isinstance(instance, Notification):
            data['id'] = str(instance.id)
            data['user_id'] = str(instance.user_id)
        return data


class NotificationCreateSerializer(serializers.Serializer):
    """创建通知序列化器"""
    user_id = serializers.CharField(required=True)
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)
    type = serializers.CharField(max_length=50, default='system')
    priority = serializers.IntegerField(default=1)
    link = serializers.URLField(required=False, allow_blank=True)
    data = serializers.DictField(required=False)
