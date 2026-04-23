---
name: openclaw-backup
description: OpenClaw 备份与恢复工具。支持自动/全量/增量备份，包含工作区、配置、数据库的独立备份与清理。当用户需要"备份"、"恢复"、"导出OpenClaw数据"时触发。
metadata:
  openclaw:
    emoji: 💾
---

# OpenClaw Backup Skill

## 备份脚本

`scripts/backup.sh`

### 用法

```bash
# 自动备份（workspace + config + db + 清理）
bash skills/openclaw-backup/scripts/backup.sh auto

# 全量备份（排除 node_modules/cache/sessions）
bash skills/openclaw-backup/scripts/backup.sh full

# 单独备份
bash skills/openclaw-backup/scripts/backup.sh workspace
bash skills/openclaw-backup/scripts/backup.sh config
bash skills/openclaw-backup/scripts/backup.sh db

# 自定义保留天数（默认7天）
KEEP_DAYS=14 bash skills/openclaw-backup/scripts/backup.sh auto
```

### 备份内容

| 模式 | 内容 |
|------|------|
| `auto` | workspace + config + db + 自动清理 |
| `full` | 整个 `~/.openclaw/`（排除缓存） |
| `workspace` | `workspace/` |
| `config` | `openclaw.json` + `agents/` + `extensions/` |
| `db` | `sessions/` + `tasks/` + `memory/` |

### 备份位置

默认：`~/.openclaw/backups/`

可通过环境变量 `BACKUP_DIR` 自定义。

## 恢复

```bash
# 恢复工作区
tar -xzf ~/.openclaw/backups/workspace-YYYYMMDD-HHMMSS.tar.gz -C ~/.openclaw/

# 恢复配置
tar -xzf ~/.openclaw/backups/config-YYYYMMDD-HHMMSS.tar.gz -C ~/.openclaw/

# 恢复全部
tar -xzf ~/.openclaw/backups/full-YYYYMMDD-HHMMSS.tar.gz -C ~/
```

## 定时任务

配合 cron 使用：

```
0 3 * * * KEEP_DAYS=7 bash ~/.openclaw/workspace/skills/openclaw-backup/scripts/backup.sh auto
```
