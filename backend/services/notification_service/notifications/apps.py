from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = '通知服务'
    
    def ready(self):
        """应用启动时初始化 MongoDB 连接"""
        from common.db import connect_mongodb
        connect_mongodb()
