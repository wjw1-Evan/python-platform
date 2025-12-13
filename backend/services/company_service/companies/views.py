"""
企业视图
"""
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
from .models import Company, UserCompany
from .serializers import (
    CompanySerializer, CompanyCreateSerializer, CompanyUpdateSerializer,
    UserCompanySerializer, JoinCompanySerializer
)
from common.data_factory.crud import BaseCRUD
from bson import ObjectId


company_crud = BaseCRUD(Company)
user_company_crud = BaseCRUD(UserCompany)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_company(request):
    """
    创建企业（用于注册）
    """
    serializer = CompanyCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    company = serializer.save()
    
    return Response({
        'id': str(company.id),
        'name': company.name,
        'code': company.code,
        'owner_id': company.owner_id,
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_company(request, company_id):
    """
    获取企业信息
    """
    # 企业信息使用自己的company_id（即自己的id）
    company = company_crud.get(company_id, company_id)
    if not company:
        return Response(
            {'error': '企业不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = CompanySerializer(company)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_companies(request):
    """
    获取企业列表（当前用户关联的企业）
    """
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response(
            {'error': '未提供用户ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 获取用户关联的企业（使用 mongoengine 查询）
    user_companies = UserCompany.objects.filter(
        user_id=user_id,
        is_deleted=False,
        is_active=True
    )
    
    company_ids = [uc.company_id for uc in user_companies]
    
    # 获取企业详情
    companies = []
    for company_id in company_ids:
        company = company_crud.get(company_id, company_id)
        if company:
            companies.append(company)
    
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_companies(request, user_id):
    """
    获取用户关联的企业列表（用于登录时选择企业）
    """
    user_companies = UserCompany.objects.filter(
        user_id=user_id,
        is_deleted=False,
        is_active=True
    )
    
    company_ids = [uc.company_id for uc in user_companies]
    
    companies = []
    for company_id in company_ids:
        company = company_crud.get(company_id, company_id)
        if company:
            companies.append(company)
    
    serializer = CompanySerializer(companies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_company(request, company_id):
    """
    更新企业信息
    """
    user_id = getattr(request, 'user_id', None)
    
    # 检查权限（只有所有者或管理员可以更新）
    company = company_crud.get(company_id, company_id)
    if not company:
        return Response(
            {'error': '企业不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 检查用户是否是企业所有者或管理员（使用 mongoengine 查询）
    user_company = UserCompany.objects.filter(
        user_id=user_id,
        company_id=company_id,
        is_deleted=False
    ).first()
    
    if not user_company or user_company.role not in ['owner', 'admin']:
        return Response(
            {'error': '无权修改企业信息'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = CompanyUpdateSerializer(company, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    updated_company = company_crud.update(
        company_id,
        serializer.validated_data,
        company_id,
        updated_by=user_id
    )
    
    result_serializer = CompanySerializer(updated_company)
    return Response(result_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def set_company_owner(request, company_id):
    """
    设置企业所有者（用于注册流程）
    注意：此接口允许匿名访问，仅用于注册时设置owner_id
    """
    owner_id = request.data.get('owner_id')
    if not owner_id:
        return Response(
            {'error': '未提供所有者ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 检查企业是否存在
    company = company_crud.get(company_id, company_id)
    if not company:
        return Response(
            {'error': '企业不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 检查是否已经设置了owner_id
    if company.owner_id:
        return Response(
            {'error': '企业已有所有者'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 更新owner_id
    company.owner_id = owner_id
    company.save()
    
    serializer = CompanySerializer(company)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_company(request, company_id):
    """
    用户加入企业
    """
    serializer = JoinCompanySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = serializer.validated_data['user_id']
    
    # 检查企业是否存在
    company = company_crud.get(company_id, company_id)
    if not company:
        return Response(
            {'error': '企业不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 检查是否已经加入（使用 mongoengine 查询）
    existing = UserCompany.objects.filter(
        user_id=user_id,
        company_id=company_id,
        is_deleted=False
    ).first()
    
    if existing:
        if existing.is_active:
            return Response(
                {'error': '用户已经加入该企业'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            # 重新激活
            existing.is_active = True
            existing.save()
            serializer = UserCompanySerializer(existing)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 创建关联（使用企业的company_id）
    user_company = UserCompany(
        user_id=user_id,
        company_id=company_id,
        role='member'
    )
    user_company.company_id = company_id  # 设置company_id用于数据隔离
    user_company.save()
    
    serializer = UserCompanySerializer(user_company)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_company(request, company_id):
    """
    用户退出企业
    """
    user_id = getattr(request, 'user_id', None)
    if not user_id:
        return Response(
            {'error': '未提供用户ID'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 查找关联（使用 mongoengine 查询）
    user_company = UserCompany.objects.filter(
        user_id=user_id,
        company_id=company_id,
        is_deleted=False
    ).first()
    
    if not user_company:
        return Response(
            {'error': '用户未加入该企业'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 不能退出自己拥有的企业
    company = company_crud.get(company_id, company_id)
    if company and company.owner_id == user_id:
        return Response(
            {'error': '不能退出自己拥有的企业'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 软删除关联
    user_company.soft_delete()
    
    return Response({'message': '退出企业成功'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_company(request, company_id):
    """
    删除企业（软删除）
    """
    user_id = getattr(request, 'user_id', None)
    
    company = company_crud.get(company_id, company_id)
    if not company:
        return Response(
            {'error': '企业不存在'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 只有所有者可以删除
    if company.owner_id != user_id:
        return Response(
            {'error': '只有企业所有者可以删除企业'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    success = company_crud.delete(company_id, company_id, hard_delete=False)
    if not success:
        return Response(
            {'error': '删除失败'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return Response({'message': '删除成功'}, status=status.HTTP_200_OK)
