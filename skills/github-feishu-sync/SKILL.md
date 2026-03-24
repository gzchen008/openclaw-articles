---
name: github-feishu-sync
description: |
  GitHub仓库到飞书文档的自动同步工具。支持定时同步、增量更新、API限频处理。
  
  使用场景：
  - 将GitHub仓库的Markdown文档同步到飞书
  - 定时自动同步（配合Cron任务）
  - 增量同步（只同步新增/修改的文件）
  - 处理API限频（自动等待重试）
  - 记录同步进度和状态
---

# GitHub -> 飞书同步工具

将GitHub仓库的Markdown文档自动同步到飞书云文档。

## 🎯 核心功能

1. **自动同步** - 从GitHub读取文件并创建飞书文档
2. **增量更新** - 只同步新增或修改的文件
3. **限频处理** - 自动处理API限频，智能等待重试
4. **进度记录** - 记录同步状态，支持断点续传
5. **定时任务** - 可配置Cron定时同步

## 📋 使用方法

### 1. 首次同步

```bash
# 同步指定仓库
python scripts/sync_github_to_feishu.py \
  --repo gzchen008/ai-user-guide \
  --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic \
  --full-sync
```

### 2. 增量同步

```bash
# 只同步新增/修改的文件
python scripts/sync_github_to_feishu.py \
  --repo gzchen008/ai-user-guide \
  --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic
```

### 3. 定时同步（Cron）

```bash
# 每天凌晨2点自动同步
0 2 * * * cd /Users/cgz/.openclaw/workspace/skills/github-feishu-sync && python scripts/sync_github_to_feishu.py --repo gzchen008/ai-user-guide --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic
```

## ⚙️ 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--repo` | GitHub仓库名 | `gzchen008/ai-user-guide` |
| `--folder-token` | 飞书文件夹Token | `OwM2fGLEJlBrOjdEUdQcmXmOnic` |
| `--full-sync` | 全量同步 | 不加此参数则为增量同步 |
| `--delay` | 每次创建后等待秒数 | 默认3秒 |
| `--max-retries` | 最大重试次数 | 默认5次 |

## 🔧 核心逻辑

### 1. 文件过滤

只同步`.md`文件，自动跳过：
- `README.md`（已手动创建）
- `CHANGELOG.md`（版本日志）
- `.github/`目录下的文件

### 2. 格式转换

Markdown -> 飞书格式转换规则：
- 标题 → 飞书标题（保留层级）
- 列表 → 飞书列表
- 表格 → 飞书表格
- 代码块 → 飞书代码块
- Callout → 飞书高亮块
- 链接 → 保留外部链接，移除相对链接

### 3. 限频处理

遇到以下错误自动等待重试：
- `folder locked` → 等待5秒后重试
- `request trigger frequency limit` → 等待10秒后重试
- 最大重试5次

### 4. 进度记录

同步进度保存在：
```
/Users/cgz/.openclaw/workspace/memory/github-feishu-sync-status.json
```

记录内容包括：
- 已同步文件列表
- 同步时间戳
- 失败文件和错误信息

## 📊 同步状态

查看同步进度：

```bash
# 查看状态文件
cat /Users/cgz/.openclaw/workspace/memory/github-feishu-sync-status.json

# 或让AI助手查询
"查看GitHub到飞书的同步进度"
```

## ⚠️ 注意事项

1. **API限制** - 飞书API有频率限制，建议每次同步间隔3秒以上
2. **文件夹锁定** - 连续创建可能触发锁定，脚本会自动等待重试
3. **链接问题** - 相对链接在飞书中不支持，会被移除
4. **授权要求** - 需要飞书用户授权（首次使用会提示）

## 🔄 定时任务配置

### OpenClaw Cron配置

```json
{
  "id": "github-feishu-sync-daily",
  "schedule": "0 2 * * *",
  "timezone": "Asia/Shanghai",
  "command": "sync-github-feishu",
  "params": {
    "repo": "gzchen008/ai-user-guide",
    "folder-token": "OwM2fGLEJlBrOjdEUdQcmXmOnic"
  },
  "enabled": true
}
```

### 配置说明

- **触发时间**：每天凌晨2点（避免API高峰期）
- **时区**：Asia/Shanghai
- **命令**：`sync-github-feishu`（自定义命令，需要注册）
- **参数**：仓库名和文件夹Token

## 📝 示例工作流

### 场景1：首次全量同步

```bash
# 1. 确认授权
"我已完成飞书账号授权"

# 2. 开始全量同步
python scripts/sync_github_to_feishu.py \
  --repo gzchen008/ai-user-guide \
  --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic \
  --full-sync

# 3. 查看进度
"查看同步进度"
```

### 场景2：定时增量同步

```bash
# 1. 配置Cron任务
openclaw cron add github-feishu-sync-daily \
  --schedule "0 2 * * *" \
  --command "sync-github-feishu" \
  --params '{"repo":"gzchen008/ai-user-guide","folder-token":"OwM2fGLEJlBrOjdEUdQcmXmOnic"}'

# 2. 启用任务
openclaw cron enable github-feishu-sync-daily

# 3. 查看任务状态
openclaw cron status github-feishu-sync-daily
```

### 场景3：手动增量同步

```bash
# 只同步GitHub上有更新的文件
python scripts/sync_github_to_feishu.py \
  --repo gzchen008/ai-user-guide \
  --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic
```

## 🐛 故障排查

### 问题1：授权过期

**症状**：提示"需要授权"

**解决**：
```
"重新授权飞书账号"
```

### 问题2：文件夹锁定

**症状**：`folder locked`错误

**解决**：
- 脚本会自动等待5秒重试
- 如果持续失败，等待10分钟后手动重试

### 问题3：API限频

**症状**：`request trigger frequency limit`错误

**解决**：
- 脚本会自动等待10秒重试
- 增加`--delay`参数（如`--delay 5`）

## 📚 相关资源

- [飞书开放平台文档](https://open.feishu.cn/document/)
- [GitHub API文档](https://docs.github.com/en/rest)
- [同步状态文件](../../memory/github-feishu-sync-status.json)
