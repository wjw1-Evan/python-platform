"""
企业序列化器
"""
from rest_framework import serializers
from .models import Company, UserCompany
from mongoengine import DoesNotExist


class CompanySerializer(serializers.Serializer):
    """企业序列化器"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    code = serializers.CharField(read_only=True, allow_null=True)
    description = serializers.CharField(read_only=True, allow_null=True)
    logo = serializers.URLField(read_only=True, allow_null=True)
    owner_id = serializers.CharField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()


class CompanyCreateSerializer(serializers.Serializer):
    """创建企业序列化器"""
    name = serializers.CharField(max_length=200, required=True)
    code = serializers.CharField(max_length=100, required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    logo = serializers.URLField(required=False, allow_blank=True)
    owner_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_code(self, value):
        """验证企业代码唯一性"""
        if value:
            try:
                Company.objects.get(code=value, is_deleted=False)
                raise serializers.ValidationError("企业代码已存在")
            except DoesNotExist:
                pass
        return value

    def create(self, validated_data):
        """创建企业"""
        company = Company(**validated_data)
        company.save()
        # 设置company_id为自己
        company.company_id = company.id
        company.save()
        return company


class CompanyUpdateSerializer(serializers.Serializer):
    """更新企业序列化器"""
    name = serializers.CharField(max_length=200, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    logo = serializers.URLField(required=False, allow_blank=True)
    is_active = serializers.BooleanField(required=False)
    
    def update(self, instance, validated_data):
        """更新企业"""
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class UserCompanySerializer(serializers.Serializer):
    """用户企业关联序列化器"""
    id = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    company_id = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    joined_at = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """使用模型的 to_dict() 方法"""
        return instance.to_dict()


class JoinCompanySerializer(serializers.Serializer):
    """加入企业序列化器"""
    user_id = serializers.CharField(required=True)
