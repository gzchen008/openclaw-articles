#!/bin/bash
# SearXNG Podman 部署脚本
# 兼容 Podman (无需 Docker Daemon)

SEARXNG_DIR="$HOME/searxng-podman"
echo "🚀 开始安装 SearXNG (Podman 版本)..."

# 创建目录
mkdir -p $SEARXNG_DIR
cd $SEARXNG_DIR

# 创建配置文件目录
mkdir -p searxng

# 复制配置文件（如果存在）
if [ -f "/Users/cgz/.openclaw/workspace/tools/searxng/settings.yml" ]; then
    cp /Users/cgz/.openclaw/workspace/tools/searxng/settings.yml searxng/
    echo "✅ 配置文件已复制"
fi

echo ""
echo "📁 安装目录: $SEARXNG_DIR"
echo ""
echo "启动命令:"
echo "  cd $SEARXNG_DIR && ./start.sh"
echo ""
echo "停止命令:"
echo "  cd $SEARXNG_DIR && ./stop.sh"
