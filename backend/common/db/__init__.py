"""
MongoDB 数据库连接配置
使用 mongoengine 连接 MongoDB
"""
import mongoengine
from decouple import config


def connect_mongodb():
    """
    连接 MongoDB 数据库
    在 Django 应用启动时调用
    """
    db_name = config('MONGODB_NAME', default='platform_db')
    host = config('MONGODB_HOST', default='mongodb')
    port = config('MONGODB_PORT', default=27017, cast=int)
    username = config('MONGODB_USER', default='admin')
    password = config('MONGODB_PASSWORD', default='admin123')
    auth_source = config('MONGODB_AUTH_SOURCE', default='admin')
    
    mongoengine.connect(
        db=db_name,
        host=host,
        port=port,
        username=username,
        password=password,
        authentication_source=auth_source,
    )


def disconnect_mongodb():
    """
    断开 MongoDB 连接
    """
    mongoengine.disconnect()
