#!/bin/bash
# OpenClaw Remotion Skill - 项目初始化脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_NAME="${1:-my-video}"
TEMPLATE="${2:-}"

echo "🎬 OpenClaw Remotion 项目初始化"
echo "================================"

# 检查是否已存在
if [ -d "$PROJECT_NAME" ]; then
    echo "❌ 目录 $PROJECT_NAME 已存在"
    exit 1
fi

# 如果有指定模板
if [ "$TEMPLATE" = "--template" ] && [ -n "$3" ]; then
    TEMPLATE_NAME="$3"
    TEMPLATE_DIR="$SKILL_DIR/assets/$TEMPLATE_NAME"
    
    if [ ! -d "$TEMPLATE_DIR" ]; then
        echo "❌ 模板不存在: $TEMPLATE_NAME"
        echo "可用模板:"
        ls -1 "$SKILL_DIR/assets/" 2>/dev/null | sed 's/^/  - /'
        exit 1
    fi
    
    echo "📦 使用模板: $TEMPLATE_NAME"
    cp -r "$TEMPLATE_DIR" "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    
    # 如果模板有 package.json，安装依赖
    if [ -f "package.json" ]; then
        echo "📥 安装依赖..."
        npm install
    fi
    
    echo ""
    echo "✅ 项目创建成功!"
    echo ""
    echo "下一步:"
    echo "  cd $PROJECT_NAME"
    echo "  npm run dev    # 启动预览"
    echo "  npm run build  # 渲染视频"
    
else
    # 使用官方模板
    echo "📦 使用官方 Hello World 模板"
    npm init video@latest "$PROJECT_NAME"
    
    echo ""
    echo "✅ 项目创建成功!"
    echo ""
    echo "下一步:"
    echo "  cd $PROJECT_NAME"
    echo "  npm run dev    # 启动预览"
fi
