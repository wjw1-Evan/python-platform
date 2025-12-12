"""
Core应用配置
"""
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'
    
    def ready(self):
        """应用就绪时初始化mongoengine连接"""
        import mongoengine
        from django.conf import settings
        
        # 确保mongoengine已连接
        try:
            # 如果已经有连接，先断开
            mongoengine.disconnect()
        except:
            pass
        
        try:
            if settings.MONGO_DB_USER and settings.MONGO_DB_PASSWORD:
                mongoengine.connect(
                    settings.MONGO_DB_NAME,
                    host=settings.MONGO_DB_HOST,
                    port=settings.MONGO_DB_PORT,
                    username=settings.MONGO_DB_USER,
                    password=settings.MONGO_DB_PASSWORD,
                    authentication_source='admin'
                )
            else:
                mongoengine.connect(
                    settings.MONGO_DB_NAME,
                    host=settings.MONGO_DB_HOST,
                    port=settings.MONGO_DB_PORT
                )
        except Exception as e:
            # 开发环境可以忽略连接错误
            if settings.DEBUG:
                print(f"MongoDB connection warning: {e}")
            pass
