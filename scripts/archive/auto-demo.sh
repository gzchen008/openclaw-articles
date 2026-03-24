#!/bin/bash
echo "========================================="
echo "  浏览器自动化演示 - AI 驱动"
echo "========================================="
echo ""

echo "[$(date '+%H:%M:%S.%3N')] 🚀 启动浏览器..."
agent-browser open https://www.baidu.com --headed

echo "[$(date '+%H:%M:%S.%3N')] 📸 获取页面元素..."
agent-browser snapshot -i | grep -E "textbox|button" | head -5

echo "[$(date '+%H:%M:%S.%3N')] ⌨️  输入搜索词..."
agent-browser fill @e1 "OpenClaw AI自动化"

echo "[$(date '+%H:%M:%S.%3N')] 🔍 执行搜索..."
agent-browser press Enter

sleep 1
echo "[$(date '+%H:%M:%S.%3N')] ✅ 搜索完成，获取结果..."
agent-browser snapshot -i | head -10

echo ""
echo "[$(date '+%H:%M:%S.%3N')] 🎬 关闭浏览器"
agent-browser close

echo ""
echo "========================================="
echo "  演示完成 - 全程自动化执行"
echo "  人类无法达到毫秒级精准操作"
echo "========================================="
