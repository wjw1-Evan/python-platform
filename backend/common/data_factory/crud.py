"""
数据工厂 - 统一CRUD操作接口
提供所有模型的统一数据操作接口
"""
from typing import Dict, List, Optional, Any
from mongoengine import DoesNotExist
from mongoengine import Q
from bson import ObjectId
from .base_model import BaseModel


class BaseCRUD:
    """
    基础CRUD操作类
    提供统一的增删改查接口，自动处理企业数据隔离
    """
    
    def __init__(self, model_class: type[BaseModel]):
        """
        初始化CRUD操作类
        
        Args:
            model_class: 继承自BaseModel的模型类
        """
        if not issubclass(model_class, BaseModel):
            raise ValueError(f"模型类 {model_class} 必须继承自 BaseModel")
        self.model = model_class

    def create(self, data: Dict[str, Any], company_id: str, created_by: Optional[str] = None) -> BaseModel:
        """
        创建记录
        
        Args:
            data: 要创建的数据字典
            company_id: 企业ID（用于数据隔离）
            created_by: 创建人ID
            
        Returns:
            创建的模型实例
        """
        # 确保company_id存在
        data['company_id'] = company_id
        if created_by:
            data['created_by'] = created_by
            data['updated_by'] = created_by
        
        instance = self.model(**data)
        instance.save()
        return instance

    def get(self, id: str, company_id: str, include_deleted: bool = False) -> Optional[BaseModel]:
        """
        根据ID获取单条记录
        
        Args:
            id: 记录ID
            company_id: 企业ID（用于数据隔离）
            include_deleted: 是否包含已删除的记录
            
        Returns:
            模型实例或None
        """
        query = {
            'id': id,
            'company_id': company_id
        }
        if not include_deleted:
            query['is_deleted'] = False
            
        try:
            return self.model.objects.get(**query)
        except DoesNotExist:
            return None

    def update(self, id: str, data: Dict[str, Any], company_id: str, updated_by: Optional[str] = None) -> Optional[BaseModel]:
        """
        更新记录
        
        Args:
            id: 记录ID
            data: 要更新的数据字典
            company_id: 企业ID（用于数据隔离）
            updated_by: 更新人ID
            
        Returns:
            更新后的模型实例或None
        """
        instance = self.get(id, company_id)
        if not instance:
            return None
        
        # 移除不允许直接更新的字段
        data.pop('id', None)
        data.pop('company_id', None)
        data.pop('created_at', None)
        data.pop('created_by', None)
        
        if updated_by:
            data['updated_by'] = updated_by
        
        for key, value in data.items():
            setattr(instance, key, value)
        
        instance.save()
        return instance

    def delete(self, id: str, company_id: str, hard_delete: bool = False) -> bool:
        """
        删除记录
        
        Args:
            id: 记录ID
            company_id: 企业ID（用于数据隔离）
            hard_delete: 是否硬删除（物理删除）
            
        Returns:
            是否删除成功
        """
        instance = self.get(id, company_id)
        if not instance:
            return False
        
        if hard_delete:
            instance.delete()
        else:
            instance.soft_delete()
        
        return True

    def list(
        self,
        company_id: str,
        filters: Optional[Dict[str, Any]] = None,
        exclude: Optional[Dict[str, Any]] = None,
        ordering: Optional[List[str]] = None,
        page: int = 1,
        page_size: int = 20,
        include_deleted: bool = False
    ) -> Dict[str, Any]:
        """
        获取记录列表（支持分页）
        
        Args:
            company_id: 企业ID（用于数据隔离）
            filters: 过滤条件
            exclude: 排除条件
            ordering: 排序字段列表，如 ['-created_at', 'name']
            page: 页码（从1开始）
            page_size: 每页数量
            include_deleted: 是否包含已删除的记录
            
        Returns:
            包含列表数据和分页信息的字典
        """
        # 构建查询条件
        query = Q(company_id=company_id)
        
        if not include_deleted:
            query &= Q(is_deleted=False)
        
        # 添加过滤条件
        if filters:
            for key, value in filters.items():
                query &= Q(**{key: value})
        
        # 添加排除条件
        if exclude:
            for key, value in exclude.items():
                query &= ~Q(**{key: value})
        
        # 构建查询集
        queryset = self.model.objects.filter(query)
        
        # 排序
        if ordering:
            queryset = queryset.order_by(*ordering)
        else:
            # 默认按创建时间倒序
            queryset = queryset.order_by('-created_at')
        
        # 计算总数
        total = queryset.count()
        
        # 分页
        skip = (page - 1) * page_size
        items = list(queryset.skip(skip).limit(page_size))
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return {
            'items': items,
            'total': total,
            'page': page,
            'page_size': page_size,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_previous': page > 1,
        }

    def count(self, company_id: str, filters: Optional[Dict[str, Any]] = None, include_deleted: bool = False) -> int:
        """
        统计记录数量
        
        Args:
            company_id: 企业ID（用于数据隔离）
            filters: 过滤条件
            include_deleted: 是否包含已删除的记录
            
        Returns:
            记录数量
        """
        query = Q(company_id=company_id)
        
        if not include_deleted:
            query &= Q(is_deleted=False)
        
        if filters:
            for key, value in filters.items():
                query &= Q(**{key: value})
        
        return self.model.objects.filter(query).count()

    def exists(self, id: str, company_id: str, include_deleted: bool = False) -> bool:
        """
        检查记录是否存在
        
        Args:
            id: 记录ID
            company_id: 企业ID（用于数据隔离）
            include_deleted: 是否包含已删除的记录
            
        Returns:
            是否存在
        """
        return self.get(id, company_id, include_deleted) is not None

    def bulk_create(self, data_list: List[Dict[str, Any]], company_id: str, created_by: Optional[str] = None) -> List[BaseModel]:
        """
        批量创建记录
        
        Args:
            data_list: 要创建的数据字典列表
            company_id: 企业ID（用于数据隔离）
            created_by: 创建人ID
            
        Returns:
            创建的模型实例列表
        """
        instances = []
        for data in data_list:
            data['company_id'] = company_id
            if created_by:
                data['created_by'] = created_by
                data['updated_by'] = created_by
            instance = self.model(**data)
            instance.save()
            instances.append(instance)
        
        return instances

    def bulk_update(self, instances: List[BaseModel], fields: List[str]) -> int:
        """
        批量更新记录
        
        Args:
            instances: 要更新的模型实例列表
            fields: 要更新的字段列表
            
        Returns:
            更新的记录数
        """
        count = 0
        for instance in instances:
            instance.save()
            count += 1
        return count
