# OpenClaw Agent Loop：从消息到回复的完整旅程

> 你发给 AI 的一条消息，在 OpenClaw 内部经历了什么？
>
> 本文将带你深入 Agent Loop 的每一个环节，理解 AI Agent 如何思考、执行工具、流式输出。

---

## 🎯 什么是 Agent Loop？

**Agent Loop（智能体循环）** 是 OpenClaw 的核心执行流程。

简单来说，它是从 **"接收用户消息"** 到 **"返回 AI 回复"** 的完整路径：

```
消息接收 → 上下文组装 → 模型推理 → 工具执行 → 流式输出 → 持久化
```

这个过程不是简单的"一发一回"，而是：

- 🔄 **串行执行**：同一会话的多次请求会排队，避免冲突
- 🛠️ **工具调用**：AI 可以执行工具（读文件、发消息、控制设备）
- 🌊 **流式输出**：回复不是等 AI 想完才发，而是一字一字地流式返回
- 💾 **状态持久化**：对话历史自动保存，下次继续

---

## 🏗️ Agent Loop 的 8 个步骤

从用户发送消息到 AI 返回回复，OpenClaw 会经历 8 个核心步骤：

### 步骤 1：入口层（Entry Point）

**📥 用户消息到达**

- 来源：WhatsApp / Telegram / Discord / iMessage / Feishu
- 方式：Gateway RPC（异步）或 CLI agent（同步）
- 特点：立即返回 runId，不阻塞

### 步骤 2：会话准备（Session Prep）

**🔧 准备运行环境**

- 解析 sessionKey，找到对应会话
- 加载当前激活的 Skills（技能快照）
- 注入引导文件：AGENTS.md / SOUL.md / MEMORY.md
- 获取会话写锁，防止并发冲突

### 步骤 3：队列控制（Queue）

**⏳ 请求排队等待**

- Session Lane：同一会话的请求串行执行
- Global Lane：控制整体并发数
- 目的：避免工具冲突、会话历史错乱

### 步骤 4：Prompt 组装（Prompt Assembly）

**📝 构建系统提示**

4 层结构：
1. 基础提示：你是 OpenClaw AI 助手 + 工具调用规范
2. Skills 提示：当前激活的技能列表
3. 引导上下文：AGENTS.md / SOUL.md / MEMORY.md
4. 对话历史：之前的所有对话（自动压缩）

### 步骤 5：模型推理（Model Inference）

**🤖 AI 开始思考**

- 运行时：pi-agent-core（嵌入式 Agent 运行时）
- 模型支持：OpenAI / Claude / Gemini / GLM / Kimi（20+ 模型）
- Fallback：首选模型失败，自动降级到备选模型
- 模式：Thinking（深度思考）/ Verbose（详细输出）

### 步骤 6：工具执行（Tool Execution）

**🛠️ AI 调用工具完成任务**

- 触发条件：AI 决定需要查天气、读文件、发消息等
- 执行流程：工具 start → update → end
- 结果处理：大小限制、图片压缩、消息去重

### 步骤 7：流式输出（Streaming）

**🌊 一字一字返回结果**

3 种事件流：
- assistant：助手文字增量（一字一字显示）
- tool：工具执行进度（透明展示）
- lifecycle：生命周期（start/end/error）

### 步骤 8：回复整形 + 持久化

**💾 保存对话历史**

- 组装最终回复：文本 + 工具结果 + 媒体
- 过滤静默令牌：NO_REPLY 不发送
- 写入会话记录：持久化到存储
- 释放会话锁：允许下一个请求执行

---

## 🔍 详细流程拆解

### 1️⃣ 入口层（Entry Point）

Agent Loop 有两个入口：

#### Gateway RPC（推荐）

```json
{
  "method": "agent",
  "params": {
    "sessionKey": "agent:main:main",
    "message": "帮我写一篇关于 AI Agent 的文章"
  }
}
```

**响应**（立即返回）：

```json
{
  "runId": "run_abc123",
  "acceptedAt": "2026-03-10T07:00:00Z"
}
```

- ✅ **异步执行**：立即返回 `runId`，不阻塞
- 📊 **状态查询**：用 `agent.wait` 等待完成

#### CLI 命令

```bash
openclaw agent "帮我写一篇文章"
```

- ✅ **同步执行**：等待完成后返回结果
- 🔧 **调试友好**：适合测试和开发

---

### 2️⃣ 会话准备（Session Prep）

在真正执行前，OpenClaw 会准备会话环境：

#### Step 1: 解析会话

```typescript
// 根据 sessionKey 找到对应的会话
const session = await resolveSession({
  sessionKey: "agent:main:main",
  sessionId: "abc123"  // 可选
});
```

#### Step 2: 加载 Skills

```typescript
// 加载当前激活的所有技能
const skills = await loadSkillsSnapshot();

// 示例：加载的技能
// - feishu-doc (飞书文档)
// - github (GitHub 操作)
// - weather (天气查询)
```

#### Step 3: 解析引导文件

```typescript
// 注入上下文文件
const bootstrapFiles = [
  "AGENTS.md",      // Agent 身份定义
  "SOUL.md",        // 人格设定
  "USER.md",        // 用户信息
  "MEMORY.md",      // 长期记忆
  "TOOLS.md"        // 工具说明
];
```

#### Step 4: 获取写锁

```typescript
// 防止并发写入冲突
await sessionWriteLock.acquire();
```

---

### 3️⃣ 队列控制（Queue）

#### 为什么需要队列？

**问题场景**：用户快速发送 3 条消息

```
用户: 帮我查天气
用户: 然后查 GitHub issues
用户: 再发个飞书通知
```

如果没有队列，3 个请求会同时执行：
- ❌ 工具冲突（同时写文件）
- ❌ 会话历史错乱
- ❌ 回复顺序混乱

#### 解决方案：双层队列

```
┌─────────────────────────────────────────────────┐
│              Global Lane (全局通道)              │
│  控制整体并发数（例如：最多 5 个会话同时执行）     │
└─────────────────┬───────────────────────────────┘
                  │
                  ↓
┌─────────────────────────────────────────────────┐
│          Session Lane (会话通道)                 │
│  同一会话的请求串行执行                           │
│                                                  │
│  Session A: [请求1] → [请求2] → [请求3]         │
│  Session B: [请求1] → [请求2]                   │
│  Session C: [请求1]                             │
└─────────────────────────────────────────────────┘
```

**效果**：
- ✅ Session A 的 3 个请求按顺序执行
- ✅ Session A/B/C 可以并行（受全局并发限制）
- ✅ 避免工具冲突和会话错乱

---

### 4️⃣ Prompt 组装（Prompt Assembly）

OpenClaw 的系统提示由多个部分组成：

```
┌─────────────────────────────────────────────────┐
│           OpenClaw System Prompt                │
├─────────────────────────────────────────────────┤
│  1. 基础提示 (Base Prompt)                      │
│     • 你是 OpenClaw AI 助手                      │
│     • 工具调用规范                                │
│     • 安全准则                                    │
├─────────────────────────────────────────────────┤
│  2. Skills 提示                                  │
│     • 当前激活的技能列表                          │
│     • 每个技能的说明和用法                        │
├─────────────────────────────────────────────────┤
│  3. 引导上下文 (Bootstrap Context)              │
│     • AGENTS.md (身份定义)                       │
│     • SOUL.md (人格设定)                         │
│     • USER.md (用户信息)                         │
│     • MEMORY.md (长期记忆)                       │
├─────────────────────────────────────────────────┤
│  4. 对话历史 (Transcript)                       │
│     • 之前的所有对话                              │
│     • 自动压缩（超出 token 限制时）              │
└─────────────────────────────────────────────────┘
```

#### Token 限制

```typescript
// 不同模型的 token 限制
const MODEL_LIMITS = {
  "gpt-4": 8192,
  "gpt-4-turbo": 128000,
  "claude-3-opus": 200000,
  "glm-4": 128000
};

// 预留空间给回复
const RESERVE_TOKENS = 4096;

// 如果超限，触发自动压缩
if (totalTokens > modelLimit - RESERVE_TOKENS) {
  await triggerCompaction();
}
```

---

### 5️⃣ 模型推理（Model Inference）

OpenClaw 使用 **pi-agent-core** 作为嵌入式 Agent 运行时：

```typescript
// runEmbeddedPiAgent 的核心逻辑
async function runEmbeddedPiAgent(params) {
  // 1. 解析模型 + 认证
  const model = await resolveModel(params.model);
  const authProfile = await getAuthProfile(model.provider);

  // 2. 构建 pi session
  const piSession = await buildPiSession({
    model,
    systemPrompt,
    tools,
    timeout: params.timeoutSeconds * 1000
  });

  // 3. 订阅事件流
  subscribeToPiEvents(piSession, (event) => {
    if (event.type === "assistant_delta") {
      emit("assistant", event.delta);
    }
    if (event.type === "tool_call") {
      emit("tool", event);
    }
  });

  // 4. 执行推理
  const result = await piSession.run();

  return {
    payloads: result.messages,
    usage: result.usage
  };
}
```

#### 多模型 Fallback

```typescript
// 模型降级链
const MODEL_FALLBACK_CHAIN = [
  "zai/glm-5",        // 首选
  "zai/glm-4.7",      // 备选 1
  "kimi-coding/k2p5"  // 备选 2
];

// 如果首选模型失败，自动尝试下一个
for (const model of MODEL_FALLBACK_CHAIN) {
  try {
    return await callModel(model, prompt);
  } catch (error) {
    console.log(`Model ${model} failed, trying next...`);
  }
}
```

---

### 6️⃣ 工具执行（Tool Execution）

当 AI 决定调用工具时：

```
AI 思考: "我需要查一下天气，调用 weather skill"
  ↓
工具调用: { name: "weather", params: { city: "北京" } }
  ↓
工具执行: weather skill 查询天气 API
  ↓
工具结果: { temperature: "15°C", condition: "晴" }
  ↓
AI 继续思考: "好的，我现在知道天气了，可以回复用户"
```

#### 工具事件流

```jsonl
{"stream": "tool", "event": "start", "tool": "weather", "callId": "call_123"}
{"stream": "tool", "event": "update", "tool": "weather", "status": "查询 API..."}
{"stream": "tool", "event": "end", "tool": "weather", "result": {...}}
```

#### 工具结果清理

```typescript
// 防止工具结果过大
function sanitizeToolResult(result) {
  // 1. 限制大小
  if (result.length > 100000) {
    result = result.substring(0, 100000) + "...(truncated)";
  }

  // 2. 处理图片
  if (result.images) {
    result.images = result.images.map(compressImage);
  }

  return result;
}
```

---

### 7️⃣ 流式输出（Streaming）

OpenClaw 支持 3 种流式事件：

#### Assistant Stream（助手增量）

```jsonl
{"stream": "assistant", "delta": "今天"}
{"stream": "assistant", "delta": "北京"}
{"stream": "assistant", "delta": "的天气"}
{"stream": "assistant", "delta": "是 15°C，晴天"}
```

- 🌊 **实时流式**：一字一字返回，不等 AI 想完
- 📱 **聊天体验**：用户看到"正在输入..."效果

#### Tool Stream（工具事件）

```jsonl
{"stream": "tool", "event": "start", "tool": "github"}
{"stream": "tool", "event": "update", "status": "查询 issues..."}
{"stream": "tool", "event": "end", "result": {...}}
```

- 🔧 **透明执行**：用户看到工具执行进度
- 🐛 **调试友好**：出错时容易定位

#### Lifecycle Stream（生命周期）

```jsonl
{"stream": "lifecycle", "phase": "start", "runId": "run_123"}
{"stream": "lifecycle", "phase": "end", "runId": "run_123"}
```

- ✅ **状态管理**：标记任务开始/结束
- ⏱️ **超时控制**：配合 `agent.wait` 使用

---

### 8️⃣ 回复整形 + 持久化

#### 回复整形

```typescript
function shapeReply(payloads) {
  // 1. 过滤 NO_REPLY
  payloads = payloads.filter(p => p.text !== "NO_REPLY");

  // 2. 去重消息工具
  payloads = deduplicateMessagingTools(payloads);

  // 3. 如果没有可渲染内容，且工具有错
  if (payloads.length === 0 && toolError) {
    payloads.push({
      type: "text",
      text: `❌ 工具执行失败: ${toolError.message}`
    });
  }

  return payloads;
}
```

#### 持久化

```typescript
// 写入会话记录
await sessionManager.append({
  role: "user",
  content: userMessage
});

await sessionManager.append({
  role: "assistant",
  content: assistantReply,
  toolCalls: [...],
  toolResults: [...]
});
```

---

## 🪝 Hook 系统：在哪里拦截？

OpenClaw 提供了两套 Hook 系统，让你可以在关键节点插入自定义逻辑：

### 1. 内部 Hook（Gateway Hooks）

运行在 Gateway 内部，用于命令和生命周期事件：

| Hook 事件 | 触发时机 | 用途 |
|----------|---------|------|
| `command:new` | 用户发送 `/new` | 保存会话快照 |
| `command:reset` | 用户发送 `/reset` | 清理临时文件 |
| `command:stop` | 用户发送 `/stop` | 记录中止原因 |
| `agent:bootstrap` | 构建引导文件时 | 动态注入上下文 |
| `gateway:startup` | Gateway 启动时 | 初始化任务 |

#### 示例：session-memory Hook

```typescript
// 当用户发送 /new 时，保存会话到 memory/ 目录
const handler: HookHandler = async (event) => {
  if (event.action !== "new") return;

  // 提取最后 15 行对话
  const transcript = await loadTranscript(event.sessionKey);
  const lastLines = transcript.slice(-15);

  // 生成文件名
  const slug = await generateSlug(lastLines);
  const filename = `memory/${date}-${slug}.md`;

  // 保存
  await writeFile(filename, lastLines);
};
```

### 2. 插件 Hook（Plugin Hooks）

运行在 Agent 循环内部，更细粒度的控制：

| Hook 事件 | 触发时机 | 用途 |
|----------|---------|------|
| `before_agent_start` | Agent 运行前 | 注入上下文、覆盖 prompt |
| `agent_end` | Agent 完成后 | 审计日志、质量检查 |
| `before_tool_call` | 工具调用前 | 参数验证、权限检查 |
| `after_tool_call` | 工具调用后 | 结果转换、错误处理 |
| `tool_result_persist` | 工具结果持久化前 | 敏感信息过滤 |
| `before_compaction` | 上下文压缩前 | 选择性保留重要内容 |

#### 示例：敏感信息过滤 Hook

```typescript
// 在工具结果写入会话前，过滤敏感信息
const hook: PluginHook = {
  event: "tool_result_persist",
  handler: (result) => {
    // 过滤 API Key
    result.content = result.content.replace(
      /sk-[a-zA-Z0-9]{48}/g,
      "sk-***REDACTED***"
    );

    // 过滤手机号
    result.content = result.content.replace(
      /\+86\d{11}/g,
      "+86***REDACTED***"
    );

    return result;
  }
};
```

---

## 🔄 压缩与重试（Compaction + Retry）

### 为什么需要压缩？

**问题**：对话历史越来越长，超出模型 token 限制

```
Session 开始: 500 tokens
对话 10 轮后: 8000 tokens
对话 50 轮后: 40000 tokens ❌ 超限！
```

### 压缩策略

OpenClaw 使用 **summarization** 压缩：

```typescript
async function compactTranscript(transcript) {
  // 1. 保留最近的对话（不压缩）
  const recent = transcript.slice(-10);

  // 2. 压缩旧对话
  const old = transcript.slice(0, -10);
  const summary = await summarize(old);

  // 3. 组合
  return [
    { role: "system", content: `历史摘要: ${summary}` },
    ...recent
  ];
}
```

### 重试机制

压缩后会触发重试：

```typescript
if (needsCompaction) {
  // 1. 发出压缩事件
  emit("compaction", { phase: "start" });

  // 2. 执行压缩
  await compactTranscript();

  // 3. 重置内存缓冲（避免重复输出）
  resetBuffers();

  // 4. 重试
  await retryAgentRun();
}
```

---

## ⏱️ 超时控制

### 两层超时

#### 1. `agent.wait` 超时（等待阶段）

```typescript
// 默认 30 秒
const result = await agent.wait({
  runId: "run_123",
  timeoutMs: 30000  // 可自定义
});

// 超时返回
{
  status: "timeout",
  startedAt: "2026-03-10T07:00:00Z",
  endedAt: null
}
```

**注意**：这只影响等待，不会中止 Agent 运行。

#### 2. Agent 运行时超时

```typescript
// 配置默认超时（10 分钟）
{
  "agents": {
    "defaults": {
      "timeoutSeconds": 600
    }
  }
}
```

超时后，Agent 会被强制中止：

```typescript
// 在 runEmbeddedPiAgent 中
const abortTimer = setTimeout(() => {
  abortController.abort();
}, timeoutSeconds * 1000);
```

---

## 🚨 可能提前结束的情况

Agent Loop 可能在以下情况提前终止：

| 情况 | 原因 | 后果 |
|-----|------|------|
| **Agent 超时** | 运行超过 `timeoutSeconds` | 中止运行，返回错误 |
| **AbortSignal** | 用户发送 `/stop` | 立即停止，保存状态 |
| **Gateway 断开** | 网络问题 / 服务重启 | 连接丢失，可能丢失未保存数据 |
| **RPC 超时** | Gateway RPC 调用超时 | 返回超时错误 |
| **模型错误** | API 错误 / 限流 | 触发 Fallback 或返回错误 |

---

## 📊 实战案例：一次完整的 Agent Loop

让我们看一个完整例子：

### 用户输入

```
用户（Telegram）: 帮我查一下北京天气，然后发个飞书通知
```

### 完整流程

```
1️⃣ 入口层
   - Telegram 消息到达 Gateway
   - 触发 agent RPC
   - 返回 { runId: "run_abc", acceptedAt: "..." }

2️⃣ 会话准备
   - 解析 sessionKey: "agent:main:telegram:+86188..."
   - 加载 Skills: [weather, feishu-doc, feishu-drive]
   - 注入 MEMORY.md（用户偏好：喜欢简洁回复）

3️⃣ 队列控制
   - Session Lane: 等待前一个请求完成
   - Global Lane: 当前 3 个并发，未超限

4️⃣ Prompt 组装
   - 基础提示 + Skills 提示 + MEMORY.md + 对话历史
   - 总 tokens: 3200（未超限）

5️⃣ 模型推理
   - 首选模型: zai/glm-5
   - AI 思考: 需要调用 weather 工具

6️⃣ 工具执行 #1
   - 工具: weather
   - 参数: { city: "北京" }
   - 结果: { temperature: "15°C", condition: "晴" }

7️⃣ 流式输出 #1
   - assistant delta: "北京今天天气不错，"
   - assistant delta: "气温 15°C，晴天。"

8️⃣ 工具执行 #2
   - 工具: feishu-message
   - 参数: { chat: "user:ou_xxx", message: "北京天气：15°C，晴" }
   - 结果: { success: true }

9️⃣ 流式输出 #2
   - tool event: "已发送飞书通知 ✅"

🔟 回复整形 + 持久化
   - 组装最终回复: "北京今天天气不错，气温 15°C，晴天。\n\n已发送飞书通知 ✅"
   - 写入会话记录
   - 释放会话锁

✅ 完成
   - 发送 lifecycle end 事件
   - Telegram 返回最终回复
```

### 最终用户看到的

```
AI: 北京今天天气不错，气温 15°C，晴天。

已发送飞书通知 ✅
```

---

## 🎓 总结：Agent Loop 的设计哲学

### 1. 串行化保证一致性

- 同一会话的请求串行执行
- 避免工具冲突和状态错乱
- 对话历史始终一致

### 2. 流式输出提升体验

- 不等 AI 想完才回复
- 一字一字流式返回
- 用户感知"正在思考"

### 3. Hook 系统提供扩展性

- 关键节点可拦截
- 自定义逻辑注入
- 不修改核心代码

### 4. 多层容错机制

- 模型 Fallback 降级
- 超时自动中止
- 压缩避免超限
- 错误优雅降级

---

## 🔗 相关文档

- [OpenClaw 整体架构解析](./2026-03-09-openclaw-architecture-guide.md)（第 1 篇）
- [Session 管理与上下文工程](#)（第 4 篇，即将发布）
- [多模型支持与 Fallback 机制](#)（第 3 篇，即将发布）

---

## 💡 思考题

1. **为什么 Agent Loop 需要双层队列（Session + Global）？单层队列不够吗？**
2. **如果工具执行时间很长（例如 5 分钟），会如何影响 Agent Loop？**
3. **如何设计一个 Hook，在每次工具调用前验证用户权限？**

---

**下一篇预告**：OpenClaw 如何支持 20+ AI 模型？多模型架构设计

我们将深入探讨：
- 模型路由机制
- Fallback 降级策略
- Provider 限流与 cooldown
- 成本优化技巧

---

*作者：小J | 发布日期：2026-03-10*
