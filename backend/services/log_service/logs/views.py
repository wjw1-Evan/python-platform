"""
日志视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.data_factory.crud import BaseCRUD
from .models import OperationLog
from .serializers import OperationLogSerializer


class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    操作日志视图集（只读）
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OperationLogSerializer
    crud = BaseCRUD(OperationLog)
    
    def get_queryset(self):
        """获取当前企业下的日志"""
        from mongoengine import Q
        from datetime import datetime
        
        company_id = getattr(self.request, 'company_id', None)
        
        if not company_id:
            return []
        
        query = Q(company_id=company_id, is_deleted=False)
        
        # 过滤条件
        log_type = self.request.query_params.get('log_type')
        log_level = self.request.query_params.get('log_level')
        user_id = self.request.query_params.get('user_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if log_type:
            query &= Q(log_type=log_type)
        if log_level:
            query &= Q(log_level=log_level)
        if user_id:
            query &= Q(user_id=user_id)
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query &= Q(created_at__gte=start_dt)
            except:
                pass
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query &= Q(created_at__lte=end_dt)
            except:
                pass
        
        queryset = OperationLog.objects.filter(query).order_by('-created_at')
        return list(queryset)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """获取日志统计信息"""
        company_id = getattr(request, 'company_id', None)
        
        if not company_id:
            return Response(
                {'error': '无法获取企业ID'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from mongoengine import Q
        from datetime import datetime, timedelta
        
        # 最近7天的日志统计
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_logs = OperationLog.objects.filter(
            Q(company_id=company_id) &
            Q(created_at__gte=seven_days_ago) &
            Q(is_deleted=False)
        )
        
        # 统计
        total = recent_logs.count()
        by_type = {}
        by_level = {}
        errors = 0
        warnings = 0
        
        for log in recent_logs:
            by_type[log.log_type] = by_type.get(log.log_type, 0) + 1
            by_level[log.log_level] = by_level.get(log.log_level, 0) + 1
            if log.log_level == 'error':
                errors += 1
            elif log.log_level == 'warning':
                warnings += 1
        
        stats = {
            'total': total,
            'by_type': by_type,
            'by_level': by_level,
            'errors': errors,
            'warnings': warnings,
        }
        
        return Response(stats)
