"""
企业序列化器
"""
from rest_framework import serializers
from apps.companies.models import Company


class CompanySerializer(serializers.Serializer):
    """企业序列化器"""
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    logo = serializers.URLField(required=False, allow_blank=True)
    owner_id = serializers.CharField(read_only=True)
    member_ids = serializers.ListField(child=serializers.CharField(), read_only=True)
    invite_code = serializers.CharField(read_only=True)
    settings = serializers.DictField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    def to_representation(self, instance):
        """转换为字典"""
        data = super().to_representation(instance)
        if isinstance(instance, Company):
            data['id'] = str(instance.id)
            data['owner_id'] = str(instance.owner_id)
            data['member_ids'] = [str(mid) for mid in instance.member_ids]
        return data


class CompanyCreateSerializer(serializers.Serializer):
    """创建企业序列化器"""
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    logo = serializers.URLField(required=False, allow_blank=True)


class CompanyUpdateSerializer(serializers.Serializer):
    """更新企业序列化器"""
    name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    logo = serializers.URLField(required=False, allow_blank=True)
