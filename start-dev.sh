#!/bin/bash

# 本地开发环境启动脚本

set -e

echo "🚀 启动本地开发环境..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 启动基础服务（MongoDB和Redis）
echo -e "${YELLOW}📦 启动基础服务（MongoDB和Redis）...${NC}"
docker-compose up -d mongodb redis

# 等待服务就绪
echo "⏳ 等待MongoDB和Redis启动..."
sleep 3

# 2. 检查Python版本
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo -e "${YELLOW}⚠️  警告: Python版本 $PYTHON_VERSION 可能不兼容，建议使用 Python 3.10-3.12${NC}"
fi

# 3. 检查Python虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 创建Python虚拟环境...${NC}"
    python3 -m venv venv
fi

# 激活虚拟环境
echo -e "${YELLOW}🔧 激活虚拟环境...${NC}"
source venv/bin/activate

# 4. 安装依赖
echo -e "${YELLOW}📥 安装Python依赖...${NC}"
cd backend
pip install -q --upgrade pip setuptools wheel

# 安装所有依赖
echo "  - 安装项目依赖..."
pip install -q -r requirements.txt

cd ..

# 4. 设置环境变量
export DEPLOYMENT_MODE=development
export MONGODB_HOST=localhost
export MONGODB_PORT=27017
export MONGODB_NAME=platform_db
export MONGODB_USER=admin
export MONGODB_PASSWORD=admin123
export REDIS_HOST=localhost
export REDIS_PORT=6379
export SECRET_KEY=dev-secret-key-change-in-production
export DEBUG=True

# 5. 启动后端服务（在后台）
echo -e "${GREEN}🔧 启动后端服务...${NC}"

# API网关 (8000)
echo "  - 启动API网关 (端口: 8000)"
cd backend/api_gateway
python manage.py runserver 0.0.0.0:8000 > /tmp/api_gateway.log 2>&1 &
API_GATEWAY_PID=$!
cd ../..

# 用户服务 (8001)
echo "  - 启动用户服务 (端口: 8001)"
cd backend/services/user_service
python manage.py runserver 0.0.0.0:8001 > /tmp/user_service.log 2>&1 &
USER_SERVICE_PID=$!
cd ../../..

# 企业服务 (8002)
echo "  - 启动企业服务 (端口: 8002)"
cd backend/services/company_service
python manage.py runserver 0.0.0.0:8002 > /tmp/company_service.log 2>&1 &
COMPANY_SERVICE_PID=$!
cd ../../..

# 认证服务 (8003)
echo "  - 启动认证服务 (端口: 8003)"
cd backend/services/auth_service
MONGODB_HOST=localhost MONGODB_PORT=27017 MONGODB_NAME=platform_db MONGODB_USER=admin MONGODB_PASSWORD=admin123 REDIS_HOST=localhost REDIS_PORT=6379 SECRET_KEY=dev-secret-key-change-in-production DEBUG=True DEPLOYMENT_MODE=development python manage.py runserver 0.0.0.0:8003 > /tmp/auth_service.log 2>&1 &
AUTH_SERVICE_PID=$!
cd ../../..

# 权限服务 (8004)
echo "  - 启动权限服务 (端口: 8004)"
cd backend/services/permission_service
python manage.py runserver 0.0.0.0:8004 > /tmp/permission_service.log 2>&1 &
PERMISSION_SERVICE_PID=$!
cd ../../..

# 通知服务 (8005)
echo "  - 启动通知服务 (端口: 8005)"
cd backend/services/notification_service
python manage.py runserver 0.0.0.0:8005 > /tmp/notification_service.log 2>&1 &
NOTIFICATION_SERVICE_PID=$!
cd ../../..

# 日志服务 (8006)
echo "  - 启动日志服务 (端口: 8006)"
cd backend/services/log_service
python manage.py runserver 0.0.0.0:8006 > /tmp/log_service.log 2>&1 &
LOG_SERVICE_PID=$!
cd ../../..

# 等待服务启动
echo "⏳ 等待后端服务启动..."
sleep 5

# 6. 启动前端服务
echo -e "${GREEN}🎨 启动前端服务...${NC}"
cd frontend

# 检查node_modules
if [ ! -d "node_modules" ]; then
    echo "  - 安装前端依赖..."
    npm install
fi

echo "  - 启动前端开发服务器 (端口: 3000)"
PORT=3000 npm run start:dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# 保存PID到文件
echo $API_GATEWAY_PID > /tmp/api_gateway.pid
echo $USER_SERVICE_PID > /tmp/user_service.pid
echo $COMPANY_SERVICE_PID > /tmp/company_service.pid
echo $AUTH_SERVICE_PID > /tmp/auth_service.pid
echo $PERMISSION_SERVICE_PID > /tmp/permission_service.pid
echo $NOTIFICATION_SERVICE_PID > /tmp/notification_service.pid
echo $LOG_SERVICE_PID > /tmp/log_service.pid
echo $FRONTEND_PID > /tmp/frontend.pid

echo ""
echo -e "${GREEN}✅ 所有服务已启动！${NC}"
echo ""
echo "📋 服务地址："
echo "  - API网关:     http://localhost:8000"
echo "  - 用户服务:    http://localhost:8001"
echo "  - 企业服务:    http://localhost:8002"
echo "  - 认证服务:    http://localhost:8003"
echo "  - 权限服务:    http://localhost:8004"
echo "  - 通知服务:    http://localhost:8005"
echo "  - 日志服务:    http://localhost:8006"
echo "  - 前端:        http://localhost:3000 (开发模式，代理API到8000)"
echo ""
echo "📝 日志文件："
echo "  - API网关:     /tmp/api_gateway.log"
echo "  - 用户服务:    /tmp/user_service.log"
echo "  - 企业服务:    /tmp/company_service.log"
echo "  - 认证服务:    /tmp/auth_service.log"
echo "  - 权限服务:    /tmp/permission_service.log"
echo "  - 通知服务:    /tmp/notification_service.log"
echo "  - 日志服务:    /tmp/log_service.log"
echo "  - 前端:        /tmp/frontend.log"
echo ""
echo "🛑 停止服务：运行 ./stop-dev.sh"
echo ""
