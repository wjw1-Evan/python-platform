#!/bin/bash

# 前端项目创建脚本

echo "开始创建 Ant Design Pro 前端项目..."

# 检查是否已安装 pro-cli
if ! command -v pro &> /dev/null; then
    echo "正在安装 @ant-design/pro-cli..."
    npm install -g @ant-design/pro-cli
fi

# 进入 frontend 目录
cd "$(dirname "$0")"

# 检查是否已存在 platform 目录
if [ -d "platform" ]; then
    echo "platform 目录已存在，是否删除并重新创建？(y/n)"
    read -r response
    if [ "$response" = "y" ]; then
        rm -rf platform
    else
        echo "取消创建"
        exit 0
    fi
fi

# 创建项目
echo "正在创建项目..."
pro create platform <<EOF
umi
TypeScript
npm
EOF

# 进入项目目录
cd platform

# 安装依赖
echo "正在安装依赖..."
npm install

echo "项目创建完成！"
echo "请按照 SETUP.md 中的说明进行配置。"
echo "然后运行 'npm start' 启动开发服务器。"
