"""
权限模型
"""
from mongoengine import StringField, BooleanField
from common.data_factory.base_model import BaseModel


class Role(BaseModel):
    """
    角色模型
    """
    name = StringField(required=True, max_length=100, verbose_name='角色名称')
    code = StringField(required=True, max_length=50, unique=True, verbose_name='角色代码')
    description = StringField(null=True, blank=True, verbose_name='角色描述')
    is_system = BooleanField(default=False, verbose_name='是否系统角色')

    meta = {
        'collection': 'roles',
        'verbose_name': '角色',
        'verbose_name_plural': '角色',
        'indexes': [
            'name',
            'code',
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
            'is_system': self.is_system,
        })
        return data


class Permission(BaseModel):
    """
    权限模型
    """
    name = StringField(required=True, max_length=100, verbose_name='权限名称')
    code = StringField(required=True, max_length=100, verbose_name='权限代码')
    resource = StringField(required=True, max_length=100, verbose_name='资源')
    action = StringField(required=True, max_length=50, verbose_name='操作')
    description = StringField(null=True, blank=True, verbose_name='权限描述')

    meta = {
        'collection': 'permissions',
        'verbose_name': '权限',
        'verbose_name_plural': '权限',
        'indexes': [
            'code',
            ('resource', 'action'),
            ('company_id', 'is_deleted'),
            {
                'fields': ('code', 'company_id'),
                'unique': True
            }
        ]
    }

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'name': self.name,
            'code': self.code,
            'resource': self.resource,
            'action': self.action,
            'description': self.description,
        })
        return data


class RolePermission(BaseModel):
    """
    角色权限关联模型
    """
    role_id = StringField(required=True, max_length=24, verbose_name='角色ID')
    permission_id = StringField(required=True, max_length=24, verbose_name='权限ID')

    meta = {
        'collection': 'role_permissions',
        'verbose_name': '角色权限关联',
        'verbose_name_plural': '角色权限关联',
        'indexes': [
            'role_id',
            'permission_id',
            ('role_id', 'permission_id'),
            {
                'fields': ('role_id', 'permission_id'),
                'unique': True
            }
        ]
    }

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'role_id': self.role_id,
            'permission_id': self.permission_id,
        })
        return data


class UserRole(BaseModel):
    """
    用户角色关联模型
    """
    user_id = StringField(required=True, max_length=24, verbose_name='用户ID')
    role_id = StringField(required=True, max_length=24, verbose_name='角色ID')

    meta = {
        'collection': 'user_roles',
        'verbose_name': '用户角色关联',
        'verbose_name_plural': '用户角色关联',
        'indexes': [
            'user_id',
            'role_id',
            ('user_id', 'role_id', 'company_id'),
            {
                'fields': ('user_id', 'role_id', 'company_id'),
                'unique': True
            }
        ]
    }

    def to_dict(self):
        """转换为字典"""
        data = super().to_dict()
        data.update({
            'user_id': self.user_id,
            'role_id': self.role_id,
        })
        return data
