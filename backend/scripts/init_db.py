"""
初始化数据库脚本
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User
from apps.companies.models import Company

def init_database():
    """初始化数据库"""
    print("初始化数据库...")
    
    # 创建索引
    print("创建索引...")
    User.ensure_indexes()
    Company.ensure_indexes()
    
    print("数据库初始化完成！")

if __name__ == '__main__':
    init_database()
