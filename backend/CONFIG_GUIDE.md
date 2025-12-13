# 配置管理指南

## 概述

项目支持两种运行模式：
- **开发模式**：使用 `start-dev.sh` 启动，服务运行在本地不同端口
- **生产模式**：使用 `docker-compose` 部署，服务运行在 Docker 容器中

配置系统会根据运行环境自动选择正确的服务URL。

## 环境变量

### DEPLOYMENT_MODE

用于明确指定部署模式：

- `development` / `dev` / `local`：开发模式
- `production` / `docker` / `prod`：生产模式

如果未设置，系统会自动检测：
- 如果 `MONGODB_HOST=mongodb`（Docker服务名），则认为是生产模式
- 如果存在 `/.dockerenv` 文件，则认为是生产模式
- 否则认为是开发模式

### 服务URL环境变量

可以通过以下环境变量显式设置服务URL（优先级最高）：

- `API_GATEWAY_URL`
- `USER_SERVICE_URL`
- `COMPANY_SERVICE_URL`
- `AUTH_SERVICE_URL`
- `PERMISSION_SERVICE_URL`
- `NOTIFICATION_SERVICE_URL`
- `LOG_SERVICE_URL`

## 配置优先级

1. **环境变量显式设置**（最高优先级）
   - 如果设置了 `AUTH_SERVICE_URL`，则使用该值
   
2. **自动环境检测**
   - 开发模式：`http://localhost:8003`（认证服务）
   - 生产模式：`http://auth_service:8000`（Docker服务名）

## 服务端口映射

### 开发模式（本地）

| 服务 | 端口 |
|------|------|
| API网关 | 8000 |
| 用户服务 | 8001 |
| 企业服务 | 8002 |
| 认证服务 | 8003 |
| 权限服务 | 8004 |
| 通知服务 | 8005 |
| 日志服务 | 8006 |

### 生产模式（Docker）

所有服务在容器内都运行在 8000 端口，通过 Docker 网络的服务名称访问。

## 使用方式

### 在 settings.py 中使用

```python
from common.utils.service_config import get_service_url, get_all_service_urls

# 获取单个服务URL
auth_service_url = get_service_url('auth_service')

# 获取所有服务URL
SERVICE_URLS = get_all_service_urls()
```

### 在代码中使用

```python
from django.conf import settings

# 使用配置的服务URL
user_service_url = settings.SERVICE_URLS['user_service']
```

## 启动脚本

### 开发模式

```bash
./start-dev.sh
```

自动设置：
- `DEPLOYMENT_MODE=development`
- `MONGODB_HOST=localhost`
- 其他开发环境变量

### 生产模式

```bash
docker-compose up -d
```

自动设置：
- `DEPLOYMENT_MODE=production`
- `MONGODB_HOST=mongodb`
- 其他生产环境变量

## 注意事项

1. **不要硬编码服务URL**：始终使用 `get_service_url()` 或 `SERVICE_URLS` 配置
2. **环境变量优先级最高**：如果需要覆盖默认配置，设置相应的环境变量
3. **开发模式**：确保所有服务都在运行，且端口未被占用
4. **生产模式**：确保 Docker 网络配置正确，服务名称可解析
