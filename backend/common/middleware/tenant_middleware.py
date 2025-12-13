"""
多租户中间件
自动从JWT Token中提取用户ID，从数据库读取企业ID，并注入到请求中
"""
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from typing import Optional
from common.utils.jwt_utils import get_user_company_id


class TenantMiddleware(MiddlewareMixin):
    """
    多租户中间件
    从请求头中提取JWT Token，解析出user_id，然后从数据库读取company_id，并添加到request对象中
    """
    
    def process_request(self, request):
        """
        处理请求，提取用户ID，从数据库读取企业ID
        """
        request.company_id = None
        request.user_id = None
        
        # 从请求头获取Token
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            access_token = AccessToken(token)
            request.user_id = access_token.get('user_id')
            
            # 从数据库读取用户的company_id
            if request.user_id:
                request.company_id = get_user_company_id(request.user_id)
        except (TokenError, Exception):
            # Token无效或解析失败，继续处理请求（可能是公开接口）
            pass
        
        return None
