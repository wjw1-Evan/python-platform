from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        """应用启动时初始化 MongoDB 连接"""
        from common.db import connect_mongodb
        connect_mongodb()
