"""
日志中间件
自动记录API请求日志
"""
import json
import time
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import OperationLog


class LoggingMiddleware(MiddlewareMixin):
    """
    日志记录中间件
    自动记录所有API请求的详细信息
    """
    
    def process_request(self, request):
        """处理请求开始"""
        # 记录请求开始时间
        request._log_start_time = time.time()
        
        # 获取请求数据
        request._log_request_data = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                if hasattr(request, 'body') and request.body:
                    request._log_request_data = request.body.decode('utf-8')
            except Exception:
                pass
    
    def process_response(self, request, response):
        """处理响应"""
        # 跳过某些路径的日志记录
        skip_paths = ['/admin/', '/static/', '/media/', '/favicon.ico']
        if any(request.path.startswith(path) for path in skip_paths):
            return response
        
        # 计算执行时间
        execution_time = None
        if hasattr(request, '_log_start_time'):
            execution_time = (time.time() - request._log_start_time) * 1000  # 转换为毫秒
        
        # 获取企业ID和用户ID
        company_id = getattr(request, 'company_id', None)
        user_id = getattr(request, 'user_id', None)
        
        if not company_id:
            return response
        
        # 确定日志类型
        log_type = 'api'
        if '/api/auth/login' in request.path:
            log_type = 'login'
        elif '/api/auth/logout' in request.path:
            log_type = 'logout'
        elif request.method == 'POST':
            log_type = 'create'
        elif request.method in ['PUT', 'PATCH']:
            log_type = 'update'
        elif request.method == 'DELETE':
            log_type = 'delete'
        
        # 确定日志级别
        log_level = 'info'
        if response.status_code >= 500:
            log_level = 'error'
        elif response.status_code >= 400:
            log_level = 'warning'
        
        # 获取响应数据（限制长度）
        response_data = None
        if hasattr(response, 'content'):
            try:
                content = response.content.decode('utf-8')
                if len(content) > 1000:  # 限制响应数据长度
                    content = content[:1000] + '...'
                response_data = content
            except Exception:
                pass
        
        # 创建日志记录（使用 mongoengine）
        try:
            log = OperationLog(
                company_id=company_id,
                log_type=log_type,
                log_level=log_level,
                user_id=user_id,
                action=f"{request.method} {request.path}",
                method=request.method,
                path=request.path,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                request_data=request._log_request_data[:5000] if hasattr(request, '_log_request_data') and request._log_request_data else None,
                response_data=response_data,
                status_code=response.status_code,
                execution_time=execution_time,
                created_by=user_id,
            )
            log.save()
        except Exception as e:
            # 日志记录失败不应该影响正常请求
            print(f"Failed to create log: {e}")
        
        return response
    
    def get_client_ip(self, request):
        """获取客户端IP地址"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
