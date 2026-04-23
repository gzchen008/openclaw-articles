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

### 备份任务详情
- **首次成功执行**: 2026-04-16 (实际时间: 11:05 AM)
- **备份大小**: 631.5 MB (工作区占主导)
- **备份模式**: auto (workspace + config + db)
- **通知状态**: 飞书配置需要修复，企业微信MCP不可用
- **完整报告**: `workspace/backup-status-2026-04-16.md`

### 公众号进度
- **仓库**：`gzchen008/openclaw-articles`
- **进度**：15/28 篇（入门+进阶基本完成，场景/高级待续）
- **计划**：`projects/ai-user-guide/`

### 创业项目：小红书文案 AI
- **AI用户指南**：`projects/ai-user-guide/`
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

## 角色风格

- **默认（所有场景）**：专业职能助手，高效简洁
- **女朋友模式**：已停用并删除相关资料 (2026-04-23)

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
├── girlfriend-scenes/           # [已删除 2026-04-23]
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

## Promoted From Short-Term Memory (2026-04-19)

<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:7:8 -->
- **待关注**: - 备份任务超时问题需解决 - AI用户指引项目进度跟踪 ## Light Sleep <!-- openclaw:dreaming:light:start --> - Candidate: 📋 工作日报生成 (2026-04-13 12:00:00): **任务ID**: daily-review-report **完成内容**: [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:38-45]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:9:12 -->
- ## Light Sleep <!-- openclaw:dreaming:light:start --> - Candidate: 📋 工作日报生成 (2026-04-13 12:00:00): **任务ID**: daily-review-report **完成内容**: - confidence: 0.00 - evidence: memory/2026-04-13.md:7-8 - recalls: 0 - status: staged - Candidate: 📋 工作日报生成 (2026-04-13 12:00:00): 查看 memory/2026-04-12.md 昨日工作记录; 分析 MEMORY.md 中的任务状态; 检查 cron 任务执行情况; 生成并发送工作日报到飞书私聊 [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:43-50]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:13:13 -->
- - recalls: 0 - status: staged - Candidate: 📋 工作日报生成 (2026-04-13 12:00:00): 查看 memory/2026-04-12.md 昨日工作记录; 分析 MEMORY.md 中的任务状态; 检查 cron 任务执行情况; 生成并发送工作日报到飞书私聊 - confidence: 0.00 - evidence: memory/2026-04-13.md:9-12 - recalls: 0 - status: staged - Candidate: 📋 工作日报生成 (2026-04-13 12:00:00): 统计估算：运行时间8.5小时，Token消耗174k，Cron任务12次 [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:48-55]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:19:19 -->
- - recalls: 0 - status: staged - Candidate: 📋 工作日报生成 (2026-04-13 12:00:00): 统计估算：运行时间8.5小时，Token消耗174k，Cron任务12次 - confidence: 0.00 - evidence: memory/2026-04-13.md:13-13 - recalls: 0 - status: staged - Candidate: 📊 系统运行状态: **Cron 任务执行情况**: [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:53-60]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:20:23 -->
- - recalls: 0 - status: staged - Candidate: 📊 系统运行状态: **Cron 任务执行情况**: - confidence: 0.00 - evidence: memory/2026-04-13.md:19-19 - recalls: 0 - status: staged - Candidate: 📊 系统运行状态: ✅ daily-wechat-article (09:00) - 公众号文章生成完成; ✅ daily-github-recommendation (10:00) - GitHub项目推荐完成; ✅ ai-user-guide-morning (10:00) - AI用户指引更新完成; ✅ daily-openclaw-version-check (09:00) - 版本检查完成（无更新） [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:58-65]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:24:26 -->
- - recalls: 0 - status: staged - Candidate: 📊 系统运行状态: ✅ daily-wechat-article (09:00) - 公众号文章生成完成; ✅ daily-github-recommendation (10:00) - GitHub项目推荐完成; ✅ ai-user-guide-morning (10:00) - AI用户指引更新完成; ✅ daily-openclaw-version-check (09:00) - 版本检查完成（无更新） - confidence: 0.00 - evidence: memory/2026-04-13.md:20-23 - recalls: 0 - status: staged - Candidate: 📊 系统运行状态: ⚠️ daily-openclaw-backup (03:00) - 备份超时，需要优化; ✅ nightly-security-audit (03:00) - 安全巡检正常; ✅ 其他日常任务正常执行 [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:63-70]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:33:36 -->
- - recalls: 0 - status: staged - Candidate: 📋 今日任务清单: **主要进行中**: - confidence: 0.00 - evidence: memory/2026-04-13.md:32-32 - recalls: 0 - status: staged - Candidate: 📋 今日任务清单: 公众号内容创作（AI 资讯深度解读）- 本周第15篇; 每日工作回顾（刚完成日报生成）; GitHub 开源项目推荐（昨已完成）; AI 用户指引项目维护（持续进行中） [score=0.838 recalls=0 avg=0.620 source=memory/2026-04-13.md:73-80]
<!-- openclaw-memory-promotion:memory:memory/2026-04-13.md:32:32 -->
- - recalls: 0 - status: staged - Candidate: 📊 系统运行状态: ⚠️ daily-openclaw-backup (03:00) - 备份超时，需要优化; ✅ nightly-security-audit (03:00) - 安全巡检正常; ✅ 其他日常任务正常执行 - confidence: 0.00 - evidence: memory/2026-04-13.md:24-26 - recalls: 0 - status: staged - Candidate: 📋 今日任务清单: **主要进行中**: [score=0.828 recalls=0 avg=0.620 source=memory/2026-04-13.md:68-75]
<!-- openclaw-memory-promotion:memory:memory/2026-04-14.md:379:381 -->
- - # 2026-04-01 日志 ## 系统通知 ### 14:28 - Ease 异步 Skill 限流机制分析完成 - 子任务完成通知 - 分析已完成 --- ### 16:26 - Ease 异步提交 Skill 使用方法 **工具位置**: `./ease-async.sh` **用法**: ```bash # 从任意目录指定项目路径 ./ease-async.sh -d ./wcs-java "分析重复代码" ./ease-async.sh -d ~/projects/wcs-java "重构数据库模块" ./ease-async.sh --dir /path/to/project "添加新功能" # 在项目目录内直接执行 cd wcs-java && ../ease-async.sh "分析重复代码" ``` **特点**: - 支持在 `wbproject` 目录下管理多个子项目的异步任务 - `-d` / `--dir` 参数指定项目路径 - 可以在项目目录内直接执行（相对路径） --- ## 状态 - 共享知识库同步：昨天已完成 (2026-03-31) - 下次同步：下周一 (2026-04-07) [confidence=0.62 evidence=memory/2026-04-01.md:1-36] - - Candidate: Possible Lasting Truths: - **组合协作模式**：多技能完成复杂任务 - **智能编排模式**：Coordinator 自动选择技能组合 **架构优势**： - 渐进式加载，按需启动 - 资源复用，避免重复初始化 - 优雅降级，错误容错机制 #### 3. 工具整合的高级模式 **统一抽象层设计**： - API 封装：Notion/Google Workspace/Linear 接口统一 - 事件驱动：Webhook 接收器响应外部事件 - 资源调度：跨技能共享上下文和数据 **技术实现要点**： - 配置管理标准化（JSON - confidence: 0.00 - evidence: memory/2026-04-09.md:378-378 - recalls: 0 - status: staged - Candidate: Possible Lasting Truths: # 2026-04-01 日志 ## 系统通知 ### 14:28 - Ease 异步 Skill 限流机制分析完成 - 子任务完成通知 - 分析已完成 --- ### 16:26 - Ease 异步提交 Skill 使用方法 **工具位置**: `./ease-async.sh` **用法**: ```bash # 从任意目录指定项目路径 ./ease-async.sh -d ./wcs-java "分析重复代码" ./ease-async.sh -d ~/projects/wcs-java "重构数据 - confidence [confidence=0.61 evidence=memory/2026-04-09.md:188-197] - - evidence: memory/2026-04-02.md:21-24 - recalls: 0 - status: staged - Candidate: 备份文件列表: *备份任务自动运行正常* - confidence: 0.00 - evidence: memory/2026-04-02.md:27-27 - recalls: 0 - status: staged - Candidate: 16:26 - Ease 异步提交 Skill 使用方法: **工具位置**: `./ease-async.sh` - confidence: 0.00 - evidence: memory/2026-04-01.md:13-13 - recalls: 0 - status: staged - Candidate: 从任意目录指定项目路径: ./ease-async.sh -d ./wcs-java "分析重复代码" ./ease-async.sh -d ~/projects/wcs-java "重构数据库模块" ./ease-async.sh --dir /path/to/project "添加新功能" - confidence: 0.00 - evidence: memory/2026-04-01.md:18-20 - recalls: 0 - status: staged - Candidate: 在项目目录内直接执行: cd wcs-java && ../ease-async.sh "分析重复代码" - c [confidence=0.61 evidence=memory/2026-04-09.md:125-157] [score=0.821 recalls=0 avg=0.620 source=memory/2026-04-14.md:379-381]

## Promoted From Short-Term Memory (2026-04-20)

<!-- openclaw-memory-promotion:memory:memory/2026-04-15.md:413:415 -->
- - Candidate: Possible Lasting Truths: # 2026-04-01 日志 ## 系统通知 ### 14:28 - Ease 异步 Skill 限流机制分析完成 - 子任务完成通知 - 分析已完成 --- ### 16:26 - Ease 异步提交 Skill 使用方法 **工具位置**: `./ease-async.sh` **用法**: ```bash # 从任意目录指定项目路径 ./ease-async.sh -d ./wcs-java "分析重复代码" ./ease-async.sh -d ~/projects/wcs-java "重构数据 - confidence: 0.00 - evidence: memory/2026-04-14.md:379-381 [score=0.822 recalls=0 avg=0.620 source=memory/2026-04-15.md:8-10]
