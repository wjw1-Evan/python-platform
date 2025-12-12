"""
企业视图
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.companies.models import Company
from apps.companies.serializers import (
    CompanySerializer, CompanyCreateSerializer, CompanyUpdateSerializer
)
from apps.core.db_factory import DBFactory
from bson import ObjectId


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_companies(request):
    """获取用户所属的企业列表"""
    user = request.user
    company_ids = user.company_ids
    
    companies = Company.objects.filter(
        id__in=company_ids,
        is_deleted=False
    )
    
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company(request, company_id):
    """获取企业详情"""
    try:
        company_id = ObjectId(company_id)
    except:
        return Response({'error': '无效的企业ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # 检查用户是否属于该企业
    if company_id not in user.company_ids:
        return Response({'error': '无权访问该企业'}, status=status.HTTP_403_FORBIDDEN)
    
    company = Company.objects.filter(
        id=company_id,
        is_deleted=False
    ).first()
    
    if not company:
        return Response({'error': '企业不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_company(request):
    """创建企业"""
    serializer = CompanyCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    user = request.user
    
    # 创建企业
    company = Company(
        name=data['name'],
        description=data.get('description', ''),
        logo=data.get('logo', ''),
        owner_id=user.id,
        company_id=ObjectId(),  # 临时值
        created_by=user.id,
    )
    company.save()
    
    # 更新company_id
    company.company_id = company.id
    company.save()
    
    # 添加用户到企业
    company.add_member(user.id)
    
    # 添加企业到用户
    user.add_company(company.id)
    
    serializer = CompanySerializer(company)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_company(request, company_id):
    """更新企业信息"""
    try:
        company_id = ObjectId(company_id)
    except:
        return Response({'error': '无效的企业ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = CompanyUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # 检查用户是否是所有者
    company = Company.objects.filter(
        id=company_id,
        is_deleted=False
    ).first()
    
    if not company:
        return Response({'error': '企业不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if not company.is_owner(user.id):
        return Response({'error': '只有所有者可以修改企业信息'}, status=status.HTTP_403_FORBIDDEN)
    
    data = serializer.validated_data
    if 'name' in data:
        company.name = data['name']
    if 'description' in data:
        company.description = data['description']
    if 'logo' in data:
        company.logo = data['logo']
    
    company.updated_by = user.id
    company.save()
    
    serializer = CompanySerializer(company)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_company(request, company_id):
    """删除企业（软删除）"""
    try:
        company_id = ObjectId(company_id)
    except:
        return Response({'error': '无效的企业ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    company = Company.objects.filter(
        id=company_id,
        is_deleted=False
    ).first()
    
    if not company:
        return Response({'error': '企业不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    if not company.is_owner(user.id):
        return Response({'error': '只有所有者可以删除企业'}, status=status.HTTP_403_FORBIDDEN)
    
    company.soft_delete()
    return Response({'message': '删除成功'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_members(request, company_id):
    """获取企业成员列表"""
    try:
        company_id = ObjectId(company_id)
    except:
        return Response({'error': '无效的企业ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # 检查用户是否属于该企业
    if company_id not in user.company_ids:
        return Response({'error': '无权访问该企业'}, status=status.HTTP_403_FORBIDDEN)
    
    company = Company.objects.filter(
        id=company_id,
        is_deleted=False
    ).first()
    
    if not company:
        return Response({'error': '企业不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    from apps.users.models import User
    members = User.objects.filter(
        id__in=company.member_ids + [company.owner_id],
        is_deleted=False
    )
    
    from apps.users.serializers import UserSerializer
    serializer = UserSerializer(members, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_member(request, company_id):
    """移除企业成员"""
    try:
        company_id = ObjectId(company_id)
        member_id = ObjectId(request.data.get('member_id'))
    except:
        return Response({'error': '无效的ID'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    company = Company.objects.filter(
        id=company_id,
        is_deleted=False
    ).first()
    
    if not company:
        return Response({'error': '企业不存在'}, status=status.HTTP_404_NOT_FOUND)
    
    # 只有所有者可以移除成员
    if not company.is_owner(user.id):
        return Response({'error': '只有所有者可以移除成员'}, status=status.HTTP_403_FORBIDDEN)
    
    # 不能移除所有者
    if company.owner_id == member_id:
        return Response({'error': '不能移除所有者'}, status=status.HTTP_400_BAD_REQUEST)
    
    company.remove_member(member_id)
    
    # 从用户的company_ids中移除
    from apps.users.models import User
    member = User.objects.filter(id=member_id).first()
    if member:
        member.remove_company(company_id)
    
    return Response({'message': '移除成功'})
