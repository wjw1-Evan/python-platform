"""
日志序列化器
"""
from rest_framework import serializers
from .models import OperationLog


class OperationLogSerializer(serializers.Serializer):
    """操作日志序列化器"""
    id = serializers.CharField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    log_type = serializers.CharField(read_only=True)
    log_level = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True, allow_null=True)
    action = serializers.CharField(read_only=True)
    resource = serializers.CharField(read_only=True, allow_null=True)
    resource_id = serializers.CharField(read_only=True, allow_null=True)
    method = serializers.CharField(read_only=True, allow_null=True)
    path = serializers.CharField(read_only=True, allow_null=True)
    ip_address = serializers.CharField(read_only=True, allow_null=True)
    user_agent = serializers.CharField(read_only=True, allow_null=True)
    request_data = serializers.CharField(read_only=True, allow_null=True)
    response_data = serializers.CharField(read_only=True, allow_null=True)
    status_code = serializers.IntegerField(read_only=True, allow_null=True)
    error_message = serializers.CharField(read_only=True, allow_null=True)
    execution_time = serializers.FloatField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.CharField(read_only=True, allow_null=True)
    updated_by = serializers.CharField(read_only=True, allow_null=True)
    
    def to_representation(self, instance):
        """转换为字典"""
        return {
            'id': str(instance.id),
            'company_id': str(instance.company_id),
            'log_type': instance.log_type,
            'log_level': instance.log_level,
            'user_id': str(instance.user_id) if instance.user_id else None,
            'action': instance.action,
            'resource': instance.resource,
            'resource_id': str(instance.resource_id) if instance.resource_id else None,
            'method': instance.method,
            'path': instance.path,
            'ip_address': instance.ip_address,
            'user_agent': instance.user_agent,
            'request_data': instance.request_data,
            'response_data': instance.response_data,
            'status_code': instance.status_code,
            'error_message': instance.error_message,
            'execution_time': instance.execution_time,
            'created_at': instance.created_at.isoformat() if instance.created_at else None,
            'updated_at': instance.updated_at.isoformat() if instance.updated_at else None,
            'created_by': str(instance.created_by) if instance.created_by else None,
            'updated_by': str(instance.updated_by) if instance.updated_by else None,
        }
