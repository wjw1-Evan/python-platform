# 本地开发启动指南

## 快速启动（推荐）

使用提供的启动脚本：

```bash
# 启动所有服务
./start-dev.sh

# 停止所有服务
./stop-dev.sh
```

## 手动启动步骤

### 1. 启动基础服务（MongoDB和Redis）

```bash
docker-compose up -d mongodb redis
```

### 2. 设置Python环境

```bash
# 创建虚拟环境（如果还没有）
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
cd backend
pip install -r requirements.txt
cd ..
```

### 3. 设置环境变量

```bash
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_NAME=platform_db
export MONGODB_USER=admin
export MONGODB_PASSWORD=admin123
export REDIS_HOST=localhost
export REDIS_PORT=6379
export SECRET_KEY=dev-secret-key-change-in-production
export DEBUG=True
```

### 4. 启动后端服务

每个服务需要在单独的终端窗口中启动：

```bash
# 终端1: API网关 (8000)
cd backend/api_gateway
python manage.py runserver 0.0.0.0:8000

# 终端2: 用户服务 (8001)
cd backend/services/user_service
python manage.py runserver 0.0.0.0:8001

# 终端3: 企业服务 (8002)
cd backend/services/company_service
python manage.py runserver 0.0.0.0:8002

# 终端4: 认证服务 (8003)
cd backend/services/auth_service
python manage.py runserver 0.0.0.0:8003

# 终端5: 权限服务 (8004)
cd backend/services/permission_service
python manage.py runserver 0.0.0.0:8004

# 终端6: 通知服务 (8005)
cd backend/services/notification_service
python manage.py runserver 0.0.0.0:8005

# 终端7: 日志服务 (8006)
cd backend/services/log_service
python manage.py runserver 0.0.0.0:8006
```

### 5. 启动前端服务

```bash
cd frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run start:dev
```

## 服务地址

- **API网关**: http://localhost:8000
- **用户服务**: http://localhost:8001
- **企业服务**: http://localhost:8002
- **认证服务**: http://localhost:8003
- **权限服务**: http://localhost:8004
- **通知服务**: http://localhost:8005
- **日志服务**: http://localhost:8006
- **前端**: http://localhost:8000 (开发模式，通过代理访问后端)

## 常见问题

### 端口被占用

如果端口被占用，可以：

1. 停止占用端口的进程
2. 或者修改服务的端口配置

### 数据库连接失败

1. 确保MongoDB和Redis正在运行：`docker-compose ps`
2. 检查环境变量是否正确设置
3. 验证MongoDB连接：`mongosh mongodb://admin:admin123@localhost:27017`

### 依赖安装失败

1. 确保Python版本 >= 3.10
2. 升级pip：`pip install --upgrade pip`
3. 使用国内镜像（如果需要）：`pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`
