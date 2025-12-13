"""
数据工厂 - 基础模型类
提供所有模型的通用字段和功能
"""
from mongoengine import Document, StringField, DateTimeField, BooleanField
from bson import ObjectId
from datetime import datetime


class BaseModel(Document):
    """
    基础模型类
    所有模型都应继承此类，提供通用字段和功能
    """
    id = StringField(primary_key=True, max_length=24, default=lambda: str(ObjectId()))
    company_id = StringField(required=True, max_length=24, verbose_name='企业ID')
    created_at = DateTimeField(default=datetime.now, verbose_name='创建时间')
    updated_at = DateTimeField(default=datetime.now, verbose_name='更新时间')
    is_deleted = BooleanField(default=False, verbose_name='是否删除')
    created_by = StringField(max_length=24, null=True, blank=True, verbose_name='创建人ID')
    updated_by = StringField(max_length=24, null=True, blank=True, verbose_name='更新人ID')

    meta = {
        'abstract': True,
        'ordering': ['-created_at'],
        'indexes': [
            'company_id',
            'is_deleted',
            'created_at',
            ('company_id', 'is_deleted'),
        ]
    }

    def save(self, *args, **kwargs):
        """保存时自动更新 updated_at"""
        if not self.id:
            self.id = str(ObjectId())
            if not self.created_at:
                self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super().save(*args, **kwargs)

    def soft_delete(self):
        """软删除"""
        self.is_deleted = True
        self.save()

    def restore(self):
        """恢复删除"""
        self.is_deleted = False
        self.save()

    def to_dict(self):
        """转换为字典"""
        return {
            'id': str(self.id),
            'company_id': str(self.company_id),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'is_deleted': self.is_deleted,
            'created_by': str(self.created_by) if self.created_by else None,
            'updated_by': str(self.updated_by) if self.updated_by else None,
        }
