# GitHub -> 飞书同步 Skill

自动将GitHub仓库的Markdown文档同步到飞书云文档。

## 🎯 功能特性

- ✅ **自动同步** - 从GitHub读取文件并创建飞书文档
- ✅ **增量更新** - 只同步新增或修改的文件
- ✅ **限频处理** - 自动处理API限频，智能等待重试
- ✅ **进度记录** - 记录同步状态，支持断点续传
- ✅ **定时任务** - 可配置Cron定时同步

## 📦 安装

Skill已创建在：
```
/Users/cgz/.openclaw/workspace/skills/github-feishu-sync/
```

## 🚀 快速开始

### 方式1：通过OpenClaw对话

```
"同步GitHub仓库 gzchen008/ai-user-guide 到飞书"
```

### 方式2：命令行

```bash
python /Users/cgz/.openclaw/workspace/skills/github-feishu-sync/scripts/sync_github_to_feishu.py \
  --repo gzchen008/ai-user-guide \
  --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic
```

### 方式3：定时任务

```bash
# 每天凌晨2点自动同步
0 2 * * * python /Users/cgz/.openclaw/workspace/skills/github-feishu-sync/scripts/sync_github_to_feishu.py --repo gzchen008/ai-user-guide --folder-token OwM2fGLEJlBrOjdEUdQcmXmOnic
```

## 📊 当前进度

**已同步：42/75 文档（56%）**

### ✅ 已完成
- 01-新手入门（6篇）
- 02-AI工具大全（27篇）
- 03-AI编程（9篇）

### ⏳ 待完成
- 03-AI编程（剩余6篇）
- 04-AI应用场景（15篇）
- 05-学习资源（5篇）
- 06-行业资讯（5篇）
- 07-常见问题（7篇）

## 📝 同步状态

查看详细进度：
```bash
cat /Users/cgz/.openclaw/workspace/memory/github-feishu-sync-status.json
```

或让AI助手：
```
"查看GitHub到飞书的同步进度"
```

## 🔧 配置

### 修改同步间隔

默认每次创建后等待3秒，可通过`--delay`参数调整：

```bash
python scripts/sync_github_to_feishu.py --delay 5 ...
```

### 全量同步

默认为增量同步（只同步新文件），添加`--full-sync`参数进行全量同步：

```bash
python scripts/sync_github_to_feishu.py --full-sync ...
```

## 🐛 故障排查

### 问题：API限频

**解决方案**：
1. 增加`--delay`参数（如5秒）
2. 等待10分钟后重试
3. 脚本会自动重试（最多5次）

### 问题：文件夹锁定

**解决方案**：
- 脚本会自动等待5秒重试
- 如果持续失败，等待10分钟

### 问题：授权过期

**解决方案**：
```
"重新授权飞书账号"
```

## 📚 相关文档

- [SKILL.md](./SKILL.md) - 完整使用说明
- [scripts/sync_github_to_feishu.py](./scripts/sync_github_to_feishu.py) - 同步脚本
- [同步状态文件](../../memory/github-feishu-sync-status.json)

---

**创建时间**：2026-03-21
**作者**：小J (OpenClaw AI)
