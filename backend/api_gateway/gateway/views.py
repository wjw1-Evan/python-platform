"""
API网关视图
统一路由分发和请求转发
"""
import requests
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError


from common.utils.service_config import get_service_url


def forward_request(request, service_name, path=''):
    """
    转发请求到指定服务
    
    Args:
        request: Django请求对象
        service_name: 服务名称
        path: 服务路径（不包含/api/前缀）
    """
    service_url = get_service_url(service_name)
    if not service_url:
        return JsonResponse(
            {'error': f'服务 {service_name} 不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 构建完整URL
    full_path = f'/api/{path}' if path else '/api/'
    url = f'{service_url}{full_path}'
    
    # 获取请求方法
    method = request.method.lower()
    
    # 准备请求参数
    params = request.GET.dict()
    headers = {}
    
    # 复制认证头
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if auth_header:
        headers['Authorization'] = auth_header
    
    # 复制其他重要头
    for key in ['Content-Type', 'Accept']:
        if key in request.META:
            headers[key] = request.META[key]
    
    # 准备请求数据
    data = None
    json_data = None
    if method in ['post', 'put', 'patch']:
        if request.content_type and 'application/json' in request.content_type:
            try:
                import json
                json_data = json.loads(request.body)
            except:
                pass
        else:
            data = request.POST.dict()
    
    try:
        # 发送请求
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            json=json_data,
            data=data,
            timeout=30
        )
        
        # 检查响应内容类型
        content_type = response.headers.get('content-type', '').lower()
        is_json = 'application/json' in content_type
        
        # 尝试解析 JSON 响应
        if is_json:
            try:
                response_data = response.json()
            except ValueError:
                # JSON 解析失败，返回原始文本
                response_data = {'error': '响应解析失败', 'details': response.text[:500]}
        else:
            # 非 JSON 响应（可能是 HTML 错误页面）
            response_data = {
                'error': '服务返回非 JSON 响应',
                'details': response.text[:500] if response.text else '空响应',
                'status_code': response.status_code
            }
        
        # 返回响应
        return JsonResponse(
            response_data,
            status=response.status_code,
            safe=False
        )
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {'error': f'服务调用失败: {str(e)}'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        return JsonResponse(
            {'error': f'请求处理失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """健康检查"""
    return Response({
        'status': 'ok',
        'service': 'api_gateway',
        'version': '1.0.0'
    })


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_service_proxy(request, path=''):
    """用户服务代理"""
    return forward_request(request, 'user_service', f'users/{path}')


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def company_service_proxy(request, path=''):
    """企业服务代理"""
    return forward_request(request, 'company_service', f'companies/{path}')


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def auth_service_proxy(request, path=''):
    """认证服务代理（允许未认证访问）"""
    return forward_request(request, 'auth_service', f'auth/{path}')


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def permission_service_proxy(request, path=''):
    """权限服务代理"""
    return forward_request(request, 'permission_service', f'permissions/{path}')


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def notification_service_proxy(request, path=''):
    """通知服务代理"""
    return forward_request(request, 'notification_service', f'notifications/{path}')


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def log_service_proxy(request, path=''):
    """日志服务代理"""
    return forward_request(request, 'log_service', f'logs/{path}')
