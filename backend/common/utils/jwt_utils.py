"""
JWT工具函数
"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from typing import Dict, Optional


def generate_token(user_id: str) -> Dict[str, str]:
    """
    生成JWT Token（不包含company_id，从数据库读取）
    
    Args:
        user_id: 用户ID
        
    Returns:
        包含access和refresh token的字典
    """
    # 创建token，只包含user_id
    refresh = RefreshToken()
    refresh['user_id'] = user_id
    
    # 同时设置access token的claims
    access_token = refresh.access_token
    access_token['user_id'] = user_id
    
    return {
        'access': str(access_token),
        'refresh': str(refresh),
    }


def get_user_from_token(token: str) -> Optional[Dict[str, str]]:
    """
    从Token中提取用户信息（只返回user_id，company_id需要从数据库读取）
    
    Args:
        token: JWT Token字符串
        
    Returns:
        包含user_id的字典，或None
    """
    try:
        from rest_framework_simplejwt.tokens import AccessToken
        access_token = AccessToken(token)
        return {
            'user_id': access_token.get('user_id'),
        }
    except TokenError:
        return None


def get_user_company_id(user_id: str) -> Optional[str]:
    """
    从数据库获取用户的company_id（返回第一个激活的企业）
    
    Args:
        user_id: 用户ID
        
    Returns:
        企业ID，如果用户没有关联企业则返回None
    """
    try:
        # 动态导入，避免循环依赖
        from services.company_service.companies.models import UserCompany
        
        # 查询用户关联的第一个激活企业（使用 mongoengine 查询）
        user_company = UserCompany.objects.filter(
            user_id=user_id,
            is_deleted=False,
            is_active=True
        ).first()
        
        if user_company:
            return user_company.company_id
        return None
    except Exception:
        # 如果导入失败或查询失败，返回None
        return None
