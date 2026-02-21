#!/bin/bash
# SearXNG 搜索脚本 - 供 OpenClaw 调用
# 用法: ./search.sh "搜索关键词" [结果数量]

SEARXNG_URL="${SEARXNG_URL:-http://localhost:8080}"
QUERY="$1"
LIMIT="${2:-10}"

if [ -z "$QUERY" ]; then
    echo "用法: $0 \"搜索关键词\" [结果数量]"
    exit 1
fi

# URL 编码查询词
ENCODED_QUERY=$(printf '%s' "$QUERY" | python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.stdin.read()))')

# 调用 SearXNG API
curl -s "${SEARXNG_URL}/search?q=${ENCODED_QUERY}&format=json&language=zh-CN" | \
python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', [])
    print(f\"🔍 搜索: {data.get('query', '')}\")
    print(f\"📊 找到 {len(results)} 条结果\\n\")
    
    for i, r in enumerate(results[:$LIMIT], 1):
        title = r.get('title', '无标题')
        url = r.get('url', '')
        content = r.get('content', '无描述')[:150]
        engine = r.get('engine', '未知')
        print(f\"{i}. {title}\")
        print(f\"   🔗 {url}\")
        print(f\"   📝 {content}...\")
        print(f\"   🔍 来源: {engine}\\n\")
except Exception as e:
    print(f'错误: {e}')
    print('原始响应:')
    print(sys.stdin.read())
"
