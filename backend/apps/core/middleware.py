"""
中间件 - 企业数据隔离
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from bson import ObjectId


class CompanyIsolationMiddleware(MiddlewareMixin):
    """
    企业数据隔离中间件
    从请求中获取当前用户的企业ID，并设置到request中
    """
    
    def process_request(self, request):
        """处理请求，设置当前企业ID"""
        # 从JWT token中获取用户信息
        if hasattr(request, 'user') and request.user.is_authenticated:
            # 从请求头或查询参数中获取企业ID
            company_id = request.headers.get('X-Company-Id') or request.GET.get('company_id')
            
            if company_id:
                try:
                    request.company_id = ObjectId(company_id)
                except:
                    request.company_id = None
            else:
                # 如果没有指定企业ID，使用用户的默认企业
                if hasattr(request.user, 'default_company_id'):
                    request.company_id = request.user.default_company_id
                else:
                    request.company_id = None
        else:
            request.company_id = None
        
        return None
    
    def process_exception(self, request, exception):
        """处理异常"""
        return None
