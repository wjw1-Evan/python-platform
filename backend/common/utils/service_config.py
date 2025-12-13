"""
微服务配置管理
根据运行环境（开发/生产）自动选择服务URL
"""
import os
from decouple import config


def is_docker_environment():
    """
    检测是否在Docker环境中运行
    
    检测方法：
    1. 检查环境变量 DEPLOYMENT_MODE
    2. 检查 MONGODB_HOST 是否为 'mongodb'（Docker服务名）
    3. 检查是否存在 /.dockerenv 文件
    """
    deployment_mode = os.getenv('DEPLOYMENT_MODE', '').lower()
    if deployment_mode in ['production', 'docker', 'prod']:
        return True
    if deployment_mode in ['development', 'dev', 'local']:
        return False
    
    # 自动检测
    mongodb_host = os.getenv('MONGODB_HOST', '')
    if mongodb_host == 'mongodb':
        return True
    
    if os.path.exists('/.dockerenv'):
        return True
    
    return False


def get_service_url(service_name, default_port=None):
    """
    获取微服务URL
    
    Args:
        service_name: 服务名称（如 'user_service', 'auth_service'）
        default_port: 本地开发环境的默认端口（可选）
    
    Returns:
        服务URL字符串
    """
    # 服务端口映射（本地开发环境）
    LOCAL_SERVICE_PORTS = {
        'api_gateway': 8000,
        'user_service': 8001,
        'company_service': 8002,
        'auth_service': 8003,
        'permission_service': 8004,
        'notification_service': 8005,
        'log_service': 8006,
    }
    
    # Docker服务名称映射
    DOCKER_SERVICE_NAMES = {
        'api_gateway': 'api_gateway',
        'user_service': 'user_service',
        'company_service': 'company_service',
        'auth_service': 'auth_service',
        'permission_service': 'permission_service',
        'notification_service': 'notification_service',
        'log_service': 'log_service',
    }
    
    # 环境变量映射
    env_var_map = {
        'api_gateway': 'API_GATEWAY_URL',
        'user_service': 'USER_SERVICE_URL',
        'company_service': 'COMPANY_SERVICE_URL',
        'auth_service': 'AUTH_SERVICE_URL',
        'permission_service': 'PERMISSION_SERVICE_URL',
        'notification_service': 'NOTIFICATION_SERVICE_URL',
        'log_service': 'LOG_SERVICE_URL',
    }
    
    # 1. 优先使用环境变量（如果显式设置）
    env_var = env_var_map.get(service_name)
    if env_var and os.getenv(env_var):
        return os.getenv(env_var)
    
    # 2. 根据环境自动选择
    if is_docker_environment():
        # Docker/生产环境：使用服务名称
        docker_name = DOCKER_SERVICE_NAMES.get(service_name, service_name)
        return f'http://{docker_name}:8000'
    else:
        # 本地开发环境：使用localhost和不同端口
        port = default_port or LOCAL_SERVICE_PORTS.get(service_name, 8000)
        return f'http://localhost:{port}'


def get_all_service_urls():
    """
    获取所有服务的URL配置
    
    Returns:
        dict: 服务名称到URL的映射
    """
    services = [
        'api_gateway',
        'user_service',
        'company_service',
        'auth_service',
        'permission_service',
        'notification_service',
        'log_service',
    ]
    
    return {
        service: get_service_url(service)
        for service in services
    }
