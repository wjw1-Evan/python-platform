"""
通知视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.notifications.models import Notification
from apps.notifications.serializers import NotificationSerializer, NotificationCreateSerializer
from apps.core.db_factory import DBFactory
from bson import ObjectId


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_notifications(request):
    """获取通知列表"""
    user = request.user
    company_id = request.company_id
    
    if not company_id:
        return Response({'error': '请选择企业'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 查询参数
    is_read = request.GET.get('is_read')
    notification_type = request.GET.get('type')
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    
    filters = {
        'user_id': user.id,
        'company_id': company_id,
    }
    
    if is_read is not None:
        filters['is_read'] = is_read.lower() == 'true'
    
    if notification_type:
        filters['type'] = notification_type
    
    skip = (page - 1) * page_size
    
    notifications = DBFactory.list(Notification, company_id, skip=skip, limit=page_size, **filters)
    
    serializer = NotificationSerializer(notifications, many=True)
    
    # 获取总数
    total = DBFactory.count(Notification, company_id, **filters)
    
    return Response({
        'data': serializer.data,
        'total': total,
        'page': page,
        'page_size': page_size,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification(request, notification_id):
    """获取通知详情"""
    try:
        notification_id = ObjectId(notification_id)
    except:
        return Response({'error': '无效的通知ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    company_id = request.company_id
    
    notification = DBFactory.get(Notification, company_id, id=notification_id, user_id=user.id)
    
    if not notification:
        return Response({'error': '通知不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_notification(request):
    """创建通知"""
    serializer = NotificationCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    company_id = request.company_id
    
    if not company_id:
        return Response({'error': '请选择企业'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user_id = ObjectId(data['user_id'])
    except:
        return Response({'error': '无效的用户ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    notification = Notification.create_notification(
        user_id=user_id,
        company_id=company_id,
        title=data['title'],
        content=data['content'],
        type=data.get('type', 'system'),
        priority=data.get('priority', 1),
        link=data.get('link', ''),
        data=data.get('data', {}),
        created_by=request.user.id,
    )
    
    serializer = NotificationSerializer(notification)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    """标记通知为已读"""
    try:
        notification_id = ObjectId(notification_id)
    except:
        return Response({'error': '无效的通知ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    company_id = request.company_id
    
    notification = DBFactory.get(Notification, company_id, id=notification_id, user_id=user.id)
    
    if not notification:
        return Response({'error': '通知不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    notification.mark_as_read()
    
    serializer = NotificationSerializer(notification)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_all_as_read(request):
    """标记所有通知为已读"""
    user = request.user
    company_id = request.company_id
    
    if not company_id:
        return Response({'error': '请选择企业'}, status=status.HTTP_400_BAD_REQUEST)
    
    count = Notification.objects.filter(
        user_id=user.id,
        company_id=company_id,
        is_deleted=False,
        is_read=False
    ).update(is_read=True)
    
    return Response({'message': f'已标记{count}条通知为已读'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_count(request):
    """获取未读通知数量"""
    user = request.user
    company_id = request.company_id
    
    if not company_id:
        return Response({'error': '请选择企业'}, status=status.HTTP_400_BAD_REQUEST)
    
    count = Notification.get_unread_count(user.id, company_id)
    return Response({'count': count})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_notification(request, notification_id):
    """删除通知"""
    try:
        notification_id = ObjectId(notification_id)
    except:
        return Response({'error': '无效的通知ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    company_id = request.company_id
    
    notification = DBFactory.get(Notification, company_id, id=notification_id, user_id=user.id)
    
    if not notification:
        return Response({'error': '通知不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    notification.soft_delete()
    return Response({'message': '删除成功'})
