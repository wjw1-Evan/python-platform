#!/bin/bash

# Django源码克隆脚本
# 如果直接克隆GitHub失败，可以尝试以下镜像源

cd "$(dirname "$0")"

echo "正在克隆Django源码..."

# 方法1: 从GitHub克隆（官方源）
if git clone --depth 1 https://github.com/django/django.git django 2>/dev/null; then
    echo "✓ 成功从GitHub克隆Django源码"
    exit 0
fi

# 方法2: 从Gitee镜像克隆（如果GitHub失败）
if git clone --depth 1 https://gitee.com/mirrors/django.git django 2>/dev/null; then
    echo "✓ 成功从Gitee镜像克隆Django源码"
    # 添加GitHub作为远程仓库以便后续更新
    cd django && git remote set-url --add origin https://github.com/django/django.git
    exit 0
fi

# 方法3: 使用SSH协议（如果配置了SSH密钥）
if git clone --depth 1 git@github.com:django/django.git django 2>/dev/null; then
    echo "✓ 成功从GitHub（SSH）克隆Django源码"
    exit 0
fi

echo "✗ 所有克隆方法都失败了，请检查网络连接"
echo "您也可以手动下载Django源码并解压到backend/django目录"
exit 1
