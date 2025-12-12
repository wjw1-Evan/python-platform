"""
JWT认证
"""
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from jose import jwt, JWTError
from django.conf import settings
from apps.users.models import User


class JWTAuthentication(BaseAuthentication):
    """
    JWT认证类
    """
    
    def authenticate(self, request):
        """验证token"""
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            user_id = payload.get('user_id')
            
            if not user_id:
                raise AuthenticationFailed('Invalid token')
            
            try:
                user = User.objects.get(id=user_id, is_deleted=False)
            except User.DoesNotExist:
                raise AuthenticationFailed('User not found')
            
            return (user, token)
            
        except JWTError:
            raise AuthenticationFailed('Invalid token')
