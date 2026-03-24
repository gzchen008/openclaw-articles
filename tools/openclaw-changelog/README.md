# OpenClaw 更新追踪工具

每天自动检查 OpenClaw 版本更新并生成公众号文章。

## 文件结构

```
tools/openclaw-changelog/
├── track.sh              # 版本检查脚本
├── generate-article.py    # 公众号文章生成器
├── daily-check.sh        # 每日检查入口脚本
├── cron.json             # 定时任务配置
└── README.md             # 本文档
```

## 工作流程

```
1. track.sh 检查 GitHub 最新版本
   ↓
2. 生成 state.json 状态文件
   ↓
3. generate-article.py 解析更新日志
   ↓
4. 生成 Markdown 公众号文章
   ↓
5. 保存到 articles/openclaw-updates/
```

## 手动运行

### 检查版本

```bash
cd /Users/cgz/.openclaw/workspace/tools/openclaw-changelog
./track.sh > /tmp/openclaw-update.json
```

### 生成文章

```bash
python3 generate-article.py /tmp/openclaw-update.json
```

### 完整流程

```bash
./daily-check.sh
```

## 定时任务配置

每天早上 8:00 自动执行检查：

```json
{
  "name": "daily-openclaw-update-check",
  "enabled": true,
  "schedule": "0 8 * * *",
  "command": "/Users/cgz/.openclaw/workspace/tools/openclaw-changelog/daily-check.sh",
  "description": "每天 8:00 检查 OpenClaw 版本更新并生成公众号文章",
  "timezone": "Asia/Shanghai"
}
```

### 启用定时任务

```bash
# 使用 OpenClaw CLI
openclaw cron create tools/openclaw-changelog/cron.json
```

### 列出定时任务

```bash
openclaw cron list
```

### 禁用定时任务

```bash
openclaw cron disable daily-openclaw-update-check
```

## 输出文件

生成的公众号文章保存在：

```
articles/openclaw-updates/
└── openclaw-update-{version}-{date}.md
```

例如：
- `openclaw-update-v2026.3.7-20260308.md`

## 文章格式

生成的公众号文章包含：

1. **版本信息** - 版本号 + 发布日期
2. **更新总览** - 简短介绍
3. **新功能** - 最多显示 5 项重要功能
4. **破坏性变更** - Breaking Changes
5. **Bug 修复** - 最多显示 5 项重要修复
6. **升级指南** - 升级命令 + 版本检查
7. **相关资源** - 文档、社区、GitHub 链接

## 日志文件

检查日志保存在：

```
tools/openclaw-changelog/check.log
```

## 状态文件

上次的检查状态保存在：

```
tools/openclaw-changelog/state.json
```

包含：
- `last_version` - 上次记录的版本
- `last_check` - 上次检查日期

## 故障排查

### 脚本无法执行

```bash
chmod +x track.sh daily-check.sh
```

### Python 脚本报错

```bash
# 确保使用 Python 3
python3 --version

# 检查依赖
pip3 install requests beautifulsoup4  # 如果需要
```

### 没有检测到新版本

检查 `state.json` 中的 `last_version`，如果和最新版本相同，不会生成文章。

可以手动删除 `state.json` 强制重新生成：

```bash
rm tools/openclaw-changelog/state.json
./daily-check.sh
```

## 自动发布到公众号（待扩展）

生成的文章可以通过微信公众号 API 自动发布。需要配置：

1. `WECHAT_APPID` - 公众号 AppID
2. `WECHAT_SECRET` - 公众号 AppSecret

然后在 `daily-check.sh` 中添加发布逻辑。

## 相关资源

- OpenClaw 文档: https://docs.openclaw.ai
- GitHub Releases: https://github.com/openclaw/openclaw/releases
- Discord 社区: https://discord.gg/clawd
