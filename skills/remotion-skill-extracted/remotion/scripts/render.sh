#!/bin/bash
# OpenClaw Remotion Skill - 视频渲染脚本

set -e

COMPOSITION="${1:-}"
OUTPUT="${2:-output.mp4}"
QUALITY="${3:-high}"
FRAMES="${4:-}"

if [ -z "$COMPOSITION" ]; then
    echo "🎬 OpenClaw Remotion 渲染脚本"
    echo ""
    echo "用法:"
    echo "  render.sh <Composition> [输出文件] [质量] [帧范围]"
    echo ""
    echo "示例:"
    echo "  render.sh MyComposition video.mp4"
    echo "  render.sh MyComposition preview.mp4 low 0-150"
    echo ""
    echo "参数:"
    echo "  Composition    Remotion 组件名称"
    echo "  输出文件       默认: output.mp4"
    echo "  质量           high/medium/low (默认: high)"
    echo "  帧范围         如: 0-150 (可选)"
    echo ""
    
    # 列出可用的 Compositions
    if [ -f "src/index.ts" ]; then
        echo "可用的 Compositions:"
        grep -o 'id="[^"]*"' src/index.ts | sed 's/id="//;s/"/  - /'
    fi
    exit 1
fi

# 检查是否在 Remotion 项目目录
if [ ! -f "package.json" ] || ! grep -q "remotion" package.json 2>/dev/null; then
    echo "❌ 当前目录不是 Remotion 项目"
    echo "   请进入项目目录后运行"
    exit 1
fi

# 构建渲染参数
RENDER_ARGS=""

case "$QUALITY" in
    low)
        RENDER_ARGS="--jpeg-quality=50 --scale=0.5"
        echo "⚡ 快速预览模式 (低质量)"
        ;;
    medium)
        RENDER_ARGS="--jpeg-quality=80 --scale=0.75"
        echo "🎥 标准质量模式"
        ;;
    high)
        RENDER_ARGS="--jpeg-quality=100"
        echo "🎬 高质量模式"
        ;;
esac

if [ -n "$FRAMES" ]; then
    RENDER_ARGS="$RENDER_ARGS --frames=$FRAMES"
    echo "📍 帧范围: $FRAMES"
fi

echo ""
echo "🎬 开始渲染..."
echo "   Composition: $COMPOSITION"
echo "   输出文件: $OUTPUT"
echo ""

# 执行渲染
npx remotion render src/index.ts "$COMPOSITION" "$OUTPUT" $RENDER_ARGS

echo ""
echo "✅ 渲染完成!"
echo "   文件: $OUTPUT"

# 显示文件大小
if [ -f "$OUTPUT" ]; then
    SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo "   大小: $SIZE"
fi
