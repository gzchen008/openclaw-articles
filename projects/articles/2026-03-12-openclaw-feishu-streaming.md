# OpenClaw 飞书流式输出：三条命令搞定，告别等待焦虑

> 之前飞书回复总是"等很久 → 突然蹦出一大段"，现在终于可以像 ChatGPT 一样逐字显示了！

---

## 😫 之前的痛点

你有没有遇到过这种情况：

在飞书里问 AI 一个问题，然后盯着屏幕等了 30 秒...

**突然！** 一大段文字蹦出来，吓你一跳。

这就是 **非流式输出** 的体验：

- ❌ 等待时间长，不知道 AI 在干嘛
- ❌ 突然出现一大段，阅读体验差
- ❌ 没有"正在思考"的反馈感

**流式输出** 的体验是这样的：

- ✅ 文字逐字出现，像真人在打字
- ✅ 可以边看边理解，不用等完整回复
- ✅ 有"正在生成"的即时反馈

---

## 🎯 三条命令启用流式输出

### Step 1：确认插件版本

```bash
openclaw plugins list | grep feishu
```

确保版本 ≥ 2026.3.8（流式输出是这个版本新增的）

### Step 2：编辑配置文件

打开 `~/.openclaw/openclaw.json`，找到飞书配置：

```json
{
  "channels": {
    "feishu": {
      "accounts": {
        "default": {
          "appId": "YOUR_APP_ID",
          "appSecret": "YOUR_APP_SECRET",
          "streaming": true,
          "renderMode": "card"
        }
      }
    }
  }
}
```

**关键配置**：
- `"streaming": true` — 启用流式输出
- `"renderMode": "card"` — 使用卡片模式（流式输出需要）

### Step 3：重启 Gateway

```bash
openclaw gateway restart
```

完成！现在飞书回复就是流式的了。

---

## 🔧 技术原理

### 为什么之前不能流式？

飞书 API 有**速率限制**，频繁更新消息容易触发限流。所以之前的实现是：

```
AI 生成完整回复 → 一次性发送 → 用户等待 30 秒
```

### 现在是怎么实现的？

OpenClaw 使用飞书 **CardKit API** 的 `streaming_mode`：

```
创建流式卡片 → 逐字更新内容 → 完成后关闭流式模式
```

### 核心代码

```typescript
// 1. 创建流式卡片
const cardJson = {
  schema: "2.0",
  config: {
    streaming_mode: true,  // 关键！
    streaming_config: {
      print_frequency_ms: { default: 50 },  // 50ms 更新一次
      print_step: { default: 2 }
    }
  },
  body: {
    elements: [{ tag: "markdown", content: "Thinking..." }]
  }
};

// 2. 发送卡片
await client.im.message.create({
  params: { receive_id_type: "chat_id" },
  data: { receive_id: chatId, msg_type: "interactive", content: cardContent }
});

// 3. 流式更新内容
await fetch(`${apiBase}/cardkit/v1/cards/${cardId}/elements/content/content`, {
  method: "PUT",
  body: JSON.stringify({ content: newText, sequence: sequence++ })
});

// 4. 完成后关闭流式模式
await fetch(`${apiBase}/cardkit/v1/cards/${cardId}/settings`, {
  method: "PATCH",
  body: JSON.stringify({
    settings: JSON.stringify({
      config: { streaming_mode: false }
    })
  })
});
```

---

## 📊 对比效果

| 特性 | 非流式 | 流式 |
|------|--------|------|
| 等待体验 | 盯着空白等 30s | 立即看到文字出现 |
| 阅读体验 | 突然一大段 | 逐字显示，边看边理解 |
| 反馈感 | 不知道 AI 在干嘛 | 明显感到"正在生成" |
| API 调用 | 1 次 | N 次（但有节流保护） |

---

## ⚠️ 注意事项

### 1. 必须使用卡片模式

流式输出需要 `renderMode: "card"`，因为它是基于 CardKit API 实现的。

```json
{
  "renderMode": "card",
  "streaming": true
}
```

### 2. 有节流保护

为了避免触发飞书 API 限流，OpenClaw 内置了节流机制：

- 最小更新间隔：100ms
- 智能合并：相同内容不重复更新
- 自动降级：如果流式失败，自动回退到普通模式

### 3. 群聊也支持

流式输出在私聊和群聊都能用，只要配置正确。

---

## 🎉 总结

**之前**：等 30 秒 → 突然蹦出一大段 → 吓一跳

**现在**：立即开始 → 逐字显示 → 像真人在打字

三条命令搞定：

```bash
# 1. 确认版本
openclaw plugins list | grep feishu

# 2. 编辑配置（添加 streaming: true）

# 3. 重启
openclaw gateway restart
```

---

如果觉得有用，点个"在看"吧 👇
