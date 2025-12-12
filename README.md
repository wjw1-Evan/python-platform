# 通用Admin平台

基于Python+Django+MongoDB+Ant Design Pro的通用管理平台，支持多企业、数据隔离、消息通知和完整日志系统。

## 技术栈

- **后端**: Python 3.11 + Django 4.2 + MongoDB
- **前端**: Ant Design Pro (React)
- **数据库**: MongoDB 7.0
- **缓存**: Redis 7
- **容器化**: Docker + Docker Compose

## 功能特性

- ✅ 用户登录注册
- ✅ 多企业用户管理
- ✅ 用户与企业多对多关系
- ✅ 注册用户自动创建企业
- ✅ 企业邀请码加入机制
- ✅ 企业间数据完全隔离
- ✅ 完整的消息通知系统（支持WebSocket实时推送）
- ✅ 完整的操作日志模块
- ✅ 完整的系统日志模块
- ✅ 数据工厂统一数据库操作
- ✅ 模型基类自动管理

## 项目结构

```
.
├── backend/                 # Django后端
│   ├── apps/
│   │   ├── core/           # 核心模块（数据工厂、基类、中间件）
│   │   ├── users/          # 用户模块
│   │   ├── companies/      # 企业模块
│   │   ├── notifications/  # 通知模块
│   │   └── logs/           # 日志模块
│   ├── config/             # Django配置
│   └── manage.py
├── frontend/               # Ant Design Pro前端
├── docker-compose.yml      # Docker编排文件
└── README.md
```

## 快速开始

### 1. 克隆Django源码（可选）

```bash
git clone https://github.com/django/django.git
```

### 2. 启动服务

```bash
# 使用Docker Compose启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 3. 初始化数据库

```bash
# 进入后端容器
docker-compose exec backend bash

# 创建超级用户（可选）
python manage.py createsuperuser
```

### 4. 访问服务

- 后端API: http://localhost:8000/api/
- 前端界面: http://localhost:3000
- MongoDB: localhost:27017
- Redis: localhost:6379

## API文档

### 用户认证

- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `GET /api/auth/profile/` - 获取当前用户信息
- `PUT /api/auth/update-profile/` - 更新用户信息
- `POST /api/auth/join-company/` - 加入企业
- `POST /api/auth/switch-company/` - 切换默认企业

### 企业管理

- `GET /api/companies/` - 获取企业列表
- `POST /api/companies/create/` - 创建企业
- `GET /api/companies/{id}/` - 获取企业详情
- `PUT /api/companies/{id}/update/` - 更新企业信息
- `DELETE /api/companies/{id}/delete/` - 删除企业
- `GET /api/companies/{id}/members/` - 获取企业成员
- `POST /api/companies/{id}/remove-member/` - 移除成员

### 通知管理

- `GET /api/notifications/` - 获取通知列表
- `POST /api/notifications/create/` - 创建通知
- `GET /api/notifications/unread-count/` - 获取未读数量
- `POST /api/notifications/mark-all-read/` - 标记全部已读
- `POST /api/notifications/{id}/read/` - 标记已读
- `DELETE /api/notifications/{id}/delete/` - 删除通知

### 日志管理

- `GET /api/logs/operation/` - 获取操作日志
- `GET /api/logs/operation/{id}/` - 获取操作日志详情
- `GET /api/logs/system/` - 获取系统日志（仅管理员）
- `GET /api/logs/system/{id}/` - 获取系统日志详情

## 环境变量

创建 `backend/.env` 文件：

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=admin_platform
DATABASE_HOST=mongodb
DATABASE_PORT=27017
DATABASE_USER=admin
DATABASE_PASSWORD=admin123
REDIS_HOST=redis
REDIS_PORT=6379
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

## 数据工厂使用

所有模型继承自 `BaseModel`，使用 `DBFactory` 进行统一操作：

```python
from apps.core.db_factory import DBFactory
from apps.users.models import User

# 创建
user = DBFactory.create(User, company_id, created_by=user_id, username='test', email='test@example.com')

# 查询
user = DBFactory.get(User, company_id, username='test')

# 列表
users = DBFactory.list(User, company_id, skip=0, limit=20)

# 更新
DBFactory.update(User, company_id, {'username': 'test'}, {'email': 'new@example.com'})

# 删除（软删除）
DBFactory.delete(User, company_id, username='test')
```

## 开发说明

### 后端开发

```bash
cd backend
pip install -r requirements.txt
python manage.py runserver
```

### 前端开发

```bash
cd frontend
npm install
npm start
```

## 许可证

MIT
