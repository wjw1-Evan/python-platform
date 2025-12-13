"""
认证序列化器
"""
from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password


class RegisterSerializer(serializers.Serializer):
    """注册序列化器"""
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    company_name = serializers.CharField(max_length=200, required=False, help_text="企业名称，如果不提供则使用用户名")

    def validate_username(self, value):
        """验证用户名"""
        if len(value) < 3:
            raise serializers.ValidationError("用户名至少需要3个字符")
        return value

    def validate_password(self, value):
        """验证密码"""
        if len(value) < 8:
            raise serializers.ValidationError("密码至少需要8个字符")
        return value


class LoginSerializer(serializers.Serializer):
    """登录序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    company_id = serializers.CharField(required=False, help_text="企业ID，如果不提供则使用用户的默认企业")


class TokenRefreshSerializer(serializers.Serializer):
    """Token刷新序列化器"""
    refresh = serializers.CharField(required=True)
