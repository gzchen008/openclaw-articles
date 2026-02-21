#!/bin/bash
# SearXNG Podman 停止脚本

echo "⏹️  停止 SearXNG..."

# 停止容器
podman stop searxng 2>/dev/null

# 删除容器
podman rm searxng 2>/dev/null

echo "✅ SearXNG 已停止"
