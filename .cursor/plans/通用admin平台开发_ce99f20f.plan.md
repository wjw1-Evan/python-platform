---
name: 通用Admin平台开发
overview: 开发一个基于Django+MongoDB+微服务架构的通用Admin平台，包含用户管理、多企业支持、消息通知、日志等完整功能模块，前后端分离，支持Docker部署。
todos:
  - id: setup-project
    content: 创建项目目录结构，克隆Django源码，配置Docker环境
    status: completed
  - id: data-factory
    content: 实现数据工厂：BaseModel基类和BaseCRUD统一接口
    status: completed
  - id: auth-service
    content: 开发认证服务：JWT Token生成验证、登录注册接口
    status: completed
  - id: user-service
    content: 开发用户服务：用户模型和CRUD操作
    status: completed
  - id: company-service
    content: 开发企业服务：企业模型、用户-企业多对多关系、自动创建企业
    status: completed
  - id: permission-service
    content: 开发权限服务：角色权限模型和验证中间件
    status: completed
  - id: notification-service
    content: 开发通知服务：通知模型、WebSocket实时推送
    status: completed
  - id: log-service
    content: 开发日志服务：日志模型、自动记录中间件
    status: completed
  - id: tenant-isolation
    content: 实现多租户数据隔离：中间件和查询过滤
    status: completed
  - id: api-gateway
    content: 实现API网关：统一路由和认证
    status: completed
  - id: frontend-setup
    content: 创建Ant Design Pro前端项目并配置API代理
    status: completed
  - id: frontend-features
    content: 实现前端功能：登录注册、用户管理、企业管理、通知、日志
    status: completed
  - id: cursor-rules
    content: 编写.cursorrules文件：项目规范和开发指南
    status: completed
  - id: documentation
    content: 编写README和API文档
    status: completed
---

# 通用Admin平台开发计划

## 项目架构

### 技术栈

- **后端**: Python 3.10+, Django (从GitHub克隆), Djongo (MongoDB集成)
- **数据库**: MongoDB
- **前端**: Ant Design Pro (使用 pro create platform 创建)
- **认证**: JWT Token
- **实时通信**: WebSocket (Django Channels)
- **容器化**: Docker + Docker Compose
- **微服务**: 6个服务（用户、企业、认证、权限、通知、日志）

### 目录结构

```
python-platform/
├── backend/                    # 后端服务
│   ├── common/                # 公共模块
│   │   ├── data_factory/      # 数据工厂
│   │   │   ├── base_model.py  # 模型基类
│   │   │   └── crud.py        # 统一CRUD接口
│   │   ├── middleware/        # 中间件
│   │   └── utils/             # 工具函数
│   ├── services/              # 微服务
│   │   ├── user_service/      # 用户服务
│   │   ├── company_service/   # 企业服务
│   │   ├── auth_service/      # 认证服务
│   │   ├── permission_service/# 权限服务
│   │   ├── notification_service/# 通知服务
│   │   └── log_service/       # 日志服务
│   ├── api_gateway/           # API网关
│   └── requirements.txt
├── frontend/                  # Ant Design Pro前端
├── docker/                    # Docker配置
│   ├── Dockerfile.backend
│   └── Dockerfile.frontend
├── docker-compose.yml
├── .cursorrules              # Cursor规则文件
└── README.md
```

## 实施步骤

### 阶段1: 项目基础搭建

1. **克隆Django源码**

   - 在backend目录下克隆Django仓库
   - 配置Django项目结构

2. **Docker环境配置**

   - 创建docker-compose.yml，包含MongoDB、Redis、各微服务
   - 编写各服务的Dockerfile
   - 配置网络和卷

3. **数据工厂实现**

   - `common/data_factory/base_model.py`: 创建BaseModel基类
     - 包含通用字段：id, created_at, updated_at, company_id (多租户)
     - 提供软删除支持
   - `common/data_factory/crud.py`: 实现统一CRUD操作
     - BaseCRUD类，提供create, read, update, delete, list等方法
     - 支持企业数据隔离过滤
     - 支持分页、排序、查询

### 阶段2: 核心服务开发

4. **认证服务 (auth_service)**

   - JWT Token生成和验证
   - 用户登录/注册接口
   - Token刷新机制
   - 文件: `auth_service/views.py`, `auth_service/serializers.py`

5. **用户服务 (user_service)**

   - 用户模型（继承BaseModel）
   - 用户CRUD操作（使用数据工厂）
   - 用户信息管理接口
   - 文件: `user_service/models.py`, `user_service/views.py`

6. **企业服务 (company_service)**

   - 企业模型（继承BaseModel）
   - 用户-企业多对多关系模型
   - 企业CRUD操作
   - 用户加入/退出企业接口
   - 注册用户时自动创建企业
   - 文件: `company_service/models.py`, `company_service/views.py`

7. **权限服务 (permission_service)**

   - 角色模型（继承BaseModel）
   - 权限模型（继承BaseModel）
   - 用户-角色-权限关联
   - 权限验证中间件
   - 文件: `permission_service/models.py`, `permission_service/middleware.py`

### 阶段3: 功能模块开发

8. **通知服务 (notification_service)**

   - 通知模型（继承BaseModel）
   - 通知CRUD操作
   - WebSocket连接管理（Django Channels）
   - 实时推送接口
   - 文件: `notification_service/models.py`, `notification_service/consumers.py`

9. **日志服务 (log_service)**

   - 日志模型（继承BaseModel）
   - 操作日志记录
   - 日志查询接口
   - 日志中间件（自动记录API请求）
   - 文件: `log_service/models.py`, `log_service/middleware.py`

10. **API网关**

    - 统一路由分发
    - 请求认证验证
    - 跨服务调用封装
    - 文件: `api_gateway/urls.py`, `api_gateway/views.py`

### 阶段4: 多租户数据隔离

11. **中间件实现**

    - 企业ID提取中间件（从JWT Token或请求头）
    - 自动过滤查询结果
    - 文件: `common/middleware/tenant_middleware.py`

12. **数据工厂增强**

    - 所有查询自动添加company_id过滤
    - 创建操作自动设置company_id
    - 更新BaseCRUD类

### 阶段5: 前端集成

13. **Ant Design Pro项目创建**

    - 使用 `pro create platform` 创建前端项目
    - 配置API代理指向后端网关

14. **前端功能实现**

    - 登录/注册页面
    - 用户管理页面
    - 企业管理页面
    - 消息通知组件
    - 日志查看页面
    - WebSocket连接管理

### 阶段6: 配置和文档

15. **环境配置**

    - 各服务的settings.py配置
    - MongoDB连接配置
    - Redis配置（WebSocket支持）
    - JWT密钥配置

16. **Cursor Rules编写**

    - 项目编码规范
    - 代码结构说明
    - 开发流程说明

17. **文档编写**

    - README.md项目说明
    - API文档
    - 部署文档

## 关键技术点

### 数据工厂基类设计

```python
# common/data_factory/base_model.py
class BaseModel(models.Model):
    id = models.ObjectIdField(primary_key=True)
    company_id = models.ObjectIdField()  # 多租户隔离
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True
```

### 统一CRUD接口

```python
# common/data_factory/crud.py
class BaseCRUD:
    def create(self, data, company_id)
    def get(self, id, company_id)
    def update(self, id, data, company_id)
    def delete(self, id, company_id)
    def list(self, filters, company_id, page, page_size)
```

### 多租户中间件

- 从JWT Token中提取company_id
- 自动注入到所有数据库查询
- 确保数据隔离

## 注意事项

1. **Djongo配置**: 需要在settings.py中正确配置Djongo作为数据库后端
2. **微服务通信**: 服务间通过HTTP API或消息队列通信
3. **WebSocket**: 使用Django Channels实现实时通知
4. **数据隔离**: 所有模型必须继承BaseModel，所有查询必须包含company_id过滤
5. **JWT Token**: 包含user_id和company_id信息
6. **Docker网络**: 各服务通过Docker网络名称通信