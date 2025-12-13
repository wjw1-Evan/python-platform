"""
日志模型
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from common.data_factory.base_model import BaseModel
from mongoengine import StringField, IntField, FloatField, DateTimeField


class OperationLog(BaseModel):
    """
    操作日志模型
    """
    LOG_TYPES = [
        ('api', 'API请求'),
        ('create', '创建操作'),
        ('update', '更新操作'),
        ('delete', '删除操作'),
        ('login', '登录操作'),
        ('logout', '登出操作'),
        ('other', '其他操作'),
    ]
    
    LOG_LEVELS = [
        ('info', '信息'),
        ('warning', '警告'),
        ('error', '错误'),
        ('debug', '调试'),
    ]
    
    log_type = StringField(max_length=20, choices=LOG_TYPES, default='api', verbose_name='日志类型')
    log_level = StringField(max_length=20, choices=LOG_LEVELS, default='info', verbose_name='日志级别')
    user_id = StringField(max_length=24, null=True, blank=True, verbose_name='用户ID')
    action = StringField(required=True, max_length=100, verbose_name='操作')
    resource = StringField(max_length=100, null=True, blank=True, verbose_name='资源')
    resource_id = StringField(max_length=24, null=True, blank=True, verbose_name='资源ID')
    method = StringField(max_length=10, null=True, blank=True, verbose_name='HTTP方法')
    path = StringField(max_length=500, null=True, blank=True, verbose_name='请求路径')
    ip_address = StringField(null=True, blank=True, verbose_name='IP地址')
    user_agent = StringField(max_length=500, null=True, blank=True, verbose_name='用户代理')
    request_data = StringField(null=True, blank=True, verbose_name='请求数据')
    response_data = StringField(null=True, blank=True, verbose_name='响应数据')
    status_code = IntField(null=True, blank=True, verbose_name='状态码')
    error_message = StringField(null=True, blank=True, verbose_name='错误信息')
    execution_time = FloatField(null=True, blank=True, verbose_name='执行时间(ms)')
    
    meta = {
        'collection': 'operation_logs',
        'verbose_name': '操作日志',
        'verbose_name_plural': '操作日志',
        'indexes': [
            ('company_id', 'user_id', 'created_at'),
            ('company_id', 'log_type', 'created_at'),
            ('company_id', 'log_level', 'created_at'),
        ]
    }
