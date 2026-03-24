#!/bin/bash
# OpenClaw 更新追踪脚本
# 每天检查版本更新并生成公众号文章

WORKSPACE="/Users/cgz/.openclaw/workspace"
STATE_FILE="$WORKSPACE/tools/openclaw-changelog/state.json"
OUTPUT_DIR="$WORKSPACE/articles/openclaw-updates"

# 创建目录
mkdir -p "$OUTPUT_DIR"
mkdir -p "$(dirname "$STATE_FILE")"

# 获取当前安装版本
CURRENT_VERSION=$(openclaw --version 2>/dev/null || echo "unknown")

# 获取 GitHub 最新 release 信息
GITHUB_API="https://api.github.com/repos/openclaw/openclaw/releases/latest"
RELEASE_INFO=$(curl -s "$GITHUB_API" 2>/dev/null)

# 解析 JSON
LATEST_VERSION=$(echo "$RELEASE_INFO" | jq -r '.tag_name // .name // "unknown"' 2>/dev/null)
RELEASE_DATE=$(echo "$RELEASE_INFO" | jq -r '.published_at // "unknown"' 2>/dev/null)
RELEASE_BODY=$(echo "$RELEASE_INFO" | jq -r '.body // ""' 2>/dev/null)
RELEASE_URL=$(echo "$RELEASE_INFO" | jq -r '.html_url // "https://github.com/openclaw/openclaw/releases"' 2>/dev/null)

# 处理日期格式
if [ "$RELEASE_DATE" != "unknown" ]; then
    RELEASE_DATE_FORMATTED=$(date -j -f "%Y-%m-%dT%H:%M:%SZ" "$RELEASE_DATE" "+%Y-%m-%d" 2>/dev/null || echo "$RELEASE_DATE")
else
    RELEASE_DATE_FORMATTED=$(date "+%Y-%m-%d")
fi

# 读取上次记录的版本
if [ -f "$STATE_FILE" ]; then
    LAST_VERSION=$(jq -r '.last_version // "unknown"' "$STATE_FILE" 2>/dev/null)
else
    LAST_VERSION="unknown"
    echo '{"last_version": "unknown", "last_check": ""}' > "$STATE_FILE"
fi

# 更新状态文件
TODAY=$(date "+%Y-%m-%d")
jq --arg version "$LATEST_VERSION" --arg date "$TODAY" \
    '.last_version = $version | .last_check = $date' "$STATE_FILE" > "${STATE_FILE}.tmp" && mv "${STATE_FILE}.tmp" "$STATE_FILE"

# 输出 JSON 供后续处理
cat <<EOF
{
  "current_installed": "$CURRENT_VERSION",
  "latest_version": "$LATEST_VERSION",
  "release_date": "$RELEASE_DATE_FORMATTED",
  "release_url": "$RELEASE_URL",
  "last_version": "$LAST_VERSION",
  "has_update": $([ "$LATEST_VERSION" != "$LAST_VERSION" ] && echo "true" || echo "false"),
  "changelog": $(echo "$RELEASE_BODY" | jq -Rs .)
}
EOF
