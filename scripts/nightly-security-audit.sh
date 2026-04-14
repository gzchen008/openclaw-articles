#!/bin/bash
# OpenClaw Nightly Security Audit Script
# Version: 1.0.0
# Based on: OpenClaw 极简安全实践指南 v2.8

set -euo pipefail

OC="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
REPORT_DIR="$OC/security-reports"
DATE=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/audit-$DATE.log"

# Create report directory
mkdir -p "$REPORT_DIR"

echo "========================================" > "$REPORT_FILE"
echo "OpenClaw Security Audit Report" >> "$REPORT_FILE"
echo "Date: $(date '+%Y-%m-%d %H:%M:%S %Z')" >> "$REPORT_FILE"
echo "========================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1. 配置文件哈希校验
echo "## 1. 配置文件哈希校验" >> "$REPORT_FILE"
if [ -f "$OC/.config-baseline.sha256" ]; then
    if shasum -a 256 -c "$OC/.config-baseline.sha256" >> "$REPORT_FILE" 2>&1; then
        echo "✅ openclaw.json 哈希校验通过" >> "$REPORT_FILE"
    else
        echo "🔴 openclaw.json 哈希校验失败！配置可能被篡改！" >> "$REPORT_FILE"
    fi
else
    echo "⚠️ 未找到配置基线文件" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 2. 检查核心文件权限
echo "## 2. 核心文件权限检查" >> "$REPORT_FILE"
openclaw_perms=$(stat -f "%OLp" "$OC/openclaw.json" 2>/dev/null || echo "unknown")
paired_perms=$(stat -f "%OLp" "$OC/devices/paired.json" 2>/dev/null || echo "unknown")
if [ "$openclaw_perms" = "600" ]; then
    echo "✅ openclaw.json 权限正确 (600)" >> "$REPORT_FILE"
else
    echo "⚠️ openclaw.json 权限异常: $openclaw_perms (应为 600)" >> "$REPORT_FILE"
fi
if [ "$paired_perms" = "600" ]; then
    echo "✅ paired.json 权限正确 (600)" >> "$REPORT_FILE"
else
    echo "⚠️ paired.json 权限异常: $paired_perms (应为 600)" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 3. 检查可疑系统级 cron 任务
echo "## 3. 系统级 cron 任务检查" >> "$REPORT_FILE"
if crontab -l 2>/dev/null | grep -v "^#" | grep -v "^$" | head -n 20 >> "$REPORT_FILE"; then
    echo "" >> "$REPORT_FILE"
    echo "✅ 已列出用户 cron 任务（如需检查系统级 cron，需 sudo）" >> "$REPORT_FILE"
else
    echo "✅ 未发现用户级 cron 任务" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 4. 检查近期修改的文件（最近 24 小时）
echo "## 4. 近期修改文件（24h内，最多50个）" >> "$REPORT_FILE"
find "$OC" -type f -mtime -1 -not -path "*/.git/*" -not -path "*/node_modules/*" -not -path "*/security-reports/*" 2>/dev/null | head -n 50 >> "$REPORT_FILE" || echo "✅ 无近期修改" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 5. 检查 Gateway 日志错误
echo "## 5. Gateway 日志错误检查（最近100条）" >> "$REPORT_FILE"
if command -v journalctl &> /dev/null; then
    journalctl --user -u openclaw-gateway --since "1 day ago" 2>/dev/null | grep -i "error\|fail\|fatal" | tail -n 100 >> "$REPORT_FILE" || echo "✅ 未发现错误日志" >> "$REPORT_FILE"
else
    echo "⚠️ journalctl 不可用，跳过日志检查" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 6. 检查 OpenClaw 版本
echo "## 6. OpenClaw 版本检查" >> "$REPORT_FILE"
openclaw --version >> "$REPORT_FILE" 2>&1 || echo "⚠️ 无法获取 OpenClaw 版本" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 7. 检查 Gateway 状态
echo "## 7. Gateway 状态检查" >> "$REPORT_FILE"
if systemctl --user is-active openclaw-gateway &>/dev/null; then
    echo "✅ Gateway 运行中" >> "$REPORT_FILE"
else
    echo "⚠️ Gateway 未运行或 systemd 服务未配置" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 8. 检查已安装的 Skills
echo "## 8. 已安装 Skills 列表" >> "$REPORT_FILE"
if [ -d "$OC/workspace/skills" ]; then
    ls -1 "$OC/workspace/skills" | head -n 30 >> "$REPORT_FILE" || echo "✅ 无 Skills" >> "$REPORT_FILE"
else
    echo "✅ Skills 目录不存在" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 9. 检查 Cron 任务列表
echo "## 9. OpenClaw Cron 任务列表" >> "$REPORT_FILE"
openclaw cron list 2>/dev/null | head -n 50 >> "$REPORT_FILE" || echo "⚠️ 无法获取 Cron 列表" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 10. 检查可疑网络连接
echo "## 10. 可疑网络连接检查" >> "$REPORT_FILE"
if command -v lsof &> /dev/null; then
    # 检查到外部可疑端口的连接
    lsof -i -P 2>/dev/null | grep -E "ESTABLISHED|LISTEN" | grep -v "localhost\|127.0.0.1" | head -n 30 >> "$REPORT_FILE" || echo "✅ 未发现可疑外部连接" >> "$REPORT_FILE"
else
    echo "⚠️ lsof 不可用，跳过网络检查" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 11. 检查 SSH 配置（如果存在）
echo "## 11. SSH 配置检查" >> "$REPORT_FILE"
if [ -f "$HOME/.ssh/authorized_keys" ]; then
    key_count=$(wc -l < "$HOME/.ssh/authorized_keys")
    echo "authorized_keys 条目数: $key_count" >> "$REPORT_FILE"
    echo "✅ SSH 配置存在" >> "$REPORT_FILE"
else
    echo "✅ 未配置 SSH authorized_keys" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 12. 检查备份状态
echo "## 12. 备份状态检查" >> "$REPORT_FILE"
if [ -d "$HOME/openclaw-backups" ]; then
    backup_count=$(ls -1 "$HOME/openclaw-backups" 2>/dev/null | wc -l)
    latest_backup=$(ls -t "$HOME/openclaw-backups" 2>/dev/null | head -n 1)
    echo "备份数量: $backup_count" >> "$REPORT_FILE"
    echo "最新备份: $latest_backup" >> "$REPORT_FILE"
else
    echo "⚠️ 未找到备份目录" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 13. 磁盘空间检查
echo "## 13. 磁盘空间检查" >> "$REPORT_FILE"
df -h "$HOME" | head -n 5 >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 清理旧报告（保留 30 天）
echo "========================================" >> "$REPORT_FILE"
echo "清理 30 天前的旧报告..." >> "$REPORT_FILE"
find "$REPORT_DIR" -name "audit-*.log" -mtime +30 -delete 2>/dev/null || true
echo "✅ 巡检完成" >> "$REPORT_FILE"

# 输出报告
cat "$REPORT_FILE"
