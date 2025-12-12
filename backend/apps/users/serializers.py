"""
用户序列化器
"""
from rest_framework import serializers
from apps.users.models import User
from apps.companies.models import Company


class UserSerializer(serializers.Serializer):
    """用户序列化器"""
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    full_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(read_only=True)
    company_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    default_company_id = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """转换为字典"""
        data = super().to_representation(instance)
        if isinstance(instance, User):
            data['id'] = str(instance.id)
            data['company_ids'] = [str(cid) for cid in instance.company_ids]
            if instance.default_company_id:
                data['default_company_id'] = str(instance.default_company_id)
        return data


class UserRegisterSerializer(serializers.Serializer):
    """用户注册序列化器"""
    username = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    full_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    company_name = serializers.CharField(max_length=100, required=False, help_text="企业名称，如果不提供则使用用户名")


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)


class UserUpdateSerializer(serializers.Serializer):
    """用户更新序列化器"""
    full_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
