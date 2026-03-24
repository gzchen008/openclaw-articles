#!/bin/bash
# OpenClaw 每日更新检查
# 每天早上 8:00 执行

set -e

WORKSPACE="/Users/cgz/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/tools/openclaw-changelog"
LOG_FILE="$SCRIPT_DIR/check.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "===== Starting OpenClaw update check ====="

# 1. 获取最新版本信息
log "Fetching latest version..."
cd "$SCRIPT_DIR"
./track.sh > /tmp/openclaw-update.json 2>> "$LOG_FILE"

# 2. 生成公众号文章（如果有新版本）
log "Checking for updates..."
if [ -f /tmp/openclaw-update.json ]; then
    # 检查是否有新版本
    HAS_UPDATE=$(cat /tmp/openclaw-update.json | jq -r '.has_update // false')
    
    if [ "$HAS_UPDATE" = "true" ]; then
        log "New version detected! Generating article..."
        python3 generate-article.py /tmp/openclaw-update.json >> "$LOG_FILE" 2>&1
        
        ARTICLE_PATH=$(ls -t "$WORKSPACE/articles/openclaw-updates/"*.md 2>/dev/null | head -1)
        
        if [ -f "$ARTICLE_PATH" ]; then
            log "Article generated: $ARTICLE_PATH"
            
            # 发送飞书通知（可选）
            # 可以在这里添加自动发布到公众号的逻辑
        fi
    else
        log "No new version available."
    fi
else
    log "Failed to fetch version info."
fi

log "===== Update check completed ====="

echo "OpenClaw update check completed. See $LOG_FILE for details."
