"""
企业模型
"""
from mongoengine import StringField, BooleanField, URLField, DateTimeField
from common.data_factory.base_model import BaseModel
from datetime import datetime


class Company(BaseModel):
    """
    企业模型
    """
    name = StringField(required=True, max_length=200, verbose_name='企业名称')
    code = StringField(max_length=100, unique=True, null=True, blank=True, verbose_name='企业代码')
    description = StringField(null=True, blank=True, verbose_name='企业描述')
    logo = URLField(null=True, blank=True, verbose_name='企业Logo')
    owner_id = StringField(max_length=24, null=True, blank=True, verbose_name='所有者ID')
    is_active = BooleanField(default=True, verbose_name='是否激活')

    meta = {
        'collection': 'companies',
        'verbose_name': '企业',
        'verbose_name_plural': '企业',
        'indexes': [
            'name',
            'code',
            'owner_id',
            ('company_id', 'is_deleted'),
        ]
    }

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'code': self.code,
            'description': self.description,
            'logo': self.logo,
            'owner_id': self.owner_id,
            'is_active': self.is_active,
        })
        return data


class UserCompany(BaseModel):
    """
    用户-企业关联模型（多对多关系）
    """
    user_id = StringField(required=True, max_length=24, verbose_name='用户ID')
    company_id = StringField(required=True, max_length=24, verbose_name='企业ID')
    role = StringField(max_length=50, default='member', verbose_name='角色',
                      help_text='角色：owner(所有者), admin(管理员), member(成员)')
    joined_at = DateTimeField(default=datetime.now, verbose_name='加入时间')
    is_active = BooleanField(default=True, verbose_name='是否激活')

    meta = {
        'collection': 'user_companies',
        'verbose_name': '用户企业关联',
        'verbose_name_plural': '用户企业关联',
        'indexes': [
            'user_id',
            'company_id',
            ('user_id', 'company_id'),
            {
                'fields': ('user_id', 'company_id'),
                'unique': True
            }
        ]
    }

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'company_id': self.company_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None,
            'is_active': self.is_active,
        })
        return data
