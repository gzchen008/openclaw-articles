# Telegram + AI 机器人：自动回复、群组管理全搞定

> 本文由 OpenClaw AI 助手协助整理

【快速导航】
- 本文适合：想用 Telegram 做 Bot、群管理的用户
- 预计阅读：5 分钟
- 难度等级：⭐⭐

---

你有没有想过，Telegram 群里有个 24 小时在线的 AI 助手，能自动回答问题、管理成员、甚至帮你发公告？

今天教你用 OpenClaw，5 分钟搞定一个 Telegram AI 机器人。

---

## 🎯 最终效果

配置完成后，你的 Telegram 机器人可以：

✅ 自动回复私聊消息
✅ 在群里智能应答
✅ 自动欢迎新成员
✅ 执行管理命令（踢人、禁言）
✅ 发送定时通知

---

## 📝 准备工作

### 1. 创建 Telegram Bot

1️⃣ 打开 Telegram，搜索 **@BotFather**
2️⃣ 发送 `/newbot`
3️⃣ 按提示设置 Bot 名称
4️⃣ 复制获得的 **Bot Token**（类似 `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

### 2. 获取 Chat ID（群组需要）

1️⃣ 把 Bot 拉进群组
2️⃣ 给群组发一条消息
3️⃣ 访问 `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
4️⃣ 找到 `"chat":{"id": -1001234567890}` 这就是群组 ID

---

## ⚙️ 配置 OpenClaw

### 1. 添加 Telegram 渠道

编辑 OpenClaw 配置文件：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE"
    }
  }
}
```

### 2. 重启 Gateway

```bash
openclaw gateway restart
```

### 3. 测试连接

给你的 Bot 发一条消息，看是否收到回复。

---

## 🤖 进阶功能

### 自动欢迎新成员

在群组设置中，Bot 可以自动发送欢迎消息：

```
欢迎 @username 加入群组！我是 AI 助手，有什么问题随时问我 💬
```

### 定时公告

用 OpenClaw 的 Cron 功能，每天定时发送：

```json
{
  "name": "daily-reminder",
  "schedule": "0 9 * * *",
  "action": "message",
  "channel": "telegram",
  "target": "-1001234567890",
  "message": "早上好！今天的任务清单..."
}
```

### 智能问答

配置关键词触发：

- 用户问 "怎么用？" → 自动发送使用教程
- 用户问 "价格" → 自动发送价目表
- 用户问 "联系方式" → 自动发送客服信息

---

## ⚠️ 常见问题

### Q: Bot 不回复消息？

检查以下几点：
1. Bot Token 是否正确
2. Gateway 是否正常运行（`openclaw gateway status`）
3. 是否给 Bot 发送了 `/start` 命令

### Q: 群组里 Bot 不响应？

1. 确认 Bot 在群里有管理员权限
2. 确认群组隐私模式已关闭（@BotFather → /setprivacy → Disable）

### Q: 如何限制 Bot 只在特定群组工作？

在配置中添加白名单：

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_BOT_TOKEN_HERE",
      "allowedChats": [-1001234567890, -1009876543210]
    }
  }
}
```

---

## 🚀 下一步

配置好 Telegram Bot 后，你可以：

1. 结合 Skills 开发更多功能
2. 用 Cron 做定时推送
3. 接入其他平台（Discord、WhatsApp）统一管理

明天教你 **Slack 配置**，打造程序员专属 AI 编程助手 💻

---

如果这篇文章对你有帮助，欢迎 **点赞、在看、转发** 三连支持！

有任何问题，欢迎在评论区留言，我会一一回复。

明天见 👋
