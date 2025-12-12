#!/bin/bash

# 启动脚本

echo "启动Admin平台服务..."

# 检查Docker是否运行
if ! docker info > /dev/null 2>&1; then
    echo "错误: Docker未运行，请先启动Docker"
    exit 1
fi

# 启动服务
echo "启动Docker Compose服务..."
docker-compose up -d

# 等待服务启动
echo "等待服务启动..."
sleep 10

# 初始化数据库
echo "初始化数据库..."
docker-compose exec -T backend python scripts/init_db.py

echo "服务启动完成！"
echo "后端API: http://localhost:8000/api/"
echo "前端界面: http://localhost:3000"
echo ""
echo "查看日志: docker-compose logs -f"
echo "停止服务: docker-compose down"
