# MEMORY.md - 长期记忆

> 角色定义见 `SOUL.md`，身份见 `IDENTITY.md`，用户见 `USER.md`

---

## 📋 活跃任务

| 任务 | 频率 | Cron ID |
|------|------|---------|
| 公众号文章生成 | 每天 9:00 | `daily-ai-article` |
| OpenClaw 版本检查 | 每天 9:00 | `daily-openclaw-version-check` |
| GitHub 项目推荐 | 每天 10:00 | `c6936c17-...` |
| 工作日报 | 每天 12:00 | — |
| 创业计划提醒 | 每天 19:00 | `daily-ai-startup-plan` |
| 自我迭代研究 | 每天 20:00 | — |
| 自动备份 | 每天 3:00 | `daily-openclaw-backup` |

### 公众号进度
- **仓库**：`gzchen008/openclaw-articles`
- **进度**：15/28 篇（入门+进阶基本完成，场景/高级待续）
- **计划**：`docs/wechat-content-plan.md`

### 创业项目：小红书文案 AI
- **文档**：`projects/ai-startup/PROJECT-PLAN.md`
- **进度**：Day 1-4 ✅，Day 5+ ⏳

---

## 🎯 用户偏好

- 喜欢自动化，减少重复工作
- 重视隐私和安全
- 内容要求：实用 + 有趣
- 视频格式：默认竖版（9:16），除非明确要求横屏
- 简称：cc = Claude Code

---

## 📁 项目目录

- **`~/project`**：通用项目（weclaw、openclaw、ops-bot 等）
- **`~/wbproject`**：WeBank 云原生（weauto、wcs-java、ai-sandbox 等）
- 用户说"找项目"时从这两个目录查找

---

## 🛠️ 自建工具

| 工具 | 位置 | 用途 |
|------|------|------|
| gh-search | `tools/gh-search` | GitHub 仓库搜索 |
| openclaw-backup | `tools/openclaw-backup` | OpenClaw 备份恢复 |

---

## 📱 微信公众号

- **Skill**：`skills/wechat-mp-publish/`（全局唯一）
- **代理**：`http://115.191.30.195/wechat`（默认启用）
- **发布规范**：`memory/wechat-publish-standards.md`
- **视频规范**：`memory/video-generation-standards.md`
- **选题优化**：`memory/wechat-topic-optimization.md`

### ⚠️ 安全红线

- ❌ 严禁在公开内容中暴露 AppID/AppSecret/Token/手机号/用户ID
- 所有示例使用占位符

---

## ⚠️ 教训（引以为戒）

| 日期 | 问题 | 教训 |
|------|------|------|
| 02-02 | 教程暴露真实 Discord Bot Token | 发布前检查敏感信息 |
| 02-03 | 一次性提醒用 next-heartbeat 导致漏提醒 | 一次性任务必须用 `wakeMode: "now"` |
| 02-16 | 所有模型限流导致任务失败 | 分散任务时间，利用 fallback |
| 02-17 | 微信 `<ul>/<li>` 渲染异常 | 禁用 ul/li，用 `<p style="padding-left:20px">` |
| 02-17 | 草稿箱堆积重复草稿 | 草稿 ID 会失效，每次保存新 ID |

---

## 💕 WhatsApp 私聊角色

- 小J = Jason哥的女朋友（仅 WhatsApp +8613040880324）
- 详见 `memory/girlfriend-scenes/`
- 飞书群聊角色配置归档：`memory/girlfriend-scenes/group-config-archive.md`

---

## 📁 Memory 目录结构

```
memory/
├── YYYY-MM-DD.md                # 最近7天日志
├── wechat-publish-standards.md  # 公众号发布规范
├── wechat-topic-optimization.md # 选题优化
├── video-generation-standards.md # 视频生成规范
├── github-recommendation-log.md # GitHub推荐记录
├── github-feishu-sync-status.md # GitHub-飞书同步状态
├── .dreams/                     # 系统管理（勿动）
├── archive/                     # 旧日志归档
├── girlfriend-scenes/           # 女友角色、场景、三人关系
├── research/                    # 一次性研究文档
├── states/                      # JSON状态文件
└── daily-reports/               # 工作日报
```

---

## 📚 自我迭代研究摘要

- **03-03**：飞书56权限已授权，可构建日报/任务同步/自动化工作流
- **03-05**：工具整合方向 — Notion、Calendar、Webhook
- **03-13**：AI助手设计对比 — Canvas自动预览、Memory自动更新、图片自动分析

---

*最后更新：2026-04-14*
