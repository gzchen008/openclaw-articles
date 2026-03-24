#!/bin/bash
# OpenClaw 版本检查脚本
# 每天检查 OpenClaw 新版本，如果有新版本就自动写公众号文章并上传草稿

set -e

WORKSPACE="$HOME/.openclaw/workspace"
VERSION_FILE="$WORKSPACE/articles/.openclaw-versions.json"
LOG_FILE="$WORKSPACE/logs/openclaw-version-check.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "开始检查 OpenClaw 新版本..."

# 检查 gh CLI 是否可用
if ! command -v gh &> /dev/null; then
    log "错误: gh CLI 未安装"
    exit 1
fi

# 获取最新版本
LATEST_VERSION=$(gh release list --repo openclaw/openclaw --limit 1 --json tagName --jq '.[0].tagName' 2>/dev/null || echo "")

if [ -z "$LATEST_VERSION" ]; then
    log "错误: 无法获取最新版本信息"
    exit 1
fi

log "最新版本: $LATEST_VERSION"

# 读取已写过的版本
if [ ! -f "$VERSION_FILE" ]; then
    log "版本记录文件不存在，创建新文件"
    echo '{"lastChecked": "", "writtenVersions": [], "latestVersion": ""}' > "$VERSION_FILE"
fi

WRITTEN_VERSIONS=$(cat "$VERSION_FILE" | jq -r '.writtenVersions[]' 2>/dev/null || echo "")

# 检查是否已写过
if echo "$WRITTEN_VERSIONS" | grep -q "$LATEST_VERSION"; then
    log "版本 $LATEST_VERSION 已写过，跳过"
    
    # 更新检查时间
    cat "$VERSION_FILE" | jq --arg date "$(date -Iseconds)" '.lastChecked = $date' > "${VERSION_FILE}.tmp" && mv "${VERSION_FILE}.tmp" "$VERSION_FILE"
    exit 0
fi

log "发现新版本: $LATEST_VERSION，开始生成文章..."

# 获取版本信息
RELEASE_INFO=$(gh release view "$LATEST_VERSION" --repo openclaw/openclaw --json body,name,publishedAt 2>/dev/null || echo "")

if [ -z "$RELEASE_INFO" ]; then
    log "错误: 无法获取版本详情"
    exit 1
fi

# 提取版本号（去掉 v 前缀）
VERSION_NUMBER=$(echo "$LATEST_VERSION" | sed 's/^v//')
DATE_TODAY=$(date '+%Y-%m-%d')

# 调用 OpenClaw 生成文章
log "调用 OpenClaw 生成文章..."

# 使用 sessions_spawn 调用 subagent 生成文章
# 这里我们需要通过 OpenClaw 的 session 来执行，所以直接调用 Python 脚本
cd "$WORKSPACE"

# 调用 Python 脚本生成文章并上传
/usr/bin/python3 "$WORKSPACE/skills/wechat-mp-publish/scripts/generate_openclaw_article.py" \
    --version "$LATEST_VERSION" \
    --date "$DATE_TODAY" \
    --release-info "$RELEASE_INFO" \
    2>&1 | tee -a "$LOG_FILE"

if [ $? -eq 0 ]; then
    log "文章生成并上传成功"
    
    # 更新版本记录
    cat "$VERSION_FILE" | \
        jq --arg date "$(date -Iseconds)" \
           --arg version "$LATEST_VERSION" \
           '.lastChecked = $date | .writtenVersions += [$version] | .latestVersion = $version' \
        > "${VERSION_FILE}.tmp" && mv "${VERSION_FILE}.tmp" "$VERSION_FILE"
    
    log "版本记录已更新: $LATEST_VERSION"
else
    log "错误: 文章生成或上传失败"
    exit 1
fi

log "OpenClaw 版本检查完成"
