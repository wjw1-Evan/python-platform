"""
企业模型
"""
from mongoengine.fields import StringField, ObjectIdField, ListField, BooleanField, DictField
from apps.core.db_factory import BaseModel
from bson import ObjectId
import secrets


class Company(BaseModel):
    """
    企业模型
    """
    meta = {
        'collection': 'companies',
        'indexes': ['name', 'invite_code', 'company_id'],
    }
    
    name = StringField(required=True, max_length=100, help_text="企业名称")
    description = StringField(max_length=500, help_text="企业描述")
    logo = StringField(help_text="企业Logo URL")
    owner_id = ObjectIdField(required=True, help_text="企业所有者ID")
    
    # 企业成员列表（多对多关系）
    member_ids = ListField(ObjectIdField(), default=list, help_text="成员ID列表")
    
    # 企业邀请码
    invite_code = StringField(unique=True, help_text="邀请码")
    
    # 企业配置
    settings = DictField(default=dict, help_text="企业配置")
    
    is_active = BooleanField(default=True, help_text="是否激活")
    
    def save(self, *args, **kwargs):
        """保存时自动生成邀请码"""
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        return super().save(*args, **kwargs)
    
    @staticmethod
    def generate_invite_code():
        """生成邀请码"""
        while True:
            code = secrets.token_urlsafe(8).upper()[:8]
            if not Company.objects.filter(invite_code=code).first():
                return code
    
    def add_member(self, user_id):
        """添加成员"""
        if user_id not in self.member_ids:
            self.member_ids.append(user_id)
            self.save()
    
    def remove_member(self, user_id):
        """移除成员"""
        if user_id in self.member_ids:
            self.member_ids.remove(user_id)
            self.save()
    
    def is_owner(self, user_id):
        """判断是否是所有者"""
        return self.owner_id == user_id
    
    def is_member(self, user_id):
        """判断是否是成员"""
        return user_id in self.member_ids or self.is_owner(user_id)
