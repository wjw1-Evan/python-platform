"""
通知模型
"""
from mongoengine.fields import StringField, ObjectIdField, BooleanField, DictField, IntField
from apps.core.db_factory import BaseModel
from bson import ObjectId


class Notification(BaseModel):
    """
    通知模型
    """
    meta = {
        'collection': 'notifications',
        'indexes': ['user_id', 'company_id', 'is_read', '-created_at'],
    }
    
    user_id = ObjectIdField(required=True, help_text="接收用户ID")
    title = StringField(required=True, max_length=200, help_text="通知标题")
    content = StringField(required=True, help_text="通知内容")
    type = StringField(required=True, max_length=50, help_text="通知类型：system, message, alert等")
    is_read = BooleanField(default=False, help_text="是否已读")
    read_at = StringField(help_text="阅读时间")
    
    # 通知相关数据
    data = DictField(default=dict, help_text="附加数据")
    
    # 优先级：0-低，1-中，2-高
    priority = IntField(default=1, help_text="优先级")
    
    # 跳转链接
    link = StringField(help_text="跳转链接")
    
    def mark_as_read(self):
        """标记为已读"""
        from datetime import datetime
        self.is_read = True
        self.read_at = datetime.now().isoformat()
        self.save()
    
    @classmethod
    def get_unread_count(cls, user_id, company_id):
        """获取未读通知数量"""
        return cls.objects.filter(
            user_id=user_id,
            company_id=company_id,
            is_deleted=False,
            is_read=False
        ).count()
    
    @classmethod
    def create_notification(cls, user_id, company_id, title, content, type='system', **kwargs):
        """创建通知"""
        notification = cls(
            user_id=user_id,
            company_id=company_id,
            title=title,
            content=content,
            type=type,
            created_by=user_id,
            **kwargs
        )
        notification.save()
        return notification
