"""
用户视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.users.models import User
from apps.users.serializers import (
    UserSerializer, UserRegisterSerializer, UserLoginSerializer, UserUpdateSerializer
)
from apps.companies.models import Company
from apps.core.utils import generate_jwt_token
from apps.core.db_factory import DBFactory
from bson import ObjectId
from datetime import datetime


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """用户注册"""
    serializer = UserRegisterSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # 检查用户名和邮箱是否已存在
    if User.objects.filter(username=data['username'], is_deleted=False).first():
        return Response({'error': '用户名已存在'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=data['email'], is_deleted=False).first():
        return Response({'error': '邮箱已存在'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 创建用户
    user = User(
        username=data['username'],
        email=data['email'],
        full_name=data.get('full_name', ''),
        phone=data.get('phone', ''),
        company_id=ObjectId(),  # 临时值，创建企业后会更新
        created_by=ObjectId(),
    )
    user.set_password(data['password'])
    
    # 创建企业
    company_name = data.get('company_name') or data['username'] + '的企业'
    company = Company(
        name=company_name,
        owner_id=user.id,
        company_id=ObjectId(),  # 临时值
        created_by=user.id,
    )
    company.save()
    
    # 更新用户的company_id和默认企业
    user.company_id = company.id
    user.company_ids = [company.id]
    user.default_company_id = company.id
    user.save()
    
    # 更新企业的company_id
    company.company_id = company.id
    company.save()
    
    # 生成token
    token = generate_jwt_token(user.id)
    
    user_serializer = UserSerializer(user)
    return Response({
        'token': token,
        'user': user_serializer.data,
        'company': {
            'id': str(company.id),
            'name': company.name,
        }
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # 查找用户
    user = User.objects.filter(
        username=data['username'],
        is_deleted=False,
        is_active=True
    ).first()
    
    if not user or not user.check_password(data['password']):
        return Response({'error': '用户名或密码错误'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # 更新最后登录时间
    user.last_login = datetime.now()
    user.save()
    
    # 生成token
    token = generate_jwt_token(user.id)
    
    user_serializer = UserSerializer(user)
    return Response({
        'token': token,
        'user': user_serializer.data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """获取当前用户信息"""
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """更新当前用户信息"""
    serializer = UserUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    user = request.user
    
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'avatar' in data:
        user.avatar = data['avatar']
    
    user.updated_by = user.id
    user.save()
    
    user_serializer = UserSerializer(user)
    return Response(user_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_company(request):
    """加入企业（需要企业邀请码）"""
    company_code = request.data.get('company_code')
    if not company_code:
        return Response({'error': '企业邀请码不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    company = Company.objects.filter(
        invite_code=company_code,
        is_deleted=False
    ).first()
    
    if not company:
        return Response({'error': '无效的企业邀请码'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # 检查是否已经加入
    if company.id in user.company_ids:
        return Response({'error': '您已经加入该企业'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 添加企业
    user.add_company(company.id)
    
    # 添加用户到企业
    company.add_member(user.id)
    
    user_serializer = UserSerializer(user)
    return Response({
        'message': '成功加入企业',
        'user': user_serializer.data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def switch_company(request):
    """切换默认企业"""
    company_id = request.data.get('company_id')
    if not company_id:
        return Response({'error': '企业ID不能为空'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        company_id = ObjectId(company_id)
    except:
        return Response({'error': '无效的企业ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    if company_id not in user.company_ids:
        return Response({'error': '您不属于该企业'}, status=status.HTTP_403_FORBIDDEN)
    
    user.set_default_company(company_id)
    
    user_serializer = UserSerializer(user)
    return Response({
        'message': '切换成功',
        'user': user_serializer.data,
    })
