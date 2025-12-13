# 通用Admin平台

基于Django + MongoDB + 微服务架构的通用Admin平台，支持多企业用户管理、消息通知、日志记录等功能。

## 技术栈

- **后端**: Python 3.10+, Django 6, MongoEngine (MongoDB ODM), Django REST Framework
- **数据库**: MongoDB 7.0
- **缓存**: Redis 7
- **前端**: React 19, Ant Design 5, Ant Design Pro, UmiJS Max
- **认证**: JWT Token (djangorestframework-simplejwt)
- **实时通信**: WebSocket (Django Channels)
- **容器化**: Docker + Docker Compose
- **架构**: 微服务架构（6个服务 + API网关）

## 功能特性

- ✅ 用户登录注册
- ✅ 多企业用户管理
- ✅ 用户与企业多对多关系
- ✅ 注册用户自动创建企业
- ✅ 企业数据隔离
- ✅ 完整的消息通知系统（WebSocket实时推送）
- ✅ 完整的日志模块（自动记录API请求）
- ✅ 完整的用户管理
- ✅ 权限管理系统
- ✅ API网关统一路由

## 项目结构

```
python-platform/
├── backend/                    # 后端服务
│   ├── common/                # 公共模块
│   │   ├── data_factory/      # 数据工厂
│   │   │   ├── base_model.py  # 模型基类
│   │   │   └── crud.py        # 统一CRUD接口
│   │   ├── middleware/        # 中间件
│   │   │   └── tenant_middleware.py  # 多租户中间件
│   │   └── utils/             # 工具函数
│   │       └── jwt_utils.py    # JWT工具
│   ├── services/              # 微服务
│   │   ├── user_service/      # 用户服务 (端口: 8001)
│   │   ├── company_service/   # 企业服务 (端口: 8002)
│   │   ├── auth_service/      # 认证服务 (端口: 8003)
│   │   ├── permission_service/# 权限服务 (端口: 8004)
│   │   ├── notification_service/# 通知服务 (端口: 8005)
│   │   └── log_service/       # 日志服务 (端口: 8006)
│   ├── api_gateway/           # API网关 (端口: 8000)
│   └── requirements.txt
├── frontend/                  # Ant Design Pro前端
│   ├── src/                   # 源代码
│   │   ├── pages/            # 页面组件
│   │   │   ├── user/         # 用户相关页面（登录、注册、列表）
│   │   │   ├── company/      # 企业管理页面
│   │   │   ├── notification/ # 通知页面
│   │   │   └── log/          # 日志查看页面
│   │   ├── services/         # API服务定义
│   │   └── components/       # 公共组件
│   ├── config/               # 配置文件
│   └── package.json
├── docker/                    # Docker配置
│   └── Dockerfile.backend
├── docker-compose.yml
├── .cursorrules              # Cursor开发规范
└── README.md
```

## 快速开始

### 前置要求

- Docker 和 Docker Compose
- Python 3.10+ (本地开发)

### 启动服务

1. 克隆项目（如果需要）
```bash
git clone <repository-url>
cd python-platform
```

2. 启动所有服务
```bash
docker-compose up -d
```

3. 查看服务状态
```bash
docker-compose ps
```

4. 查看日志
```bash
docker-compose logs -f
```

### 服务端口

- **API网关**: http://localhost:8000
- **用户服务**: http://localhost:8001
- **企业服务**: http://localhost:8002
- **认证服务**: http://localhost:8003
- **权限服务**: http://localhost:8004
- **通知服务**: http://localhost:8005
- **日志服务**: http://localhost:8006
- **前端**: http://localhost:3000（开发模式，代理API到8000）
- **MongoDB**: localhost:27017
- **Redis**: localhost:6379

## API文档

### 认证接口

#### 用户注册
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123",
  "company_name": "测试企业"
}
```

#### 用户登录
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123",
  "company_id": "optional_company_id"
}
```

响应：
```json
{
  "message": "登录成功",
  "user_id": "user_id",
  "company_id": "company_id",
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

**注意**：
- JWT Token 中只包含 `user_id`，不包含 `company_id`
- `company_id` 从数据库的 `UserCompany` 表中实时读取（返回用户第一个激活的企业）
- 如果登录时指定了 `company_id`，会验证用户是否属于该企业
- 如果未指定 `company_id`，会自动使用用户关联的第一个激活企业

#### 刷新Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "jwt_refresh_token"
}
```

响应：
```json
{
  "access": "new_jwt_access_token"
}
```

**注意**：
- 刷新后的 Token 只包含 `user_id`，不包含 `company_id`
- `company_id` 会在每次请求时从数据库实时读取

### 用户接口

所有用户接口需要JWT认证，在请求头中添加：
```
Authorization: Bearer <access_token>
```

**认证说明**：
- JWT Token 中只包含 `user_id`
- `TenantMiddleware` 会自动从数据库读取用户的 `company_id` 并注入到请求中
- 在视图中通过 `request.company_id` 和 `request.user_id` 访问
- 如果用户没有关联企业，`request.company_id` 为 `None`

#### 获取用户列表
```http
GET /api/users/?page=1&page_size=20&search=keyword
```

#### 获取用户详情
```http
GET /api/users/{user_id}/
```

#### 更新用户信息
```http
PUT /api/users/{user_id}/
Content-Type: application/json

{
  "full_name": "新名称",
  "phone": "13800138000"
}
```

### 企业接口

#### 获取企业列表
```http
GET /api/companies/
```

#### 获取企业详情
```http
GET /api/companies/{company_id}/
```

#### 用户加入企业
```http
POST /api/companies/{company_id}/join/
Content-Type: application/json

{
  "user_id": "user_id"
}
```

#### 用户退出企业
```http
POST /api/companies/{company_id}/leave/
```

### 通知接口

#### 获取通知列表
```http
GET /api/notifications/
```

#### 获取未读通知数量
```http
GET /api/notifications/unread_count/
```

#### 标记通知为已读
```http
POST /api/notifications/{notification_id}/mark_read/
```

#### 标记所有通知为已读
```http
POST /api/notifications/mark_all_read/
```

### 日志接口

#### 获取日志列表
```http
GET /api/logs/?log_type=api&log_level=error&page=1&page_size=20
```

#### 获取日志统计
```http
GET /api/logs/statistics/
```

## WebSocket连接

### 通知WebSocket

连接地址：
```
ws://localhost:8005/ws/notifications/?token=<access_token>
```

**连接说明**：
- WebSocket 连接时会从 Token 中提取 `user_id`
- 然后从数据库的 `UserCompany` 表查询用户的 `company_id`
- 如果用户没有关联企业，连接会被拒绝

消息格式：
```json
{
  "type": "notification",
  "title": "通知标题",
  "content": "通知内容",
  "notification_type": "info"
}
```

## 数据模型

### 核心模型

- **User**: 用户模型
- **Company**: 企业模型
- **UserCompany**: 用户-企业关联（多对多）
- **Role**: 角色模型
- **Permission**: 权限模型
- **UserRole**: 用户-角色关联
- **RolePermission**: 角色-权限关联
- **Notification**: 通知模型
- **OperationLog**: 操作日志模型

所有模型都继承自 `BaseModel`，包含以下通用字段：
- `id`: ObjectId主键
- `company_id`: 企业ID（用于数据隔离）
- `created_at`: 创建时间
- `updated_at`: 更新时间
- `is_deleted`: 软删除标记
- `created_by`: 创建人ID
- `updated_by`: 更新人ID

**重要说明**：
- `company_id` 用于多租户数据隔离
- JWT Token 中**不包含** `company_id`，只包含 `user_id`
- `company_id` 从数据库的 `UserCompany` 表中实时读取
- `TenantMiddleware` 会自动将 `company_id` 注入到每个请求中

## 开发指南

### 创建新模型

1. 继承 `BaseModel`
2. 定义字段
3. 使用 `BaseCRUD` 进行数据操作

示例：
```python
from common.data_factory.base_model import BaseModel
from django.db import models

class MyModel(BaseModel):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'my_models'
```

### 创建新服务

1. 在 `backend/services/` 下创建服务目录
2. 创建Django项目结构
3. 配置 `settings.py`
4. 在 `docker-compose.yml` 中添加服务配置

### 数据工厂使用

```python
from common.data_factory.crud import BaseCRUD
from .models import MyModel

crud = BaseCRUD(MyModel)

# 创建
instance = crud.create(data, company_id, created_by=user_id)

# 查询
instance = crud.get(id, company_id)

# 更新
instance = crud.update(id, data, company_id, updated_by=user_id)

# 删除（软删除）
crud.delete(id, company_id)

# 列表
result = crud.list(company_id, filters={}, page=1, page_size=20)
```

### 在视图中获取company_id

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def my_view(request):
    # 从request对象获取company_id和user_id（由TenantMiddleware自动注入）
    company_id = getattr(request, 'company_id', None)
    user_id = getattr(request, 'user_id', None)
    
    if not company_id:
        return Response(
            {'error': '用户未关联企业，请先加入企业'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 使用company_id进行数据操作
    # ...
```

### 手动获取用户的company_id

```python
from common.utils.jwt_utils import get_user_company_id

# 获取用户的company_id（返回第一个激活的企业）
company_id = get_user_company_id(user_id)
if not company_id:
    # 用户没有关联企业
    pass
```

## 环境变量

在 `docker-compose.yml` 或 `.env` 文件中配置：

```env
MONGODB_HOST=mongodb
MONGODB_PORT=27017
MONGODB_NAME=platform_db
MONGODB_USER=admin
MONGODB_PASSWORD=admin123
REDIS_HOST=redis
REDIS_PORT=6379
SECRET_KEY=your-secret-key
DEBUG=True
```

## 故障排查

### 服务无法启动

1. 检查Docker和Docker Compose是否正常运行
2. 查看服务日志：`docker-compose logs [service_name]`
3. 检查端口是否被占用
4. 检查MongoDB和Redis是否正常启动

### 数据库连接失败

1. 检查MongoDB服务是否运行
2. 验证连接配置（用户名、密码、主机、端口）
3. 检查网络连接（Docker网络）

### JWT Token无效

1. 检查Token是否过期
2. 验证Token格式是否正确
3. 检查JWT密钥配置
4. 确认Token中包含 `user_id`（不包含 `company_id`）

### company_id为None

1. 检查用户是否关联了企业（查询 `UserCompany` 表）
2. 确认企业状态为激活（`is_active=True`）且未删除（`is_deleted=False`）
3. 检查 `TenantMiddleware` 是否正确配置在 `settings.py` 中
4. 确认中间件顺序：`TenantMiddleware` 应该在认证中间件之前

## 前端开发

### 本地开发

```bash
cd frontend
npm install
npm start
```

前端开发服务器运行在 http://localhost:3000，API请求会自动代理到后端API网关（http://localhost:8000）。

### 构建生产版本

```bash
cd frontend
npm run build
```

构建产物在 `frontend/dist/` 目录。

### 已实现功能

- ✅ 用户登录注册页面
- ✅ 用户管理页面（列表、详情、编辑）
- ✅ 企业管理页面（列表、详情、加入/退出企业）
- ✅ 消息通知页面（列表、未读数量、标记已读）
- ✅ 日志查看页面（列表、筛选、统计）

## 架构说明

### 多租户数据隔离

- 所有数据操作都通过 `company_id` 进行隔离
- `TenantMiddleware` 自动从数据库读取用户的 `company_id`
- JWT Token 中只包含 `user_id`，`company_id` 实时从数据库获取
- 优势：用户切换企业时无需重新登录，`company_id` 始终是最新值

### JWT认证流程

1. 用户登录后，生成包含 `user_id` 的 JWT Token
2. 客户端在请求头中携带 Token：`Authorization: Bearer <token>`
3. `TenantMiddleware` 从 Token 提取 `user_id`
4. 从数据库的 `UserCompany` 表查询用户的 `company_id`
5. 将 `company_id` 和 `user_id` 注入到 `request` 对象
6. 视图函数通过 `request.company_id` 访问企业ID

## 待办事项

- [ ] 完善API文档
- [ ] 添加单元测试
- [ ] 性能优化
- [ ] 安全加固
- [ ] 前端权限控制完善
- [ ] WebSocket连接优化
- [ ] 支持用户切换企业功能

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系项目维护者。
