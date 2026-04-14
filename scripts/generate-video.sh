#!/bin/bash

# Simple video generator for OpenClaw v2026.4.2 update
# This creates a basic MP4 video using ffmpeg

VIDEO_OUTPUT="/Users/cgz/.openclaw/workspace-content-lead/articles/openclaw-v2026.4.2-update-video.mp4"
TITLE="OpenClaw v2026.4.2 发布：重大更新与功能增强"
CURRENT_DATE=$(date +%Y-%m-%d)
VERSION="v2026.4.2"

# Create a simple video with text overlays
echo "🎬 Generating OpenClaw v2026.4.2 update video..."

# Create temporary text files for video content
TEMP_DIR=$(mktemp -d)

# Create title card
cat > "$TEMP_DIR/title.txt" << EOF
${TITLE}
发布日期: ${CURRENT_DATE}
版本: ${VERSION}

🎉 重大更新与功能增强
🚀 插件系统重构
📊 任务流管理增强
🔒 安全性重大改进
📱 多平台支持增强
EOF

# Create feature highlights card
cat > "$TEMP_DIR/features.txt" << EOF
🎯 主要特性

🔧 插件系统重构
- 配置路径标准化
- 统一认证机制
- 自动配置迁移

⚡ 任务流管理
- 托管与镜像同步
- 持久化状态跟踪
- openclaw flows 检查工具

🛡️ 安全性增强
- 传输策略集中化
- 执行权限改进
- 认证标准化

🌐 多平台支持
- Android 助手集成
- Feishu/Matrix 增强
- 改进的用户体验
EOF

# Create call-to-action card
cat > "$TEMP_DIR/cta.txt" << EOF
📥 立即升级

🔗 下载链接:
• macOS 版本: OpenClaw-2026.4.2.dmg
• 源代码: OpenClaw-2026.4.2.zip
• 调试符号: OpenClaw-2026.4.2.dSYM.zip

💡 升级建议:
1. 运行 openclaw doctor --fix 迁移配置
2. 重启 OpenClaw 服务
3. 检查权限设置

📞 技术支持:
• GitHub Issues
• 官方文档
• 社区论坛
EOF

# Generate video using ffmpeg with text overlays
ffmpeg -y \
-f lavfi -i color=c=#1a1a1a:s=1920x1080:d=3 \
-vf "drawtext=textfile='$TEMP_DIR/title.txt':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=48:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:borderw=3:bordercolor=black" \
-t 3 \
-f lavfi -i color=c=#1a1a1a:s=1920x1080:d=5 \
-vf "drawtext=textfile='$TEMP_DIR/features.txt':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=36:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:borderw=2:bordercolor=black" \
-t 5 \
-f lavfi -i color=c=#1a1a1a:s=1920x1080:d=7 \
-vf "drawtext=textfile='$TEMP_DIR/cta.txt':fontfile=/System/Library/Fonts/PingFang.ttc:fontsize=28:fontcolor=white:x=(w-tw)/2:y=(h-th)/2:borderw=2:bordercolor=black" \
-t 7 \
-filter_complex "[0:v][1:v][2:v]concat=n=3:v=1:a=0" \
-c:v libx264 -preset fast -crf 23 -pix_fmt yuv420p \
"$VIDEO_OUTPUT"

# Clean up temporary files
rm -rf "$TEMP_DIR"

echo "✅ Video generated: $VIDEO_OUTPUT"
echo "📏 Video duration: $(ffprobe -i "$VIDEO_OUTPUT" -show_entries format=duration -v quiet -of csv='p=0') seconds"
echo "🎬 Video format: 1920x1080 horizontal (16:9)"