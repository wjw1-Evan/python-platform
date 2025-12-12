"""
数据工厂 - 统一实现数据库操作并创建模型的基类
"""
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    StringField, IntField, DateTimeField, BooleanField,
    ObjectIdField, ListField, ReferenceField, DictField
)
from datetime import datetime
from bson import ObjectId


class BaseModel(Document):
    """
    模型基类 - 所有模型继承此类
    提供统一的基础字段和操作方法
    """
    meta = {
        'abstract': True,
        'indexes': ['-created_at', 'company_id'],
    }
    
    # 基础字段（mongoengine的Document已经有id字段，不需要重复定义）
    company_id = ObjectIdField(required=True, help_text="企业ID，用于数据隔离")
    created_at = DateTimeField(default=datetime.now, help_text="创建时间")
    updated_at = DateTimeField(default=datetime.now, help_text="更新时间")
    is_deleted = BooleanField(default=False, help_text="软删除标记")
    created_by = ObjectIdField(help_text="创建人ID")
    updated_by = ObjectIdField(help_text="更新人ID")
    
    def save(self, *args, **kwargs):
        """重写save方法，自动更新updated_at"""
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
    
    @classmethod
    def get_by_company(cls, company_id, **kwargs):
        """根据企业ID查询，自动过滤已删除数据"""
        kwargs['company_id'] = company_id
        kwargs['is_deleted'] = False
        return cls.objects.filter(**kwargs)
    
    @classmethod
    def create_by_company(cls, company_id, created_by=None, **kwargs):
        """为企业创建数据"""
        kwargs['company_id'] = company_id
        if created_by:
            kwargs['created_by'] = created_by
        return cls(**kwargs).save()
    
    def to_dict(self):
        """转换为字典"""
        data = self.to_mongo().to_dict()
        # mongoengine的to_mongo()返回的是dict，需要处理_id
        if '_id' in data:
            data['id'] = str(data['_id'])
            del data['_id']
        elif 'id' not in data:
            data['id'] = str(self.id)
        return data


class BaseEmbeddedModel(EmbeddedDocument):
    """
    嵌入式文档基类
    """
    meta = {
        'abstract': True,
    }
    
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)


class DBFactory:
    """
    数据工厂类 - 统一数据库操作
    """
    
    @staticmethod
    def create(model_class, company_id, created_by=None, **kwargs):
        """
        创建记录
        :param model_class: 模型类
        :param company_id: 企业ID
        :param created_by: 创建人ID
        :param kwargs: 其他字段
        :return: 创建的模型实例
        """
        return model_class.create_by_company(company_id, created_by, **kwargs)
    
    @staticmethod
    def get(model_class, company_id, **filters):
        """
        查询单条记录
        :param model_class: 模型类
        :param company_id: 企业ID
        :param filters: 查询条件
        :return: 模型实例或None
        """
        filters['company_id'] = company_id
        filters['is_deleted'] = False
        return model_class.objects.filter(**filters).first()
    
    @staticmethod
    def list(model_class, company_id, skip=0, limit=20, **filters):
        """
        查询列表
        :param model_class: 模型类
        :param company_id: 企业ID
        :param skip: 跳过数量
        :param limit: 限制数量
        :param filters: 查询条件
        :return: 查询结果列表
        """
        filters['company_id'] = company_id
        filters['is_deleted'] = False
        return model_class.objects.filter(**filters).skip(skip).limit(limit)
    
    @staticmethod
    def count(model_class, company_id, **filters):
        """
        统计数量
        :param model_class: 模型类
        :param company_id: 企业ID
        :param filters: 查询条件
        :return: 数量
        """
        filters['company_id'] = company_id
        filters['is_deleted'] = False
        return model_class.objects.filter(**filters).count()
    
    @staticmethod
    def update(model_class, company_id, filters, update_data, updated_by=None):
        """
        更新记录
        :param model_class: 模型类
        :param company_id: 企业ID
        :param filters: 查询条件
        :param update_data: 更新数据
        :param updated_by: 更新人ID
        :return: 更新的记录数
        """
        filters['company_id'] = company_id
        filters['is_deleted'] = False
        if updated_by:
            update_data['updated_by'] = updated_by
        update_data['updated_at'] = datetime.now()
        return model_class.objects.filter(**filters).update(**update_data)
    
    @staticmethod
    def delete(model_class, company_id, **filters):
        """
        软删除记录
        :param model_class: 模型类
        :param company_id: 企业ID
        :param filters: 查询条件
        :return: 删除的记录数
        """
        filters['company_id'] = company_id
        filters['is_deleted'] = False
        return model_class.objects.filter(**filters).update(
            is_deleted=True,
            updated_at=datetime.now()
        )
    
    @staticmethod
    def hard_delete(model_class, company_id, **filters):
        """
        硬删除记录
        :param model_class: 模型类
        :param company_id: 企业ID
        :param filters: 查询条件
        :return: 删除的记录数
        """
        filters['company_id'] = company_id
        return model_class.objects.filter(**filters).delete()
