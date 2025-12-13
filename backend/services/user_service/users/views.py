"""
用户视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import User
from .serializers import (
    UserSerializer, UserCreateSerializer, UserUpdateSerializer, LoginSerializer
)
from common.data_factory.crud import BaseCRUD
from bson import ObjectId


user_crud = BaseCRUD(User)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    创建用户（用于注册）
    """
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建用户（此时还没有company_id，会在注册流程中设置）
    user = serializer.save()
    
    return Response({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
    }, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_user_company_id(request, user_id):
    """
    更新用户的company_id（用于注册流程）
    注意：此接口允许匿名访问，仅用于注册时更新company_id
    """
    company_id = request.data.get('company_id')
    if not company_id:
        return Response(
            {'error': '未提供企业ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 查找用户（不检查company_id，因为此时可能还是临时值）
    try:
        from mongoengine import DoesNotExist
        user = User.objects.get(id=user_id, is_deleted=False)
    except DoesNotExist:
        return Response(
            {'error': '用户不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 更新company_id
    user.company_id = company_id
    try:
        user.save()
    except Exception as e:
        return Response(
            {'error': f'更新用户company_id失败: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({
        'id': str(user.id),
        'company_id': str(user.company_id),
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    验证用户登录
    """
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    username = serializer.validated_data['username']
    password = serializer.validated_data['password']
    company_id = serializer.validated_data.get('company_id')
    
    try:
        # 查找用户（使用 mongoengine 查询）
        user = User.objects.filter(username=username, is_deleted=False).first()
        
        if not user or not user.check_password(password):
            return Response(
                {'error': '用户名或密码错误'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': '用户已被禁用'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 更新最后登录时间
        user.last_login = timezone.now()
        user.save()
        
        return Response({
            'user_id': str(user.id),
            'username': user.username,
            'email': user.email,
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': '登录失败', 'details': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, user_id):
    """
    获取用户信息
    """
    company_id = getattr(request, 'company_id', None)
    if not company_id:
        return Response(
            {'error': '未提供企业ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = user_crud.get(user_id, company_id)
    if not user:
        return Response(
            {'error': '用户不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    """
    获取用户列表
    """
    company_id = getattr(request, 'company_id', None)
    if not company_id:
        return Response(
            {'error': '未提供企业ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 获取查询参数
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))
    search = request.GET.get('search', '')
    
    # 构建过滤条件
    filters = {}
    if search:
        filters['username__icontains'] = search
    
    # 获取列表
    result = user_crud.list(
        company_id=company_id,
        filters=filters,
        page=page,
        page_size=page_size
    )
    
    # 序列化
    serializer = UserSerializer(result['items'], many=True)
    
    return Response({
        'items': serializer.data,
        'total': result['total'],
        'page': result['page'],
        'page_size': result['page_size'],
        'total_pages': result['total_pages'],
    }, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    """
    更新用户信息
    """
    company_id = getattr(request, 'company_id', None)
    user_id_from_token = getattr(request, 'user_id', None)
    
    # 只能更新自己的信息，除非是管理员
    if str(user_id) != user_id_from_token:
        return Response(
            {'error': '无权修改其他用户信息'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user = user_crud.get(user_id, company_id)
    if not user:
        return Response(
            {'error': '用户不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    updated_user = user_crud.update(
        user_id,
        serializer.validated_data,
        company_id,
        updated_by=user_id_from_token
    )
    
    result_serializer = UserSerializer(updated_user)
    return Response(result_serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    """
    删除用户（软删除）
    """
    company_id = getattr(request, 'company_id', None)
    
    success = user_crud.delete(user_id, company_id, hard_delete=False)
    if not success:
        return Response(
            {'error': '用户不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
