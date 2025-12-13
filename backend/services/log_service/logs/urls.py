"""
日志服务路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OperationLogViewSet

router = DefaultRouter()
router.register(r'logs', OperationLogViewSet, basename='log')

urlpatterns = [
    path('', include(router.urls)),
]
