"""
权限序列化器
"""
from rest_framework import serializers
from .models import Role, Permission, RolePermission, UserRole


class RoleSerializer(serializers.Serializer):
    """角色序列化器"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True, allow_null=True)
    is_system = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()


class PermissionSerializer(serializers.Serializer):
    """权限序列化器"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True)
    resource = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()


class RolePermissionSerializer(serializers.Serializer):
    """角色权限关联序列化器"""
    id = serializers.CharField(read_only=True)
    role_id = serializers.CharField(read_only=True)
    permission_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()


class UserRoleSerializer(serializers.Serializer):
    """用户角色关联序列化器"""
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    role_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()
