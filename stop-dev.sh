#!/bin/bash

# 停止本地开发环境脚本

echo "🛑 停止本地开发环境..."

# 停止后端服务
if [ -f /tmp/api_gateway.pid ]; then
    kill $(cat /tmp/api_gateway.pid) 2>/dev/null || true
    rm /tmp/api_gateway.pid
    echo "  ✓ 已停止API网关"
fi

if [ -f /tmp/user_service.pid ]; then
    kill $(cat /tmp/user_service.pid) 2>/dev/null || true
    rm /tmp/user_service.pid
    echo "  ✓ 已停止用户服务"
fi

if [ -f /tmp/company_service.pid ]; then
    kill $(cat /tmp/company_service.pid) 2>/dev/null || true
    rm /tmp/company_service.pid
    echo "  ✓ 已停止企业服务"
fi

if [ -f /tmp/auth_service.pid ]; then
    kill $(cat /tmp/auth_service.pid) 2>/dev/null || true
    rm /tmp/auth_service.pid
    echo "  ✓ 已停止认证服务"
fi

if [ -f /tmp/permission_service.pid ]; then
    kill $(cat /tmp/permission_service.pid) 2>/dev/null || true
    rm /tmp/permission_service.pid
    echo "  ✓ 已停止权限服务"
fi

if [ -f /tmp/notification_service.pid ]; then
    kill $(cat /tmp/notification_service.pid) 2>/dev/null || true
    rm /tmp/notification_service.pid
    echo "  ✓ 已停止通知服务"
fi

if [ -f /tmp/log_service.pid ]; then
    kill $(cat /tmp/log_service.pid) 2>/dev/null || true
    rm /tmp/log_service.pid
    echo "  ✓ 已停止日志服务"
fi

if [ -f /tmp/frontend.pid ]; then
    kill $(cat /tmp/frontend.pid) 2>/dev/null || true
    rm /tmp/frontend.pid
    echo "  ✓ 已停止前端服务"
fi

# 停止Docker服务（可选）
read -p "是否停止MongoDB和Redis? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose stop mongodb redis
    echo "  ✓ 已停止MongoDB和Redis"
fi

echo "✅ 所有服务已停止"
