"""
通知序列化器
"""
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.Serializer):
    """通知序列化器"""
    id = serializers.CharField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    content = serializers.CharField(read_only=True)
    notification_type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    recipient_id = serializers.CharField(read_only=True)
    sender_id = serializers.CharField(read_only=True, allow_null=True)
    link = serializers.URLField(read_only=True, allow_null=True)
    read_at = serializers.DateTimeField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True, allow_null=True)
    updated_by = serializers.CharField(read_only=True, allow_null=True)
    
    def to_representation(self, instance):
        """转换为字典"""
        return {
            'id': str(instance.id),
            'company_id': str(instance.company_id),
            'title': instance.title,
            'content': instance.content,
            'notification_type': instance.notification_type,
            'status': instance.status,
            'recipient_id': str(instance.recipient_id),
            'sender_id': str(instance.sender_id) if instance.sender_id else None,
            'link': instance.link,
            'read_at': instance.read_at.isoformat() if instance.read_at else None,
            'created_at': instance.created_at.isoformat() if instance.created_at else None,
            'updated_at': instance.updated_at.isoformat() if instance.updated_at else None,
            'created_by': str(instance.created_by) if instance.created_by else None,
            'updated_by': str(instance.updated_by) if instance.updated_by else None,
        }


class NotificationCreateSerializer(serializers.Serializer):
    """创建通知序列化器"""
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)
    notification_type = serializers.CharField(max_length=20, required=False, default='info')
    recipient_id = serializers.CharField(max_length=24, required=True)
    sender_id = serializers.CharField(max_length=24, required=False, allow_blank=True)
    link = serializers.URLField(required=False, allow_blank=True)
    
    def create(self, validated_data):
        """创建通知"""
        notification = Notification(**validated_data)
        notification.save()
        return notification


class NotificationUpdateSerializer(serializers.Serializer):
    """更新通知序列化器"""
    status = serializers.CharField(max_length=20, required=False)
    
    def update(self, instance, validated_data):
        """更新通知"""
        status = validated_data.get('status')
        if status:
            if status == 'read':
                instance.mark_as_read()
            elif status == 'archived':
                instance.mark_as_archived()
            else:
                instance.status = status
                instance.save()
        return instance
