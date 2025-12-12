"""
用户模型
"""
from mongoengine import Document, ReferenceField
from mongoengine.fields import StringField, EmailField, BooleanField, DateTimeField, ListField, ObjectIdField
from apps.core.db_factory import BaseModel
from datetime import datetime
from bson import ObjectId


class User(BaseModel):
    """
    用户模型
    """
    meta = {
        'collection': 'users',
        'indexes': ['email', 'username', 'company_id'],
    }
    
    username = StringField(required=True, unique=True, max_length=50, help_text="用户名")
    email = EmailField(required=True, unique=True, help_text="邮箱")
    password_hash = StringField(required=True, help_text="密码哈希")
    full_name = StringField(max_length=100, help_text="全名")
    phone = StringField(max_length=20, help_text="手机号")
    avatar = StringField(help_text="头像URL")
    is_active = BooleanField(default=True, help_text="是否激活")
    is_superuser = BooleanField(default=False, help_text="是否超级用户")
    last_login = DateTimeField(help_text="最后登录时间")
    
    # 用户所属的企业列表（多对多关系）
    company_ids = ListField(ObjectIdField(), default=list, help_text="所属企业ID列表")
    default_company_id = ObjectIdField(help_text="默认企业ID")
    
    def set_password(self, password):
        """设置密码"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password_hash = pwd_context.hash(password)
    
    def check_password(self, password):
        """验证密码"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.password_hash)
    
    def add_company(self, company_id):
        """添加企业"""
        if company_id not in self.company_ids:
            self.company_ids.append(company_id)
            if not self.default_company_id:
                self.default_company_id = company_id
            self.save()
    
    def remove_company(self, company_id):
        """移除企业"""
        if company_id in self.company_ids:
            self.company_ids.remove(company_id)
            if self.default_company_id == company_id:
                self.default_company_id = self.company_ids[0] if self.company_ids else None
            self.save()
    
    def set_default_company(self, company_id):
        """设置默认企业"""
        if company_id in self.company_ids:
            self.default_company_id = company_id
            self.save()
