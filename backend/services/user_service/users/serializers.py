"""
用户序列化器
"""
from rest_framework import serializers
from .models import User
from mongoengine import DoesNotExist


class UserSerializer(serializers.Serializer):
    """用户序列化器"""
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    full_name = serializers.CharField(read_only=True, allow_null=True)
    phone = serializers.CharField(read_only=True, allow_null=True)
    avatar = serializers.URLField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()


class UserCreateSerializer(serializers.Serializer):
    """创建用户序列化器"""
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, write_only=True, required=True)
    company_id = serializers.CharField(required=False, help_text="企业ID，注册时传入")
    full_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_username(self, value):
        """验证用户名唯一性"""
        try:
            User.objects.get(username=value, is_deleted=False)
            raise serializers.ValidationError("用户名已存在")
        except DoesNotExist:
            pass
        return value

    def validate_email(self, value):
        """验证邮箱唯一性"""
        try:
            User.objects.get(email=value, is_deleted=False)
            raise serializers.ValidationError("邮箱已存在")
        except DoesNotExist:
            pass
        return value

    def create(self, validated_data):
        """创建用户"""
        password = validated_data.pop('password')
        company_id = validated_data.pop('company_id', None)
        
        # 如果提供了company_id，使用它；否则生成一个随机的ObjectId作为临时company_id
        if not company_id:
            from bson import ObjectId
            company_id = str(ObjectId())
        
        # 设置 company_id
        validated_data['company_id'] = company_id
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user


class UserUpdateSerializer(serializers.Serializer):
    """更新用户序列化器"""
    full_name = serializers.CharField(max_length=200, required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    
    def update(self, instance, validated_data):
        """更新用户"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    """登录验证序列化器"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    company_id = serializers.CharField(required=False)
