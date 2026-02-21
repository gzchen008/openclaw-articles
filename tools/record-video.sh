#!/bin/bash

# 录制 ASCII 旋转动画视频
# 使用 ffmpeg 录制终端

OUTPUT_FILE="${1:-ascii-rotate.mp4}"
DURATION="${2:-5}"

# 获取终端窗口 ID
TERMINAL_WINDOW=$(osascript -e 'tell application "Terminal" to id of front window' 2>/dev/null || echo "")

if [ -z "$TERMINAL_WINDOW" ]; then
    echo "❌ 无法获取终端窗口"
    echo "请确保 Terminal.app 正在运行"
    exit 1
fi

echo "🎬 开始录制 ASCII 旋转动画..."
echo "📁 输出文件: $OUTPUT_FILE"
echo "⏱️  录制时长: ${DURATION}秒"
echo ""
echo "⚠️  录制将在 3 秒后开始，请确保终端窗口可见"
sleep 3

# 使用 ffmpeg 录制屏幕
# -f avfoundation: macOS 屏幕录制
# -i 1: 录制主屏幕
# -r 30: 30fps
# -t: 录制时长
ffmpeg -f avfoundation \
    -i "1" \
    -r 30 \
    -t "$DURATION" \
    -pix_fmt yuv420p \
    -vf "scale=1280:720" \
    -c:v libx264 \
    -preset fast \
    -crf 23 \
    "$OUTPUT_FILE" 2>&1 | grep -E "(frame|size|time)" || true

echo ""
echo "✅ 录制完成: $OUTPUT_FILE"
ls -lh "$OUTPUT_FILE"