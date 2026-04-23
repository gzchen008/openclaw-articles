# Telegram + AI 机器人：自动回复、群组管理全搞定

> 本文由 OpenClaw AI 助手协助整理

【快速导航】
- 本文适合：想用 Telegram 做 AI Bot 的用户
- 预计阅读：5 分钟
- 难度等级：⭐⭐

---

你有没有想过，让 Telegram 群里有个 24 小时在线的 AI 助手，自动回答问题、管理成员、甚至帮你发公告？

想象一下，你在睡觉，AI 在群里帮你回复新人的常见问题；你在忙工作，AI 自动踢掉发广告的机器人；你想发公告，一句话就让 AI 同步到所有群组。

这不是科幻，OpenClaw + Telegram 就能做到。

今天教你 5 分钟搭建一个 Telegram AI Bot，让你的群组管理效率提升 10 倍。

---

## 🎯 最终效果

搭建完成后，你的 Telegram Bot 可以：

- **自动回复私聊**：用户私信机器人，AI 自动回答
- **群组智能对话**：在群里 @机器人，AI 回答问题
- **管理功能**：自动踢广告、欢迎新成员
- **定时公告**：每天自动发送群公告
- **多群同步**：一条消息同时推送到多个群

---

## 📋 前置条件

在开始之前，你需要：

- 一台能访问互联网的电脑（本地或服务器）
- 已安装 OpenClaw（还没安装？看[这篇教程](https://docs.openclaw.ai)）
- 一个 Telegram 账号

---

## 🔧 第一步：创建 Telegram Bot

Telegram Bot 需要通过 BotFather 创建。

**操作步骤：**

1. 在 Telegram 搜索 `@BotFather`
2. 发送 `/newbot`
3. 按提示输入机器人名称（如：`OpenClaw AI Assistant`）
4. 输入机器人用户名（如：`openclaw_ai_bot`，必须以 `_bot` 结尾）
5. **复制 API Token**（格式：`123456789:ABCdefGHIjklMNOpqrsTUVwxyz`）

**⚠️ 重要：Token 只显示一次，务必保存好！**

---

## ⚙️ 第二步：配置 OpenClaw

拿到 Token 后，配置 OpenClaw。

**编辑配置文件：**

打开 `~/.openclaw/openclaw.json`，添加 Telegram 配置：

```json
{
  "telegram": {
    "enabled": true,
    "token": "YOUR_BOT_TOKEN_HERE"
  }
}
```

**⚠️ 安全提示：**
- Token 不要提交到 GitHub
- 不要在公开场合泄露 Token
- 如果泄露，立即去 BotFather 重新生成

---

## 🤖 第三步：启动机器人

配置好后，启动 OpenClaw：

```bash
openclaw start
```

或者直接运行：

```bash
npx openclaw start
```

启动成功后，你会看到类似日志：

```
[telegram] Bot started: @openclaw_ai_bot
[telegram] Webhook set successfully
```

---

## 💬 第四步：测试机器人

现在去 Telegram 测试一下。

**私聊测试：**

1. 在 Telegram 搜索你的机器人用户名
2. 点击 `Start` 或发送 `/start`
3. 发送任意消息，AI 会自动回复

**群组测试：**

1. 把机器人拉进群组
2. 在群里 @机器人（如：`@openclaw_ai_bot 你好`）
3. AI 会回复你的消息

---

## 🎨 进阶功能

### 1️⃣ 自动欢迎新成员

当有人进群，机器人自动发欢迎消息。

**配置方法：**

在 OpenClaw 的 Skills 中添加：

```javascript
// 当检测到新成员加入
if (message.new_chat_members) {
  const welcomeMsg = `欢迎 @${message.from.username} 加入！
我是 AI 助手，有问题随时 @我`;
  sendMessage(welcomeMsg);
}
```

### 2️⃣ 自动踢广告

检测到广告关键词，自动删除消息并踢人。

**配置方法：**

```javascript
const adKeywords = ['加微信', '代购', '兼职', '赚钱'];
if (adKeywords.some(kw => message.text.includes(kw))) {
  deleteMessage(message.message_id);
  kickUser(message.from.id);
}
```

### 3️⃣ 定时公告

每天早上 9 点自动发群公告。

**使用 OpenClaw Cron：**

```bash
openclaw cron add "0 9 * * *" "telegram broadcast '早安！今天是新的一天'"
```

### 4️⃣ 多群同步

一条消息推送到所有群。

**配置方法：**

```json
{
  "telegram": {
    "broadcastGroups": ["-100123456789", "-100987654321"]
  }
}
```

然后使用：

```bash
openclaw telegram broadcast "重要通知：服务器维护"
```

---

## ❓ 常见问题

**Q: 机器人不回复消息？**

检查以下几点：
- Token 是否正确配置
- OpenClaw 是否正常启动
- 机器人是否被群组禁言

**Q: 群里 @机器人 没反应？**

确保：
- 机器人有读取消息的权限
- 群组隐私模式已关闭（BotFather 中设置）

**Q: 如何获取群组 ID？**

把机器人拉进群，发送一条消息，然后访问：

```
https://api.telegram.org/botYOUR_TOKEN/getUpdates
```

在返回的 JSON 中找到 `chat.id`。

---

## 💡 实用技巧

**1. 设置机器人命令**

在 BotFather 中发送 `/setcommands`，然后输入：

```
start - 开始对话
help - 获取帮助
status - 查看状态
```

用户输入 `/` 时会自动提示这些命令。

**2. 设置机器人头像**

在 BotFather 中发送 `/setuserpic`，然后上传图片。

**3. 设置机器人描述**

在 BotFather 中发送 `/setdescription`，输入机器人简介。

---

## 📊 效果对比

| 场景 | 手动管理 | AI Bot 管理 |
|------|---------|------------|
| 回复新人问题 | 1-5 分钟 | **即时** |
| 踢广告机器人 | 需要在线 | **自动** |
| 发送群公告 | 手动复制粘贴 | **一键推送** |
| 多群同步 | 逐个发送 | **同时推送** |

---

## 🚀 下一步

现在你已经拥有了一个 Telegram AI Bot，可以：

- **接入更多模型**：切换到 Claude、GPT-4 获得更好效果
- **添加自定义 Skills**：写脚本扩展功能
- **对接其他平台**：同时接入微信、Discord

明天教你如何在 Slack 里搭建 AI 编程助手，让你的团队协作效率翻倍！

---

如果这篇文章对你有帮助，欢迎 **点赞、在看、转发** 三连支持！

有任何问题，欢迎在评论区留言，我会一一回复。

明天见 👋
