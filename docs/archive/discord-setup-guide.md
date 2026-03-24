# OpenClaw 配置 Discord Bot 完整教程

## 前言

OpenClaw 是一个强大的 AI 助手网关，可以让你在各种聊天平台上与 AI 助手交互。本文将详细介绍如何在 OpenClaw 中配置 Discord 频道，让你的 AI 助手能够在 Discord 服务器中响应消息。

---

## 一、准备工作

### 1. 创建 Discord Bot

1. 访问 [Discord 开发者门户](https://discord.com/developers/applications)
2. 点击 **New Application**，输入应用名称
3. 进入 **Bot** 页面，点击 **Add Bot**
4. 复制 **Token**（重要，妥善保存）

### 2. 启用必要权限

在 Bot 页面，找到 **Privileged Gateway Intents**，开启以下选项：
- ✅ **MESSAGE CONTENT INTENT**（必须，用于读取消息内容）

### 3. 邀请 Bot 加入服务器

1. 进入 **OAuth2 → URL Generator**
2. 勾选 `bot` 和 `applications.commands`
3. 选择 Bot 权限（建议：Send Messages, Read Messages, Read Message History）
4. 复制生成的链接，在浏览器中打开并选择服务器邀请

---

## 二、OpenClaw 配置步骤

### 1. 编辑配置文件

打开 OpenClaw 配置文件：

```bash
~/.openclaw/openclaw.json
```

### 2. 配置 Discord 频道

在 `channels` 部分添加 Discord 配置：

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN_HERE",
      "allowBots": true,
      "groupPolicy": "allowlist",
      "actions": {
        "channelInfo": true,
        "channels": true
      },
      "guilds": {
        "YOUR_GUILD_ID": {
          "channels": {
            "general": {
              "allow": true
            }
          }
        }
      }
    }
  }
}
```

### 3. 配置项说明

| 配置项 | 说明 |
|--------|------|
| `enabled` | 是否启用 Discord 频道 |
| `token` | Discord Bot Token |
| `allowBots` | 是否接收其他 Bot 的消息 |
| `groupPolicy` | 服务器策略：`allowlist`（白名单）/ `all`（所有）/ `denylist`（黑名单）|
| `guilds` | 允许访问的服务器列表 |

### 4. 获取服务器和频道信息

**服务器 ID（Guild ID）：**
- 在 Discord 中右键点击服务器名称
- 开启开发者模式：设置 → 高级 → 开发者模式
- 点击"复制服务器 ID"

**频道名称：**
- 使用频道的实际名称（如 `general`、`general-chat` 等）

---

## 三、用户配对授权

首次在 Discord 中使用 OpenClaw 时，需要进行用户配对：

1. 在 Discord 频道中发送任意消息
2. Bot 会回复配对码，例如：
   ```
   Pairing code: KSKLHWSB
   Ask the bot owner to approve with: 
   openclaw pairing approve discord <code>
   ```

3. 在终端中执行批准命令：
   ```bash
   openclaw pairing approve discord KSKLHWSB
   ```
   
   或使用 npx：
   ```bash
   npx openclaw pairing approve discord KSKLHWSB
   ```

4. 批准后，用户即可正常使用

---

## 四、重启 Gateway

配置更改后，需要重启 OpenClaw Gateway 才能生效：

```bash
openclaw gateway restart
```

或手动重启：
```bash
pkill -f openclaw-gateway
openclaw gateway start
```

---

## 五、常见问题排查

### 1. Bot 不回复消息

**检查清单：**
- [ ] Message Content Intent 已启用
- [ ] Bot Token 正确无误
- [ ] Bot 已加入服务器
- [ ] Bot 有发送/读取消息权限
- [ ] 用户已完成配对授权
- [ ] Gateway 已重启

### 2. 频道名称不匹配

确保配置中的频道名称与实际频道名称完全一致（区分大小写）。

### 3. 权限不足

在 Discord 服务器设置中，检查 Bot 角色的权限：
- View Channels
- Send Messages
- Read Message History
- Embed Links

---

## 六、高级配置

### 1. 允许多个频道

```json
"guilds": {
  "YOUR_GUILD_ID": {
    "channels": {
      "general": { "allow": true },
      "random": { "allow": true },
      "ai-chat": { "allow": true }
    }
  }
}
```

### 2. 允许所有服务器

将 `groupPolicy` 改为 `all`：

```json
"groupPolicy": "all",
"guilds": {}
```

### 3. 添加更多操作权限

```json
"actions": {
  "channelInfo": true,
  "channels": true,
  "channelCreate": true,
  "channelDelete": false
}
```

---

## 七、总结

配置 OpenClaw 的 Discord 频道主要包括以下步骤：

1. ✅ 创建 Discord Bot 并获取 Token
2. ✅ 启用 Message Content Intent
3. ✅ 邀请 Bot 加入服务器
4. ✅ 编辑 OpenClaw 配置文件
5. ✅ 重启 Gateway
6. ✅ 完成用户配对

配置完成后，你就可以在 Discord 中随时随地与 AI 助手交互了！

---

## 参考链接

- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Discord 开发者门户](https://discord.com/developers/applications)
- [Discord Bot 权限计算器](https://discordapi.com/permissions.html)

---

*本文基于 OpenClaw 2026.1.30 版本编写*
