"""
通知视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from common.data_factory.crud import BaseCRUD
from .models import Notification
from .serializers import (
    NotificationSerializer,
    NotificationCreateSerializer,
    NotificationUpdateSerializer
)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    通知视图集
    """
    permission_classes = [IsAuthenticated]
    crud = BaseCRUD(Notification)
    
    def get_queryset(self):
        """获取当前用户所在企业的通知"""
        company_id = getattr(self.request, 'company_id', None)
        user_id = getattr(self.request, 'user_id', None)
        
        if not company_id or not user_id:
            return []
        
        queryset = Notification.objects.filter(
            company_id=company_id,
            recipient_id=user_id,
            is_deleted=False
        ).order_by('-created_at')
        return list(queryset)
    
    def get_serializer_class(self):
        """根据操作返回不同的序列化器"""
        if self.action == 'create':
            return NotificationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return NotificationUpdateSerializer
        return NotificationSerializer
    
    def create(self, request, *args, **kwargs):
        """创建通知"""
        company_id = getattr(request, 'company_id', None)
        user_id = getattr(request, 'user_id', None)
        
        if not company_id:
            return Response(
                {'error': '无法获取企业ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        if not data.get('sender_id'):
            data['sender_id'] = user_id
        
        notification = self.crud.create(data, company_id, created_by=user_id)
        
        return Response(
            NotificationSerializer(notification).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """标记为已读"""
        company_id = getattr(request, 'company_id', None)
        notification = self.crud.get(pk, company_id)
        
        if not notification:
            return Response(
                {'error': '通知不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        notification.mark_as_read()
        return Response(NotificationSerializer(notification).data)
    
    @action(detail=True, methods=['post'])
    def mark_archived(self, request, pk=None):
        """标记为已归档"""
        company_id = getattr(request, 'company_id', None)
        notification = self.crud.get(pk, company_id)
        
        if not notification:
            return Response(
                {'error': '通知不存在'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        notification.mark_as_archived()
        return Response(NotificationSerializer(notification).data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """获取未读通知数量"""
        company_id = getattr(request, 'company_id', None)
        user_id = getattr(request, 'user_id', None)
        
        if not company_id or not user_id:
            return Response({'count': 0})
        
        count = Notification.objects.filter(
            company_id=company_id,
            recipient_id=user_id,
            status='unread',
            is_deleted=False
        ).count()
        
        return Response({'count': count})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """标记所有通知为已读"""
        company_id = getattr(request, 'company_id', None)
        user_id = getattr(request, 'user_id', None)
        
        if not company_id or not user_id:
            return Response(
                {'error': '无法获取企业ID或用户ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from datetime import datetime
        notifications = Notification.objects.filter(
            company_id=company_id,
            recipient_id=user_id,
            status='unread',
            is_deleted=False
        )
        count = 0
        for notification in notifications:
            notification.status = 'read'
            notification.read_at = datetime.now()
            notification.save()
            count += 1
        
        return Response({'updated_count': count})
