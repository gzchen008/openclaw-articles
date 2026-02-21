#!/bin/bash
# SearXNG 搜索命令行工具
# 用法: ./searxng.sh "搜索关键词" [结果数量]

SEARXNG_URL="${SEARXNG_URL:-http://localhost:1679}"
QUERY="$1"
LIMIT="${2:-10}"

# 检查服务是否运行
check_service() {
    if ! curl -s "${SEARXNG_URL}/status" > /dev/null 2>&1; then
        echo "❌ SearXNG 服务未运行"
        echo ""
        echo "启动服务:"
        echo "  cd /Users/cgz/.openclaw/workspace/tools/searxng"
        echo "  python3 searxng_server.py 1679 &"
        exit 1
    fi
}

# 显示帮助
show_help() {
    echo "🔍 SearXNG 本地搜索工具"
    echo ""
    echo "用法:"
    echo "  $0 \"搜索关键词\"       # 搜索并显示结果"
    echo "  $0 \"关键词\" 5        # 显示前5条结果"
    echo "  $0 --status            # 检查服务状态"
    echo "  $0 --stop              # 停止服务"
    echo "  $0 --help              # 显示帮助"
    echo ""
    echo "环境变量:"
    echo "  SEARXNG_URL=http://localhost:1679"
}

# 检查参数
case "$1" in
    --help|-h)
        show_help
        exit 0
        ;;
    --status)
        echo "🔍 检查 SearXNG 服务状态..."
        curl -s "${SEARXNG_URL}/status" | python3 -m json.tool 2>/dev/null || echo "❌ 服务未响应"
        exit 0
        ;;
    --stop)
        echo "⏹️  停止 SearXNG 服务..."
        pkill -f "searxng_server.py" 2>/dev/null && echo "✅ 服务已停止" || echo "⚠️  服务未运行"
        exit 0
        ;;
esac

if [ -z "$QUERY" ]; then
    show_help
    exit 1
fi

check_service

# URL 编码查询词
ENCODED_QUERY=$(printf '%s' "$QUERY" | python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.stdin.read()))')

echo "🔍 搜索: $QUERY"
echo "🌐 $SEARXNG_URL"
echo ""

# 调用 SearXNG API
curl -s "${SEARXNG_URL}/search?q=${ENCODED_QUERY}&format=json" | python3 << 'PYEOF'
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    print(f"📊 找到 {len(results)} 条结果\n")
    
    for i, r in enumerate(results[:'$LIMIT'], 1):
        title = r.get('title', '无标题')
        url = r.get('url', '')
        content = r.get('content', '无描述')[:120]
        engine = r.get('engine', '未知')
        print(f"{i}. {title}")
        print(f"   🔗 {url}")
        print(f"   📝 {content}...")
        print(f"   🔍 {engine}\n")
except Exception as e:
    print(f'❌ 错误: {e}')
    print('原始响应:')
    print(sys.stdin.read())
PYEOF
