"""
用户模型
"""
from mongoengine import StringField, EmailField, BooleanField, DateTimeField, URLField
from common.data_factory.base_model import BaseModel
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime


class User(BaseModel):
    """
    用户模型
    """
    username = StringField(required=True, max_length=150, unique=True, verbose_name='用户名')
    email = EmailField(required=True, unique=True, verbose_name='邮箱')
    password_hash = StringField(required=True, max_length=255, verbose_name='密码哈希')
    full_name = StringField(max_length=200, null=True, blank=True, verbose_name='全名')
    phone = StringField(max_length=20, null=True, blank=True, verbose_name='手机号')
    avatar = URLField(null=True, blank=True, verbose_name='头像')
    is_active = BooleanField(default=True, verbose_name='是否激活')
    last_login = DateTimeField(null=True, blank=True, verbose_name='最后登录时间')

    meta = {
        'collection': 'users',
        'verbose_name': '用户',
        'verbose_name_plural': '用户',
        'indexes': [
            'username',
            'email',
            ('company_id', 'is_deleted'),
        ]
    }

    def set_password(self, raw_password):
        """设置密码"""
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        """验证密码"""
        return check_password(raw_password, self.password_hash)

    def to_dict(self):
        """转换为字典（不包含敏感信息）"""
        data = super().to_dict()
        data.update({
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'avatar': self.avatar,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        })
        data.pop('password_hash', None)  # 移除密码哈希
        return data
