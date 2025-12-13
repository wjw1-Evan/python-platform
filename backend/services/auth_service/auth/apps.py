from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth'
    label = 'auth_service'  # 使用唯一的标签避免与django.contrib.auth冲突
    
    def ready(self):
        """应用启动时初始化 MongoDB 连接"""
        from common.db import connect_mongodb
        connect_mongodb()
