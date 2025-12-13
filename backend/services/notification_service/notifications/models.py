"""
通知模型
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from common.data_factory.base_model import BaseModel
from mongoengine import StringField, URLField, DateTimeField
from datetime import datetime


class Notification(BaseModel):
    """
    通知模型
    """
    NOTIFICATION_TYPES = [
        ('system', '系统通知'),
        ('message', '消息通知'),
        ('alert', '警告通知'),
        ('info', '信息通知'),
    ]
    
    STATUS_CHOICES = [
        ('unread', '未读'),
        ('read', '已读'),
        ('archived', '已归档'),
    ]
    
    title = StringField(required=True, max_length=200, verbose_name='标题')
    content = StringField(required=True, verbose_name='内容')
    notification_type = StringField(max_length=20, choices=NOTIFICATION_TYPES, default='info', verbose_name='通知类型')
    status = StringField(max_length=20, choices=STATUS_CHOICES, default='unread', verbose_name='状态')
    recipient_id = StringField(required=True, max_length=24, verbose_name='接收人ID')
    sender_id = StringField(max_length=24, null=True, blank=True, verbose_name='发送人ID')
    link = URLField(null=True, blank=True, verbose_name='链接')
    read_at = DateTimeField(null=True, blank=True, verbose_name='阅读时间')
    
    meta = {
        'collection': 'notifications',
        'verbose_name': '通知',
        'verbose_name_plural': '通知',
        'indexes': [
            ('company_id', 'recipient_id', 'status'),
            ('company_id', 'created_at'),
        ]
    }
    
    def mark_as_read(self):
        """标记为已读"""
        self.status = 'read'
        self.read_at = datetime.now()
        self.save()
    
    def mark_as_archived(self):
        """标记为已归档"""
        self.status = 'archived'
        self.save()
