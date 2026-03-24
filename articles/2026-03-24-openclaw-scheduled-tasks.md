# OpenClaw 定时任务配置：让 AI 助手自动工作

定时任务是 OpenClaw 的杀手级功能之一。你可以设置 AI 在特定时间自动执行任务，比如每天早上推送天气、定时检查邮件、自动发布内容等。

今天我们就来详解如何配置 OpenClaw 的定时任务系统。

---

## ⏰ 定时任务的两种方式

OpenClaw 提供两种定时任务机制：

### 1. Cron Jobs（精确调度）

适合需要**精确时间点**执行的任务：
- 每天早上 9 点推送天气
- 每周一发送周报提醒
- 每月 1 号生成月度报告

### 2. Heartbeats（智能轮询）

适合**周期性检查**但不需要精确时间的任务：
- 检查未读邮件（每 30 分钟）
- 查看日历提醒（每 1 小时）
- 监控系统状态（每 5 分钟）

---

## 🔧 Cron Job 配置详解

### 基本结构

```json
{
  "name": "每日天气推送",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "查询上海今天的天气并发送到 Discord"
  },
  "sessionTarget": "isolated"
}
```

### Schedule 类型

**1. 固定时间（at）**
```json
{
  "kind": "at",
  "at": "2026-03-25T09:00:00+08:00"
}
```
一次性任务，指定时间执行一次。

**2. 间隔重复（every）**
```json
{
  "kind": "every",
  "everyMs": 3600000,
  "anchorMs": 0
}
```
每隔固定时间执行（毫秒单位）。

**3. Cron 表达式（cron）**
```json
{
  "kind": "cron",
  "expr": "0 9 * * *",
  "tz": "Asia/Shanghai"
}
```
最灵活，支持标准 cron 语法。

### Cron 表达式速查

| 表达式 | 含义 |
|--------|------|
| `0 9 * * *` | 每天 9:00 |
| `0 9 * * 1` | 每周一 9:00 |
| `0 9 1 * *` | 每月 1 号 9:00 |
| `*/30 * * * *` | 每 30 分钟 |
| `0 9,18 * * *` | 每天 9:00 和 18:00 |

### Payload 类型

**1. systemEvent（注入到主会话）**
```json
{
  "kind": "systemEvent",
  "text": "请检查今天的日程安排"
}
```

**2. agentTurn（独立 agent 执行）**
```json
{
  "kind": "agentTurn",
  "message": "查询天气并发送通知",
  "model": "gpt-4o-mini"
}
```

---

## 💓 Heartbeat 配置详解

Heartbeat 是一种轻量级的轮询机制，AI 会定期检查是否有任务需要执行。

### 配置位置

在 `HEARTBEAT.md` 文件中配置：

```markdown
# 心跳任务

每次心跳时检查以下任务：

- [ ] 检查未读邮件
- [ ] 查看未来 2 小时内的日程
- [ ] 检查 Discord 通知
```

### 智能轮询逻辑

AI 会根据以下原则决定是否执行：

1. **时间间隔**：距离上次检查是否超过阈值
2. **静默时段**：夜间（23:00-08:00）除非紧急否则不打扰
3. **上下文相关**：根据当前对话判断是否需要检查

### 状态追踪

在 `memory/heartbeat-state.json` 中记录：

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "discord": 1703274000
  }
}
```

---

## 🎯 实战案例

### 案例 1：每日天气推送

```json
{
  "name": "每日天气推送",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "查询上海今天和明天的天气，发送到 WhatsApp 私聊"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "none"
  }
}
```

### 案例 2：周报提醒

```json
{
  "name": "周报提醒",
  "schedule": {
    "kind": "cron",
    "expr": "0 18 * * 5",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "提醒：该写周报了！请查看本周的 GitHub 提交记录和任务完成情况"
  },
  "sessionTarget": "main"
}
```

### 案例 3：定时内容发布

```json
{
  "name": "每日公众号文章",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "执行每日公众号文章生成任务：读取发布计划、生成文章、创建草稿、通知用户"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce"
  }
}
```

---

## 📋 最佳实践

### 选择合适的类型

| 场景 | 推荐方式 |
|------|----------|
| 精确时间点执行 | Cron Job |
| 周期性检查，可漂移 | Heartbeat |
| 需要隔离执行 | agentTurn |
| 需要对话上下文 | systemEvent |

### 避免常见错误

1. **时区问题**：始终指定 `tz` 参数
2. **重复任务**：避免同时使用 cron 和 heartbeat 做同样的事
3. **资源消耗**：不要设置过于频繁的任务（如每分钟）
4. **错误处理**：任务失败时确保有通知机制

### 调试技巧

查看任务状态：
```bash
# 列出所有 cron jobs
curl http://localhost:3000/api/cron/list

# 查看任务执行历史
curl http://localhost:3000/api/cron/runs/{jobId}
```

---

## 🚀 进阶用法

### 条件触发

在 heartbeat 中使用条件判断：

```markdown
# 心跳任务

- [ ] 如果是工作日 9:00-18:00，检查邮件
- [ ] 如果是周末，跳过邮件检查
- [ ] 如果下雨，提醒带伞
```

### 链式任务

一个任务触发另一个任务：

```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "检查邮件，如果有重要邮件则发送 Discord 通知，并创建飞书任务跟进"
  }
}
```

### 多时区支持

为不同地区的用户配置：

```json
[
  {
    "name": "上海天气",
    "schedule": { "expr": "0 8 * * *", "tz": "Asia/Shanghai" }
  },
  {
    "name": "纽约天气",
    "schedule": { "expr": "0 8 * * *", "tz": "America/New_York" }
  }
]
```

---

## 💡 总结

定时任务让 OpenClaw 从被动响应变成主动服务。合理配置后，你的 AI 助手可以：

- 早上自动推送天气和日程
- 定期检查重要信息并通知
- 在合适的时间提醒你做事
- 自动执行重复性工作

关键是选择合适的方式（Cron vs Heartbeat），设置合理的频率，并确保有错误通知机制。

如果觉得有用，点个"在看"吧 👇
