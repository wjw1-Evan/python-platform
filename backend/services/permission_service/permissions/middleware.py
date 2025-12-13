"""
权限验证中间件
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework import status


class PermissionMiddleware(MiddlewareMixin):
    """
    权限验证中间件
    根据请求路径和用户角色验证权限
    """
    
    # 不需要权限验证的路径
    EXEMPT_PATHS = [
        '/admin/',
        '/api/auth/',
        '/api/permissions/check/',  # 权限检查接口本身
    ]
    
    def process_request(self, request):
        """
        处理请求，验证权限
        """
        # 跳过不需要验证的路径
        path = request.path
        for exempt_path in self.EXEMPT_PATHS:
            if path.startswith(exempt_path):
                return None
        
        # 如果没有company_id，跳过权限验证（可能是公开接口）
        company_id = getattr(request, 'company_id', None)
        user_id = getattr(request, 'user_id', None)
        
        if not company_id or not user_id:
            return None
        
        # 这里可以添加更详细的权限验证逻辑
        # 例如：检查用户是否有访问特定资源的权限
        # 暂时允许所有已认证用户访问
        
        return None
