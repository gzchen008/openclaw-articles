#!/bin/bash
# SearXNG Podman 启动脚本

SEARXNG_DIR="$HOME/searxng-podman"
cd $SEARXNG_DIR

echo "🚀 启动 SearXNG (Podman)..."

# 检查是否已运行
if podman ps | grep -q searxng; then
    echo "⚠️  SearXNG 已经在运行"
    echo "🌐 访问: http://localhost:1679"
    exit 0
fi

# 生成随机密钥
SECRET_KEY=$(openssl rand -hex 32)

# 启动容器
podman run -d \
    --name searxng \
    --label io.podman.compose.config-hash=123 \
    --label io.podman.compose.project=searxng \
    --label io.podman.compose.version=0.0.1 \
    --label podman.compose.container-number=1 \
    --label io.podman.compose.service=searxng \
    -e SEARXNG_BASE_URL=http://localhost:1679/ \
    -e SEARXNG_SECRET_KEY=$SECRET_KEY \
    -p 1679:1679 \
    -v "$SEARXNG_DIR/searxng:/etc/searxng:rw,Z" \
    --cap-drop ALL \
    --cap-add CHOWN \
    --cap-add SETGID \
    --cap-add SETUID \
    --log-driver json-file \
    --log-opt max-size=1m \
    --log-opt max-file=1 \
    --restart unless-stopped \
    searxng/searxng:latest

if [ $? -eq 0 ]; then
    echo "✅ SearXNG 启动成功!"
    echo ""
    echo "🌐 访问地址:"
    echo "   Web 界面: http://localhost:1679"
    echo "   API:      http://localhost:1679/search?q=关键词\&format=json"
    echo ""
    echo "📊 查看日志:"
    echo "   podman logs -f searxng"
    echo ""
    echo "⏹️  停止服务:"
    echo "   ./stop.sh"
else
    echo "❌ 启动失败"
    exit 1
fi
