"""
Django源码路径配置辅助模块

此模块用于配置Python路径，以便项目可以使用本地的Django源码进行开发。
在生产环境中，应该使用PyPI上发布的Django版本。
"""
import os
import sys
from pathlib import Path


def setup_django_source_path(backend_base_dir=None):
    """
    配置Django源码路径（可选）
    
    如果backend/django目录存在，将其添加到Python路径中。
    这样可以使用本地Django源码进行开发和调试。
    
    Args:
        backend_base_dir: backend目录的路径，如果为None则自动检测
    
    Returns:
        bool: 是否成功添加了Django源码路径
    """
    if backend_base_dir is None:
        # 自动检测：从当前文件位置推断backend目录
        current_file = Path(__file__).resolve()
        backend_base_dir = current_file.parent.parent
    
    backend_base_dir = Path(backend_base_dir)
    django_source_dir = backend_base_dir / 'django'
    
    # 检查Django源码目录是否存在
    if django_source_dir.exists() and django_source_dir.is_dir():
        django_path = str(django_source_dir.resolve())
        
        # 如果还没有在路径中，则添加
        if django_path not in sys.path:
            sys.path.insert(0, django_path)
            print(f"✓ Django源码路径已添加: {django_path}")
            return True
    
    return False


def is_using_local_django():
    """
    检查是否在使用本地Django源码
    
    Returns:
        bool: 如果Django的路径包含backend/django，返回True
    """
    try:
        import django
        django_path = Path(django.__file__).resolve()
        return 'backend' in str(django_path) and 'django' in str(django_path)
    except ImportError:
        return False


# 环境变量控制：设置 USE_LOCAL_DJANGO=true 来启用本地Django源码
USE_LOCAL_DJANGO = os.getenv('USE_LOCAL_DJANGO', 'false').lower() == 'true'

if USE_LOCAL_DJANGO:
    setup_django_source_path()
