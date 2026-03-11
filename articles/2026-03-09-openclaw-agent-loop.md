# OpenClaw Agent Loop：从消息到回复的完整旅程

> 本文是 OpenClaw 源码解读系列的第 2 篇，将深入剖析 AI Agent 的执行流程。

---

## 🎯 什么是 Agent Loop？

当你向 OpenClaw 发送一条消息："帮我写一个 Python 爬虫"，从消息发出到收到回复，中间经历了什么？

**Agent Loop 就是这个完整的执行流程**：
1. 📥 **接收消息**（Intake）
2. 🧩 **组装上下文**（Context Assembly）
3. 🤖 **模型推理**（Model Inference）
4. 🛠️ **工具执行**（Tool Execution）
5. 🚀 **流式输出**（Streaming）
6. 💾 **持久化**（Persistence）

这个循环是 OpenClaw 的核心，它将一条消息转换为具体的行动和最终回复，同时保持会话状态的一致性。

---

## 🔄 Agent Loop 生命周期

### 完整流程图

```
┌──────────────────────────────────────────────────────┐
│ 1. 消息接收 (Intake)                                  │
│    - Gateway RPC: agent / agent.wait                │
│    - CLI: openclaw agent --message "xxx"            │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 2. 参数验证与 Session 解析                            │
│    - 验证 params (message, sessionKey, model 等)     │
│    - 解析 sessionKey/sessionId                       │
│    - 持久化 session metadata                         │
│    - 返回 { runId, acceptedAt }                      │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 3. 模型选择与配置                                     │
│    - 解析 model + thinking/verbose defaults          │
│    - 加载 skills snapshot                            │
│    - 准备 agent 环境                                  │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 4. Prompt 组装                                        │
│    - 加载 system prompt                               │
│    - 加载 skills prompt                               │
│    - 加载 bootstrap context                           │
│    - 加载 session history                             │
│    - 应用 hooks (before_prompt_build)                │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 5. 模型推理 (Model Inference)                         │
│    - 调用 AI 模型 (OpenAI/Claude/Gemini 等)          │
│    - 流式输出 assistant deltas                        │
│    - 流式输出 tool events                             │
│    - 流式输出 lifecycle events                        │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 6. 工具执行 (Tool Execution)                          │
│    - 解析 tool calls                                  │
│    - 执行 tools (read/write/exec 等)                  │
│    - 返回 tool results                                │
│    - 循环执行直到模型停止调用 tools                    │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 7. 流式输出 (Streaming)                               │
│    - 发送 assistant deltas                            │
│    - 发送 tool events                                 │
│    - 发送 lifecycle events                            │
│    - 组装最终回复                                      │
└───────────────────┬──────────────────────────────────┘
                    │
                    ↓
┌──────────────────────────────────────────────────────┐
│ 8. 持久化 (Persistence)                               │
│    - 保存 session history                             │
│    - 保存 tool results                                │
│    - 保存 usage metadata                              │
│    - 发送 lifecycle end event                         │
└──────────────────────────────────────────────────────┘
```

### 关键步骤详解

#### 1. 消息接收（Intake）

**入口点**：
- **Gateway RPC**: `agent` 和 `agent.wait`
- **CLI**: `openclaw agent --message "xxx"`

**RPC 请求示例**：
```json
{
  "type": "req",
  "id": "req-uuid-123",
  "method": "agent",
  "params": {
    "message": "帮我写一个 Python 爬虫",
    "sessionKey": "user:123456",
    "model": "zai/glm-5",
    "thinking": "high"
  }
}
```

**RPC 响应**（立即返回）：
```json
{
  "type": "res",
  "id": "req-uuid-123",
  "ok": true,
  "payload": {
    "runId": "run-uuid-456",
    "acceptedAt": "2026-03-09T12:00:00Z"
  }
}
```

**关键点**：
- ✅ RPC 立即返回 `runId`，不等待 Agent 执行完成
- ✅ Agent 在后台异步执行
- ✅ 客户端可以通过 `agent.wait` 等待完成

---

#### 2. 参数验证与 Session 解析

**验证参数**：
```javascript
// 验证必填参数
if (!params.message) {
  throw new Error('message is required');
}

// 验证 sessionKey
if (!params.sessionKey && !params.sessionId) {
  throw new Error('sessionKey or sessionId is required');
}
```

**解析 Session**：
```javascript
// 解析 sessionKey
const sessionKey = params.sessionKey || `user:${params.sessionId}`;

// 持久化 session metadata
await sessionManager.updateMetadata(sessionKey, {
  lastMessageAt: Date.now(),
  messageCount: (session.messageCount || 0) + 1
});
```

---

#### 3. 模型选择与配置

**模型解析**：
```javascript
// 解析模型
const model = params.model || config.defaults.model || 'zai/glm-5';

// 解析 thinking/verbose
const thinking = params.thinking || config.defaults.thinking || 'low';
const verbose = params.verbose || config.defaults.verbose || false;

// 加载 skills snapshot
const skills = await skillLoader.loadSnapshot();
```

**模型配置示例**：
```javascript
{
  model: 'zai/glm-5',
  thinking: 'high',  // 'low' | 'medium' | 'high'
  verbose: true,     // 是否显示详细日志
  timeoutSeconds: 600  // 超时时间（秒）
}
```

---

## 📊 队列机制：如何避免并发冲突？

### 问题场景

**如果没有队列机制**：
```
用户 A: "写一个爬虫"  → Agent 开始执行
用户 A: "读取文件"    → Agent 开始执行
                         ↑ 两个 Agent 同时修改 session，导致冲突！
```

### 队列设计

OpenClaw 使用 **两级队列** 来避免并发冲突：

#### 1. Session Lane（会话通道）

```javascript
// 每个 sessionKey 一个队列
const sessionLanes = new Map();

// 获取 session lane
function getSessionLane(sessionKey) {
  if (!sessionLanes.has(sessionKey)) {
    sessionLanes.set(sessionKey, new Queue());
  }
  return sessionLanes.get(sessionKey);
}

// 添加任务到 session lane
async function enqueueSession(sessionKey, task) {
  const lane = getSessionLane(sessionKey);
  await lane.add(task);
}
```

**效果**：
- ✅ 同一个 session 的任务按顺序执行
- ✅ 不同 session 的任务可以并发执行

#### 2. Global Lane（全局通道）

```javascript
// 全局队列（可选）
const globalLane = new Queue({ concurrency: 3 });

// 添加任务到 global lane
async function enqueueGlobal(task) {
  await globalLane.add(task);
}
```

**效果**：
- ✅ 限制全局并发数（避免资源耗尽）
- ✅ 可以控制整体负载

### 队列配置

```javascript
// session lane 配置
{
  sessionLane: {
    concurrency: 1,  // 每个 session 同时只能运行 1 个任务
    timeout: 600000   // 超时时间（毫秒）
  }
}

// global lane 配置
{
  globalLane: {
    concurrency: 3,  // 全局最多同时运行 3 个任务
    timeout: 600000
  }
}
```

### 队列流程图

```
┌──────────┐
│ 任务请求  │
└─────┬────┘
      │
      ↓
┌─────────────────┐
│ Session Lane    │ ← 同一 session 的任务排队
│ (Queue per key) │
└─────┬───────────┘
      │
      ↓
┌─────────────────┐
│ Global Lane     │ ← 全局任务排队（可选）
│ (Queue global)  │
└─────┬───────────┘
      │
      ↓
┌─────────────────┐
│ Agent 执行      │
└─────────────────┘
```

---

## 🎯 Hook 系统：如何扩展 Agent 能力？

### 什么是 Hook？

Hook 是在 Agent Loop 的特定阶段执行的扩展点，允许你在不修改核心代码的情况下扩展功能。

### Hook 类型

#### 1. before_model_resolve

**触发时机**：模型解析之前
**用途**：动态覆盖模型选择

```javascript
// 示例：根据时间选择不同的模型
registerHook('before_model_resolve', (context) => {
  const hour = new Date().getHours();
  
  if (hour >= 22 || hour < 6) {
    // 夜间使用便宜的模型
    context.model = 'zai/glm-4.7';
  } else {
    // 白天使用高质量模型
    context.model = 'zai/glm-5';
  }
});
```

#### 2. before_prompt_build

**触发时机**：Prompt 组装之前（已加载 session）
**用途**：注入动态上下文

```javascript
// 示例：注入当前时间
registerHook('before_prompt_build', (context) => {
  context.prependContext = `\n当前时间：${new Date().toLocaleString('zh-CN')}\n`;
  
  // 或者修改 system prompt
  context.systemPrompt = context.systemPrompt + '\n\n请注意：用户是技术背景，可以使用专业术语。';
});
```

#### 3. agent_end

**触发时机**：Agent 执行完成后
**用途**：记录日志、发送通知

```javascript
// 示例：记录 token 消耗
registerHook('agent_end', (context) => {
  const usage = context.usage;
  
  logger.info('Agent completed', {
    runId: context.runId,
    promptTokens: usage.promptTokens,
    completionTokens: usage.completionTokens,
    totalTokens: usage.totalTokens,
    duration: context.duration
  });
});
```

#### 4. before_tool_call / after_tool_call

**触发时机**：工具执行前后
**用途**：拦截工具调用

```javascript
// 示例：记录所有文件读取
registerHook('before_tool_call', (context) => {
  if (context.toolName === 'read') {
    logger.info('Reading file:', context.params.path);
  }
});

// 示例：过滤敏感信息
registerHook('after_tool_call', (context) => {
  if (context.toolName === 'read') {
    // 移除敏感信息
    context.result = context.result.replace(/API_KEY=.*/g, 'API_KEY=***');
  }
});
```

### Hook 执行流程

```
Agent Loop 开始
     │
     ├─→ before_model_resolve
     │      └─→ 覆盖模型选择
     │
     ├─→ 加载 Session
     │
     ├─→ before_prompt_build
     │      ├─→ prependContext（动态文本）
     │      ├─→ systemPrompt（系统提示）
     │      └─→ prependSystemContext（系统上下文）
     │
     ├─→ 模型推理
     │
     ├─→ before_tool_call
     │      └─→ 拦截工具调用
     │
     ├─→ 工具执行
     │
     ├─→ after_tool_call
     │      └─→ 过滤工具结果
     │
     ├─→ 持久化
     │
     └─→ agent_end
            └─→ 记录日志/发送通知
```

---

## 📝 Prompt 组装：AI 看到了什么？

### System Prompt 结构

OpenClaw 的 System Prompt 由多个部分组成：

```
┌────────────────────────────────────────┐
│ 1. Base System Prompt                  │
│    - 角色定义                           │
│    - 能力说明                           │
│    - 行为准则                           │
└───────────────────┬────────────────────┘
                    │
                    ↓
┌────────────────────────────────────────┐
│ 2. Skills Prompt                       │
│    - 已加载技能的说明                   │
│    - 工具使用指南                       │
│    - 技能特定规则                       │
└───────────────────┬────────────────────┘
                    │
                    ↓
┌────────────────────────────────────────┐
│ 3. Bootstrap Context                   │
│    - MEMORY.md 内容                     │
│    - USER.md 内容                       │
│    - SOUL.md 内容                       │
│    - 其他上下文文件                     │
└───────────────────┬────────────────────┘
                    │
                    ↓
┌────────────────────────────────────────┐
│ 4. Session History                     │
│    - 历史对话记录                       │
│    - 工具调用历史                       │
│    - 压缩后的上下文（如果启用）         │
└───────────────────┬────────────────────┘
                    │
                    ↓
┌────────────────────────────────────────┐
│ 5. User Message                        │
│    - 当前用户消息                       │
└────────────────────────────────────────┘
```

### Prompt 组装示例

**Base System Prompt**（简化版）：
```
你是 OpenClaw AI 助手，一个功能强大的个人 AI 助手。

你的核心能力：
- 理解和处理用户的消息
- 使用工具完成任务（read、write、exec 等）
- 保持会话上下文和记忆

行为准则：
- 优先使用工具解决问题
- 保持简洁和高效
- 在不确定时主动询问
```

**Skills Prompt**：
```
当前加载的技能：

1. github - GitHub 操作
   - gh CLI 集成
   - 仓库管理、PR 创建等

2. discord - Discord 操作
   - 消息发送
   - 频道管理

工具使用指南：
- 使用 gh 工具进行 GitHub 操作
- 使用 message 工具发送消息
```

**Bootstrap Context**：
```
[MEMORY.md 内容]

# 长期记忆

## 当前任务
- 公众号内容创作
- 每日工作回顾
...

[USER.md 内容]

# 用户信息
- Name: Jason
- Timezone: Asia/Shanghai
...
```

**Session History**：
```
[15:00] User: 帮我写一个 Python 爬虫
[15:01] Assistant: 好的，我来帮你写一个爬虫...
[15:02] Tool: write(path="spider.py", content="...")
[15:02] Tool Result: File created successfully
[15:03] Assistant: 爬虫已创建，文件位置：spider.py
```

**User Message**：
```
帮我添加异常处理
```

### Token 限制

```javascript
// 模型 token 限制
const MODEL_LIMITS = {
  'zai/glm-5': 128000,      // 128K
  'openai/gpt-4': 128000,   // 128K
  'anthropic/claude-3': 200000  // 200K
};

// 压缩预留
const COMPACTION_RESERVE = 8000;  // 预留 8K tokens

// 实际可用
const availableTokens = MODEL_LIMITS[model] - COMPACTION_RESERVE;
```

---

## 🚀 流式输出：如何实现实时响应？

### 流式事件类型

OpenClaw 支持三种流式事件：

#### 1. Assistant Stream（助手回复流）

```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "assistant",
    "delta": "好的，我来帮你",
    "runId": "run-uuid-456"
  }
}
```

#### 2. Tool Stream（工具执行流）

```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "tool",
    "toolName": "read",
    "params": { "path": "spider.py" },
    "status": "start",
    "runId": "run-uuid-456"
  }
}
```

```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "tool",
    "toolName": "read",
    "result": "文件内容...",
    "status": "end",
    "runId": "run-uuid-456"
  }
}
```

#### 3. Lifecycle Stream（生命周期流）

```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "lifecycle",
    "phase": "start",
    "runId": "run-uuid-456"
  }
}
```

```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "lifecycle",
    "phase": "end",
    "status": "ok",
    "summary": {
      "promptTokens": 1234,
      "completionTokens": 567,
      "totalTokens": 1801
    },
    "runId": "run-uuid-456"
  }
}
```

### 流式输出流程

```
模型开始生成
     │
     ├─→ lifecycle: start
     │
     ├─→ assistant: "好的" (delta 1)
     ├─→ assistant: "，我来" (delta 2)
     ├─→ assistant: "帮你" (delta 3)
     │
     ├─→ tool: read (start)
     │      └─→ 工具执行
     ├─→ tool: read (end)
     │
     ├─→ assistant: "文件内容是..." (delta 4)
     │
     └─→ lifecycle: end
            └─→ 总结 + usage
```

### 流式输出的优势

**用户体验**：
- ✅ 实时看到回复，不需要等待
- ✅ 可以提前中断（如果发现方向错误）
- ✅ 更自然的对话体验

**技术优势**：
- ✅ 减少内存占用（不需要缓存完整回复）
- ✅ 可以提前检测错误
- ✅ 支持超长回复

---

## 🛠️ 工具执行：如何调用外部功能？

### Tool Calling 流程

```
模型推理
     │
     ├─→ 检测到 tool_call
     │
     ├─→ 解析 tool_name + params
     │      {
     │        "name": "read",
     │        "arguments": { "path": "spider.py" }
     │      }
     │
     ├─→ before_tool_call hook
     │
     ├─→ 执行工具
     │      const result = await tools.read(params);
     │
     ├─→ after_tool_call hook
     │
     ├─→ 返回 tool result
     │      {
     │        "role": "tool",
     │        "content": "文件内容...",
     │        "tool_call_id": "call-123"
     │      }
     │
     └─→ 继续模型推理
            （模型根据工具结果继续生成）
```

### 工具执行示例

**模型生成**：
```json
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call-123",
      "type": "function",
      "function": {
        "name": "read",
        "arguments": "{\"path\": \"spider.py\"}"
      }
    }
  ]
}
```

**工具执行**：
```javascript
// 执行 read 工具
const result = await tools.read({ path: "spider.py" });

// 返回结果
{
  "role": "tool",
  "content": result,
  "tool_call_id": "call-123"
}
```

**模型继续生成**：
```
好的，我看到文件内容了。现在我来添加异常处理...
```

### 工具结果处理

**Sanitization（清理）**：
```javascript
// 工具结果会被清理
function sanitizeToolResult(result) {
  // 1. 限制大小
  if (result.length > 100000) {
    result = result.substring(0, 100000) + '\n... (truncated)';
  }
  
  // 2. 移除敏感信息
  result = result.replace(/API_KEY=.*/g, 'API_KEY=***');
  
  return result;
}
```

---

## 📤 回复塑造：如何生成最终输出？

### 最终回复组装

```javascript
// 最终回复由以下部分组成
const finalReply = {
  // 1. 助手文本
  text: assistantText,
  
  // 2. 工具摘要（如果 verbose）
  toolSummary: verbose ? generateToolSummary(toolCalls) : null,
  
  // 3. 错误信息（如果有）
  error: hasError ? errorMessage : null
};
```

### 回复过滤

**NO_REPLY 处理**：
```javascript
// 如果助手返回 NO_REPLY，不发送消息
if (assistantText === 'NO_REPLY') {
  // 静默处理，不发送到消息平台
  return;
}
```

**消息工具去重**：
```javascript
// 如果助手已经发送了消息，不再重复发送
const messagingTools = ['send', 'reply'];
const hasMessagingTool = toolCalls.some(t => messagingTools.includes(t.name));

if (hasMessagingTool) {
  // 不再发送最终回复
  return;
}
```

---

## 🔄 压缩与重试：如何处理长对话？

### 上下文压缩（Compaction）

**触发条件**：
```javascript
// 当 token 数接近限制时触发压缩
if (currentTokens > modelLimit * 0.8) {
  await compact(session);
}
```

**压缩流程**：
```
原始 Session History (100K tokens)
     │
     ├─→ 提取关键信息
     │      - 重要决策
     │      - 用户偏好
     │      - 未完成任务
     │
     ├─→ 生成摘要
     │      "之前讨论了 Python 爬虫，已创建 spider.py..."
     │
     └─→ 替换历史
            100K tokens → 10K tokens (摘要)
```

**压缩事件**：
```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "compaction",
    "phase": "start",
    "runId": "run-uuid-456"
  }
}
```

### 重试机制

**工具执行失败**：
```javascript
// 工具执行失败时，模型可以重试
if (toolError) {
  // 返回错误信息给模型
  return {
    "role": "tool",
    "content": `Error: ${error.message}`,
    "tool_call_id": toolCallId
  };
  
  // 模型可以尝试不同的参数或工具
}
```

---

## ⏱️ 超时处理：如何避免无限等待？

### 超时配置

```javascript
// Agent 执行超时
const AGENT_TIMEOUT = 600000;  // 10 分钟

// agent.wait 超时
const WAIT_TIMEOUT = 30000;    // 30 秒

// 工具执行超时
const TOOL_TIMEOUT = 60000;    // 1 分钟
```

### 超时处理流程

```
Agent 开始执行
     │
     ├─→ 设置超时定时器 (10分钟)
     │
     ├─→ 模型推理
     │
     ├─→ 工具执行
     │      └─→ 设置超时定时器 (1分钟)
     │
     └─→ 超时触发
            │
            ├─→ 发送超时事件
            │      {
            │        "stream": "lifecycle",
            │        "phase": "error",
            │        "error": "Agent timeout"
            │      }
            │
            └─→ 终止执行
                   abortController.abort();
```

---

## 🎯 实战：如何优化 Agent 性能？

### 1. 使用队列机制避免冲突

```javascript
// ✅ 正确：同一 session 的任务按顺序执行
async function handleUserMessage(sessionKey, message) {
  await enqueueSession(sessionKey, async () => {
    await runAgent(sessionKey, message);
  });
}

// ❌ 错误：直接并发执行
async function handleUserMessage(sessionKey, message) {
  await runAgent(sessionKey, message);  // 可能导致冲突
}
```

### 2. 使用 Hook 扩展功能

```javascript
// ✅ 正确：使用 Hook 注入上下文
registerHook('before_prompt_build', (context) => {
  context.prependContext = `\n当前时间：${new Date().toLocaleString()}\n`;
});

// ❌ 错误：直接修改核心代码
function buildPrompt(session) {
  // 不推荐：修改核心代码
  prompt += `\n当前时间：${new Date().toLocaleString()}\n`;
}
```

### 3. 使用流式输出提升体验

```javascript
// ✅ 正确：使用流式输出
ws.on('message', (data) => {
  const event = JSON.parse(data);
  
  if (event.event === 'agent') {
    if (event.payload.stream === 'assistant') {
      // 实时显示回复
      displayText(event.payload.delta);
    }
  }
});

// ❌ 错误：等待完整回复
const response = await agent.run(message);
displayText(response.text);  // 用户需要等待很久
```

### 4. 处理超时和错误

```javascript
// ✅ 正确：设置超时和错误处理
try {
  await agent.run(message, { timeout: 600000 });
} catch (error) {
  if (error.name === 'TimeoutError') {
    // 处理超时
    notifyUser('执行超时，请稍后重试');
  } else {
    // 处理其他错误
    notifyUser(`执行失败：${error.message}`);
  }
}

// ❌ 错误：不处理错误
await agent.run(message);  // 可能永远等待
```

---

## 📊 性能监控

### 关键指标

```javascript
// 监控指标
const metrics = {
  // 1. 响应时间
  responseTime: {
    firstToken: 1234,    // 首个 token 时间（毫秒）
    complete: 5678,      // 完成时间（毫秒）
  },
  
  // 2. Token 使用
  tokens: {
    prompt: 1234,        // 输入 token
    completion: 567,     // 输出 token
    total: 1801          // 总 token
  },
  
  // 3. 工具调用
  tools: {
    count: 3,            // 工具调用次数
    totalTime: 2345      // 工具执行总时间（毫秒）
  },
  
  // 4. 压缩
  compaction: {
    before: 100000,      // 压缩前 token
    after: 10000,        // 压缩后 token
    ratio: 0.1           // 压缩比例
  }
};
```

### 性能优化建议

1. **减少 token 使用**：
   - 使用压缩（Compaction）
   - 精简 system prompt
   - 移除不必要的历史记录

2. **优化工具执行**：
   - 缓存工具结果
   - 并行执行独立工具
   - 设置合理的超时

3. **使用流式输出**：
   - 提升用户体验
   - 减少内存占用
   - 支持提前中断

---

## 🎯 总结

### Agent Loop 的核心设计

| 组件 | 职责 | 关键特性 |
|------|------|----------|
| **队列机制** | 避免并发冲突 | Session Lane + Global Lane |
| **Hook 系统** | 扩展功能 | before/after hooks |
| **Prompt 组装** | 构建上下文 | System + Skills + Bootstrap + History |
| **流式输出** | 实时响应 | Assistant + Tool + Lifecycle streams |
| **工具执行** | 调用外部功能 | Tool calling + Sanitization |
| **压缩机制** | 处理长对话 | Compaction + Retry |
| **超时处理** | 避免无限等待 | Agent + Tool + Wait timeouts |

### 核心设计思想

1. **串行化执行**：通过队列机制保证 session 状态一致性
2. **可扩展性**：通过 Hook 系统支持灵活扩展
3. **实时性**：通过流式输出提升用户体验
4. **健壮性**：通过超时、压缩、重试机制保证系统稳定

### 下一步

在下一篇文章中，我们将深入剖析 **多模型支持与 Fallback 机制**，看看 OpenClaw 如何支持 20+ AI 模型，并在模型失败时自动降级。

---

**系列文章**：
- 第 1 篇：从 0 到 1 理解 OpenClaw：Gateway-Client-Node 三层架构 ✅
- 第 2 篇：OpenClaw Agent Loop：从消息到回复的完整旅程 ✅（本文）
- 第 3 篇：OpenClaw 如何支持 20+ AI 模型？多模型架构设计
- 第 4 篇：OpenClaw Session 管理：如何保持 AI 长期记忆？

---

**参考资源**：
- [Agent Loop 文档](https://docs.openclaw.ai/concepts/agent-loop)
- [Queue 文档](https://docs.openclaw.ai/concepts/queue)
- [Hooks 文档](https://docs.openclaw.ai/automation/hooks)
- [Streaming 文档](https://docs.openclaw.ai/concepts/streaming)

---

**作者**：小J  
**发布日期**：2026-03-09  
**系列**：OpenClaw 源码解读系列  
**标签**：#OpenClaw #AgentLoop #AI Agent #流式输出
