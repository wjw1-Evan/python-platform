"""
工具函数
"""
from jose import jwt
from django.conf import settings
from datetime import datetime, timedelta


def generate_jwt_token(user_id):
    """
    生成JWT token
    :param user_id: 用户ID
    :return: token字符串
    """
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_DELTA),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
