#!/bin/bash
# SearXNG 快速安装脚本

SEARXNG_DIR="$HOME/searxng"
echo "🚀 开始安装 SearXNG..."

# 创建目录
mkdir -p $SEARXNG_DIR
cd $SEARXNG_DIR

# 创建 docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.7'

services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "1679:1679"
    volumes:
      - ./searxng:/etc/searxng
    environment:
      - SEARXNG_BASE_URL=http://localhost:1679/
      - SEARXNG_SECRET_KEY=${SEARXNG_SECRET_KEY:-$(openssl rand -hex 32)}
    restart: unless-stopped
    cap_drop:
      - ALL
    cap_add:
      - CHOWN
      - SETGID
      - SETUID
    logging:
      driver: "json-file"
      options:
        max-size: "1m"
        max-file: "1"
EOF

echo "✅ docker-compose.yml 已创建"

# 创建配置文件目录
mkdir -p searxng

# 下载默认配置
docker pull searxng/searxng:latest
docker run --rm -v "$PWD/searxng:/etc/searxng" searxng/searxng:latest cp /usr/local/searxng/searx/settings.yml /etc/searxng/

echo "✅ 默认配置已下载"
echo ""
echo "📁 安装目录: $SEARXNG_DIR"
echo "🌐 访问地址: http://localhost:1679"
echo ""
echo "启动命令:"
echo "  cd $SEARXNG_DIR && docker-compose up -d"
echo ""
echo "停止命令:"
echo "  cd $SEARXNG_DIR && docker-compose down"
