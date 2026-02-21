#!/bin/bash
# 移除 Claude Code 的 Co-Authored-By 签名
COMMIT_MSG_FILE=$1

# 使用 sed 移除 Co-Authored-By 行
sed -i '' '/^Co-Authored-By: Claude Opus/d' "$COMMIT_MSG_FILE"

exit 0
