# Django源码配置说明

## 目录结构

```
backend/
├── django/                    # Django源码（已克隆）
│   ├── django/               # Django核心包
│   ├── tests/                # Django测试套件
│   ├── docs/                 # Django文档
│   └── ...
├── common/                    # 公共模块
├── services/                  # 微服务（各服务均为独立Django项目）
│   ├── user_service/
│   ├── company_service/
│   ├── auth_service/
│   └── ...
└── api_gateway/              # API网关（Django项目）
```

## Django源码使用方式

### 方式1: 开发模式安装（推荐）

在虚拟环境中以开发模式安装Django源码：

```bash
cd backend/django
pip install -e .
```

这样可以在项目中使用Django源码进行开发和调试。

### 方式2: 直接引用

在`requirements.txt`中添加：

```
-e ./django
```

### 方式3: PYTHONPATH方式

在启动脚本或环境变量中设置：

```bash
export PYTHONPATH=/path/to/backend/django:$PYTHONPATH
```

## 项目结构配置

本项目采用微服务架构，每个服务都是独立的Django项目：

### 服务目录结构

每个微服务遵循标准Django项目结构：

```
service_name/
├── manage.py                 # Django管理脚本
├── service_name/             # 项目配置目录
│   ├── __init__.py
│   ├── settings.py           # Django配置
│   ├── urls.py               # URL路由
│   ├── wsgi.py               # WSGI配置
│   └── asgi.py               # ASGI配置（如需要）
└── app_name/                 # 应用目录
    ├── __init__.py
    ├── models.py             # 数据模型
    ├── views.py              # 视图
    ├── serializers.py        # 序列化器（DRF）
    ├── urls.py               # 应用URL
    └── ...
```

### 配置要点

1. **settings.py配置**
   - 使用Djongo作为MongoDB后端
   - 配置JWT认证
   - 配置CORS（跨域）
   - 配置Redis（缓存和WebSocket）

2. **公共模块引用**
   - 通过Python路径引用`common`模块
   - 使用`common.data_factory.base_model.BaseModel`
   - 使用`common.data_factory.crud.BaseCRUD`

3. **数据库配置**
   - MongoDB连接配置
   - 使用Djongo适配器

## 更新Django源码

### 从Gitee更新

```bash
cd backend/django
git pull origin main  # 或 master
```

### 从GitHub更新

```bash
cd backend/django
git fetch upstream
git merge upstream/main  # 或 upstream/master
```

## 注意事项

1. **不要直接修改Django源码**
   - 除非是在进行Django本身的功能开发
   - 业务逻辑应放在各自的微服务中

2. **使用虚拟环境**
   - 建议在虚拟环境中安装Django源码
   - 避免与系统Python环境冲突

3. **版本管理**
   - Django源码使用Git管理
   - 可以切换到特定版本或分支进行测试

4. **生产环境**
   - 生产环境建议使用PyPI上的稳定版本
   - 例如：`pip install django==4.2.x`

## 开发环境配置

### 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 安装依赖

**方式1: 使用PyPI版本（推荐，默认）**

```bash
pip install -r requirements.txt
```

**方式2: 使用本地Django源码（开发调试）**

```bash
# 修改requirements.txt，注释掉Django>=4.2.0，启用-e ./django
pip install -r requirements.txt
cd django && pip install -e . && cd ..
```

**方式3: 使用环境变量控制（高级）**

```bash
# 设置环境变量启用本地Django
export USE_LOCAL_DJANGO=true
pip install -r requirements.txt
```

然后在各服务的`settings.py`开头添加：

```python
# 在settings.py开头添加
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR.parent.parent  # backend目录

# 可选：使用本地Django源码（如果设置了USE_LOCAL_DJANGO环境变量）
if os.getenv('USE_LOCAL_DJANGO', 'false').lower() == 'true':
    django_source = BACKEND_DIR / 'django'
    if django_source.exists():
        sys.path.insert(0, str(django_source))
```

### 验证安装

```bash
# 检查Django版本
python -c "import django; print(f'Django版本: {django.get_version()}')"

# 查看Django路径（确认是否使用本地源码）
python -c "import django; print(f'Django路径: {django.__file__}')"

# 使用配置辅助函数检查
python -c "from common.django_path_config import is_using_local_django; print(f'使用本地Django: {is_using_local_django()}')"
```
