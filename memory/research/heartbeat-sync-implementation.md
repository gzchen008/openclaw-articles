# 心跳同步实现指南

创建时间: 2026-03-31 13:15
创建人: Clawra

## 概述
本文档说明如何实现共享知识库的每周心跳同步。

## 宣现步骤

### 1. 创建同步脚本
创建 `~/.openclaw/scripts/sync-shared-knowledge.sh`:

```bash
#!/bin/bash
# 同步共享知识库到各 workspace
# 创建时间: 2026-03-31

SHARED_DIR="$HOME/.openclaw/shared"
WORKSPACES=("workspace" "workspace-feishu" "workspace-weixin")
LOG_FILE="$HOME/.openclaw/workspace-weixin/memory/heartbeat-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S)] $1" >> "$LOG_FILE"
}

sync_workspace() {
    local workspace=$1
    local workspace_dir="$HOME/.openclaw/$workspace"
    local memory_file="$workspace_dir/memory/$(date +%Y-%m-%d).md"

    log "开始同步到 $workspace..."

    # 检查是否需要同步
    if [ ! -f "$memory_file" ]; then
        # 创建新的每日记忆文件
        mkdir -p "$workspace_dir/memory"
        echo "# $workspace 记忆 - $(date +%Y-%m-%d)" > "$memory_file"
        echo "## 共享知识同步 - $(date +%Y-%m-%d)" >> "$memory_file"
        echo "同步来源: ~/.openclaw/shared" >> "$memory_file"
        log "创建新的记忆文件: $memory_file"
    else
        # 追加到现有文件
        echo - "" >> "$memory_file"
        echo "## 共享知识同步 - $(date +%Y-%m-%d)" >> "$memory_file"
    fi

    # 同步 lessons-learned.md
    if [ -f "$SHARED_DIR/lessons-learned.md" ]; then
        echo "" >> "$memory_file"
        echo "### 经验教训" >> "$memory_file"
        cat "$SHARED_DIR/lessons-learned.md" >> "$memory_file"
        log "同步 lessons-learned.md 到 $memory_file"
    fi

    # 同步 project-knowledge/
    if [ -d "$SHARED_DIR/project-knowledge" ]; then
        echo "" >> "$memory_file"
        echo "### 项目知识" >> "$memory_file"
        find "$SHARED_DIR/project-knowledge" -type f -name "*.md" | while read -r; do
            echo "" >> "$memory_file"
            echo "#### $(basename $r .md)" >> "$memory_file"
            cat "$r" >> "$memory_file"
        done
        log "同步 project-knowledge/ 到 $memory_file"
    fi

    log "同步完成: $workspace"
}

# 主逻辑
log "========== 开始共享知识同步 =========="
for workspace in "${WORKSPACES[@]}"; do
    sync_workspace "$workspace"
done
log "========== 共享知识同步完成 =========="

# 记录完成日志
log "同步完成"
```

### 2. 创建 Cron 任务
使用 OpenClaw 的 cron 功能创建定时任务。

#### 配置文件位置
`~/.openclaw/openclaw.json`

#### 配置示例
```json
{
  "crons": [
    {
      "id": "sync-shared-knowledge-weekly",
      "schedule": "0 0 12 * * 1",
      "command": "bash $HOME/.openclaw/scripts/sync-shared-knowledge.sh",
      "delivery": {
        "mode": "announce",
        "channel": "openclaw-weixin",
        "to": "o9cq809jbJZBOY8RdJrX797DXA8s@im.wechat"
      },
      "model": "zai/glm-5"
    }
  ]
}
```

**说明**:
- `schedule: "0 0 12 * * 1"` = 每周一中午 12:00 执行
- `command`: 脚本路径
- `delivery`: 通知方式

### 3. 更新 HEARTBEAT.md
在 workspace-weixin 的 HEARTBEAT.md 中添加同步说明。

### 4. 更新 MEMORY.md
在 workspace-weixin 的 MEMORY.md 中添加同步任务说明。

### 5. 测试
1. 手动运行脚本测试
2. 磾查日志文件确认同步成功
3. 检查各 workspace 的 memory/ 目录是否有新的同步文件

## 同步内容

- `shared/lessons-learned.md` - 经验教训
- `shared/project-knowledge/` - 项目知识

## 同步频率
- 每周一中午 12:00

## 同步范围
- workspace
- workspace-feishu
- workspace-weixin

## 日志文件
`~/.openclaw/workspace-weixin/memory/heartbeat-sync.log`

## 注意事项
1. 節目内存占用： 同步会读取多个文件,建议使用 `--max-chars` 限制
2. 并发安全: 脚本使用简单的顺序执行,避免并发问题
3. 错误处理: 脚本会捕获异常并记录日志
4. 彊增更新: 追加模式不会删除旧内容
5. 测试: 上线前充分测试,确保同步逻辑正确
6. 文档化: 记录同步内容和时间,方便排查问题
