#!/bin/bash
# SearXNG Podman 管理脚本
# 用法: ./searxng-podman.sh [start|stop|restart|status|logs|update]

SEARXNG_DIR="$HOME/searxng-podman"
CONTAINER_NAME="searxng"
IMAGE="searxng/searxng:latest"
PORT="1679"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo "🔍 SearXNG Podman 管理脚本"
    echo ""
    echo "用法:"
    echo "  $0 start      # 启动服务"
    echo "  $0 stop       # 停止服务"
    echo "  $0 restart    # 重启服务"
    echo "  $0 status     # 查看状态"
    echo "  $0 logs       # 查看日志"
    echo "  $0 update     # 更新镜像"
    echo "  $0 shell      # 进入容器"
    echo "  $0 help       # 显示帮助"
    echo ""
    echo "访问地址:"
    echo "  Web: http://localhost:1679"
    echo "  API: http://localhost:1679/search?q=关键词\&format=json"
}

start_service() {
    echo -e "${BLUE}🚀 启动 SearXNG...${NC}"
    
    # 检查是否已运行
    if podman ps | grep -q $CONTAINER_NAME; then
        echo -e "${YELLOW}⚠️  SearXNG 已经在运行${NC}"
        echo -e "${GREEN}🌐 访问: http://localhost:1679${NC}"
        return 0
    fi
    
    # 创建目录
    mkdir -p $SEARXNG_DIR/searxng
    cd $SEARXNG_DIR
    
    # 生成密钥
    if [ ! -f "secret.key" ]; then
        openssl rand -hex 32 > secret.key
    fi
    SECRET_KEY=$(cat secret.key)
    
    # 检查镜像是否存在
    if ! podman images | grep -q searxng; then
        echo -e "${BLUE}📥 拉取镜像...${NC}"
        podman pull $IMAGE
    fi
    
    # 启动容器
    podman run -d \
        --name $CONTAINER_NAME \
        -e SEARXNG_BASE_URL=http://localhost:1679/ \
        -e SEARXNG_SECRET_KEY=$SECRET_KEY \
        -p 1679:1679 \
        -v "$SEARXNG_DIR/searxng:/etc/searxng:rw,Z" \
        --cap-drop ALL \
        --cap-add CHOWN \
        --cap-add SETGID \
        --cap-add SETUID \
        --restart unless-stopped \
        $IMAGE
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ SearXNG 启动成功!${NC}"
        echo ""
        echo -e "${GREEN}🌐 访问地址:${NC}"
        echo -e "   Web: ${BLUE}http://localhost:1679${NC}"
        echo -e "   API: ${BLUE}http://localhost:1679/search?q=关键词\&format=json${NC}"
        echo ""
        echo "等待服务就绪..."
        sleep 3
        
        # 测试服务
        if curl -s http://localhost:1679 > /dev/null 2>&1; then
            echo -e "${GREEN}✅ 服务已就绪!${NC}"
        else
            echo -e "${YELLOW}⏳ 服务启动中，请稍后访问...${NC}"
        fi
    else
        echo -e "${RED}❌ 启动失败${NC}"
        return 1
    fi
}

stop_service() {
    echo -e "${BLUE}⏹️  停止 SearXNG...${NC}"
    
    if ! podman ps | grep -q $CONTAINER_NAME; then
        echo -e "${YELLOW}⚠️  SearXNG 未在运行${NC}"
        return 0
    fi
    
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    echo -e "${GREEN}✅ 已停止${NC}"
}

restart_service() {
    stop_service
    sleep 2
    start_service
}

show_status() {
    echo -e "${BLUE}📊 SearXNG 状态${NC}"
    echo ""
    
    if podman ps | grep -q $CONTAINER_NAME; then
        echo -e "${GREEN}✅ 运行中${NC}"
        echo ""
        podman ps --filter name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        echo ""
        echo -e "🌐 访问地址:"
        echo -e "   ${BLUE}http://localhost:1679${NC}"
    else
        echo -e "${YELLOW}⏹️  未运行${NC}"
    fi
}

show_logs() {
    if podman ps -a | grep -q $CONTAINER_NAME; then
        podman logs -f $CONTAINER_NAME
    else
        echo -e "${RED}❌ 容器不存在${NC}"
    fi
}

update_image() {
    echo -e "${BLUE}📥 更新 SearXNG 镜像...${NC}"
    stop_service
    podman pull $IMAGE
    start_service
}

enter_shell() {
    if podman ps | grep -q $CONTAINER_NAME; then
        podman exec -it $CONTAINER_NAME /bin/sh
    else
        echo -e "${RED}❌ 容器未运行${NC}"
    fi
}

# 主逻辑
case "${1:-help}" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    update)
        update_image
        ;;
    shell)
        enter_shell
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ 未知命令: $1${NC}"
        show_help
        exit 1
        ;;
esac
