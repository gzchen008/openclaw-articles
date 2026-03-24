#!/bin/bash

# WeAuto 自动完善脚本
# 每 2 小时执行一次，完善一个待办项

set -e

PROJECT_DIR="$HOME/wbproject/weauto/weauto-server"
TASKS_FILE="$HOME/.openclaw/workspace/memory/weauto-tasks.md"
NOTIFY_CHAT="oc_684c4d31eb3fbc2a03978be4034ad0e7"

echo "========================================="
echo "WeAuto 自动完善任务"
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================="

# 进入项目目录
cd "$PROJECT_DIR"

# 运行 Claude Code 完善任务
claude --permission-mode bypassPermissions --print "
请完成以下任务：

1. 读取 $TASKS_FILE 查看当前待办项列表
2. 选择第一个状态为 '⏳ 待开始' 的任务
3. 实现该任务（修改代码、添加测试等）
4. 更新 $TASKS_FILE 将该任务标记为 ✅ 已完成
5. 生成变更摘要

要求：
- 每次只完成一个任务
- 确保代码编译通过
- 添加必要的注释
- 更新任务清单文件
"

# 发送通知到飞书群
openclaw message send \
  --channel feishu \
  --target "chat:$NOTIFY_CHAT" \
  --message "✅ WeAuto 自动完善任务已完成

$(cat $PROJECT_DIR/.last-task-summary 2>/dev/null || echo '查看任务清单了解详情')

查看完整清单: $TASKS_FILE"

echo "========================================="
echo "任务执行完成"
echo "========================================="
