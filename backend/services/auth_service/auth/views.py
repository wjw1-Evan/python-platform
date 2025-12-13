"""
认证视图
"""
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer, TokenRefreshSerializer
from common.utils.jwt_utils import generate_token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    用户注册
    注册时会自动创建一个新企业
    """
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    username = data['username']
    email = data['email']
    password = data['password']
    company_name = data.get('company_name', username)
    
    try:
        # 1. 先创建用户（调用用户服务）
        # 注意：此时还没有企业，使用临时company_id（用户自己的id）
        user_service_url = settings.SERVICE_URLS['user_service']
        user_data = {
            'username': username,
            'email': email,
            'password': password,
            # 不传入company_id，让用户服务使用临时值
        }
        user_response = requests.post(
            f'{user_service_url}/api/users/create/',
            json=user_data,
            timeout=5
        )
        
        if user_response.status_code != 201:
            # 尝试解析错误响应
            try:
                error_details = user_response.json()
            except (ValueError, AttributeError):
                # 如果不是 JSON，返回原始文本
                error_details = user_response.text[:500] if hasattr(user_response, 'text') else str(user_response)
            
            return Response(
                {'error': '创建用户失败', 'details': error_details},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 解析用户创建结果
        try:
            user_result = user_response.json()
        except (ValueError, AttributeError):
            return Response(
                {'error': '创建用户成功，但响应格式错误', 'details': user_response.text[:500] if hasattr(user_response, 'text') else '无法解析响应'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        user_id = user_result['id']
        
        # 2. 创建企业（调用企业服务，使用用户ID作为owner_id）
        company_service_url = settings.SERVICE_URLS['company_service']
        company_data = {
            'name': company_name,
            'owner_id': user_id,  # 使用用户ID作为所有者
        }
        company_response = requests.post(
            f'{company_service_url}/api/companies/create/',
            json=company_data,
            timeout=5
        )
        
        if company_response.status_code != 201:
            # 尝试解析错误响应
            try:
                error_details = company_response.json()
            except (ValueError, AttributeError):
                error_details = company_response.text[:500] if hasattr(company_response, 'text') else str(company_response)
            
            # 如果创建企业失败，需要删除已创建的用户（实际生产环境应该使用事务）
            try:
                # 注意：这里需要认证，暂时跳过删除用户
                # 实际生产环境应该使用事务或补偿机制
                pass
            except Exception:
                pass
            
            return Response(
                {'error': '创建企业失败', 'details': error_details},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 解析企业创建结果
        try:
            company_result = company_response.json()
        except (ValueError, AttributeError):
            return Response(
                {'error': '创建企业成功，但响应格式错误', 'details': company_response.text[:500] if hasattr(company_response, 'text') else '无法解析响应'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        company_id = company_result['id']
        
        # 3. 更新用户的company_id为企业ID（调用用户服务）
        update_user_response = requests.patch(
            f'{user_service_url}/api/users/{user_id}/update_company_id/',
            json={'company_id': company_id},
            timeout=5
        )
        
        if update_user_response.status_code not in [200, 201]:
            # 尝试解析错误响应
            try:
                error_details = update_user_response.json()
            except (ValueError, AttributeError):
                error_details = update_user_response.text[:500] if hasattr(update_user_response, 'text') else str(update_user_response)
            
            # 如果更新用户company_id失败，不影响注册流程，但记录警告
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'更新用户company_id失败: {error_details}')
        
        # 4. 将用户加入企业（调用企业服务）
        join_response = requests.post(
            f'{company_service_url}/api/companies/{company_id}/join/',
            json={'user_id': user_id},
            timeout=5
        )
        
        if join_response.status_code not in [200, 201]:
            # 尝试解析错误响应
            try:
                error_details = join_response.json()
            except (ValueError, AttributeError):
                error_details = join_response.text[:500] if hasattr(join_response, 'text') else str(join_response)
            
            # 如果加入企业失败，不影响注册流程，因为用户已经设置了company_id
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'用户加入企业失败: {error_details}')
        
        # 4. 生成JWT Token（不包含company_id，从数据库读取）
        tokens = generate_token(user_id)
        
        return Response({
            'message': '注册成功',
            'user_id': user_id,
            'company_id': company_id,
            **tokens
        }, status=status.HTTP_201_CREATED)
        
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': '服务调用失败', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': '注册失败', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    用户登录
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    username = data['username']
    password = data['password']
    company_id = data.get('company_id')
    
    try:
        # 验证用户（调用用户服务）
        user_service_url = settings.SERVICE_URLS['user_service']
        login_data = {
            'username': username,
            'password': password,
        }
        if company_id:
            login_data['company_id'] = company_id
        
        user_response = requests.post(
            f'{user_service_url}/api/users/login/',
            json=login_data,
            timeout=5
        )
        
        if user_response.status_code != 200:
            return Response(
                {'error': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        user_result = user_response.json()
        user_id = user_result['user_id']
        
        # 如果没有指定company_id，使用用户的默认企业
        if not company_id:
            # 获取用户的默认企业（调用企业服务）
            company_service_url = settings.SERVICE_URLS['company_service']
            companies_response = requests.get(
                f'{company_service_url}/api/companies/user/{user_id}/',
                timeout=5
            )
            
            if companies_response.status_code == 200:
                companies = companies_response.json()
                if companies and len(companies) > 0:
                    company_id = companies[0]['id']
                else:
                    return Response(
                        {'error': '用户没有关联的企业'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'error': '获取企业信息失败'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        # 生成JWT Token（不包含company_id，从数据库读取）
        tokens = generate_token(user_id)
        
        return Response({
            'message': '登录成功',
            'user_id': user_id,
            'company_id': company_id,
            **tokens
        }, status=status.HTTP_200_OK)
        
    except requests.exceptions.RequestException as e:
        return Response(
            {'error': '服务调用失败', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': '登录失败', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    刷新Token
    """
    serializer = TokenRefreshSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    refresh_token_str = serializer.validated_data['refresh']
    
    try:
        refresh = RefreshToken(refresh_token_str)
        # 从refresh token中获取user_id
        user_id = refresh.get('user_id')
        
        # 创建新的access token，只包含user_id
        access_token = refresh.access_token
        access_token['user_id'] = user_id
        
        return Response({
            'access': str(access_token),
        }, status=status.HTTP_200_OK)
    except TokenError:
        return Response(
            {'error': '无效的刷新Token'},
            status=status.HTTP_401_UNAUTHORIZED
        )
