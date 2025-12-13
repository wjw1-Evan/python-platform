"""
公共工具函数
"""
# 服务配置可以独立导入（不依赖Django）
from .service_config import (
    get_service_url,
    get_all_service_urls,
    is_docker_environment,
)

__all__ = [
    # 服务配置（总是可用）
    'get_service_url',
    'get_all_service_urls',
    'is_docker_environment',
]

# JWT工具需要Django环境，延迟导入
# 在Django环境中使用时，可以直接导入：
# from common.utils.jwt_utils import generate_token
