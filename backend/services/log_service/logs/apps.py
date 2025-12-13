from django.apps import AppConfig


class LogsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'logs'
    verbose_name = '日志服务'
    
    def ready(self):
        """应用启动时初始化 MongoDB 连接"""
        from common.db import connect_mongodb
        connect_mongodb()
