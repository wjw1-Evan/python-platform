"""
API网关路由配置
"""
from django.urls import path
from .views import (
    health_check,
    user_service_proxy,
    company_service_proxy,
    auth_service_proxy,
    permission_service_proxy,
    notification_service_proxy,
    log_service_proxy,
)

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('api/users/', user_service_proxy, name='user_service_proxy'),
    path('api/users/<path:path>', user_service_proxy, name='user_service_proxy_detail'),
    path('api/companies/', company_service_proxy, name='company_service_proxy'),
    path('api/companies/<path:path>', company_service_proxy, name='company_service_proxy_detail'),
    path('api/auth/', auth_service_proxy, name='auth_service_proxy'),
    path('api/auth/<path:path>', auth_service_proxy, name='auth_service_proxy_detail'),
    path('api/permissions/', permission_service_proxy, name='permission_service_proxy'),
    path('api/permissions/<path:path>', permission_service_proxy, name='permission_service_proxy_detail'),
    path('api/notifications/', notification_service_proxy, name='notification_service_proxy'),
    path('api/notifications/<path:path>', notification_service_proxy, name='notification_service_proxy_detail'),
    path('api/logs/', log_service_proxy, name='log_service_proxy'),
    path('api/logs/<path:path>', log_service_proxy, name='log_service_proxy_detail'),
]
