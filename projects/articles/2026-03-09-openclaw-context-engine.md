# OpenClaw Context Engine 插件：让你的 AI 助手拥有「无损记忆」

> 本文将深入解析 OpenClaw 的 Context Engine 插件机制，并探索如何实现「无损记忆」—— 让 AI 在长对话中不再遗忘任何细节。

---

## 🤔 你有没有遇到过这种情况？

你和一个 AI 聊了 100 轮，做了很多决策，改了很多代码。突然你想回到第 5 轮讨论的话题...

**AI 回复**：「抱歉，我不记得我们之前讨论过什么了。」

这就是 **上下文压缩** 的代价 —— 为了节省 token，旧对话被压缩成摘要，细节全部丢失。

今天我们来研究 OpenClaw 的 **Context Engine 插件**，看看如何实现「无损记忆」。

---

## 📦 什么是 Context Engine？

### 核心概念

**Context Engine** 是 OpenClaw 的一个**独占插件插槽**，负责管理 AI Agent 的上下文。

**什么是上下文？**
- 上下文 = **所有发送给 AI 模型的内容**
- 包括：System Prompt、对话历史、工具调用、附件等
- 上下文受模型的 **token 限制**（如 GPT-4 的 128K tokens）

**Context Engine 的职责**：

| 职责 | 说明 |
|------|------|
| **Context Assembly** | 构建发送给模型的完整上下文 |
| **Compaction** | 当上下文接近 token 限制时，压缩旧对话 |
| **Session Orchestration** | 管理会话的生命周期 |
| **Ingest** | 处理新的消息和工具结果 |

### 插件插槽机制

```json
// openclaw.json 配置
{
  "plugins": {
    "slots": {
      "memory": "memory-core",
      "contextEngine": "legacy"  // 默认使用 legacy 引擎
    }
  }
}
```

**独占插槽的特点**：
- 同一时间只能激活一个插件
- 其他同类型插件会被自动禁用
- 通过 `plugins.slots` 配置选择

---

## 🔍 默认引擎：Legacy Context Engine

### Legacy 引擎的工作原理

OpenClaw 默认使用 `legacy` 上下文引擎，提供基本的上下文管理功能。

**上下文组装流程**：

```
┌─────────────────────────────────────┐
│ 1. System Prompt                    │
│    - 工具列表                        │
│    - 技能列表                        │
│    - Workspace 文件                  │
│    - 运行时元数据                    │
├─────────────────────────────────────┤
│ 2. 对话历史                          │
│    - 用户消息                        │
│    - 助手回复                        │
├─────────────────────────────────────┤
│ 3. 工具调用和结果                    │
├─────────────────────────────────────┤
│ 4. 附件                              │
└─────────────────────────────────────┘
```

### 压缩机制的问题

当上下文接近 token 限制（80%）时，Legacy 引擎会触发压缩：

```
原始对话（100K tokens）：
[10:00] User: 帮我写一个爬虫
[10:01] Assistant: 好的，我来帮你...
[10:02] Tool: write(spider.py)
...
[14:00] User: 添加异常处理

压缩后（10K tokens）：
[System] 之前讨论了 Python 爬虫，已创建 spider.py...
[14:00] User: 添加异常处理
```

**压缩的问题**：
- ❌ **信息丢失**：旧的对话细节被总结成摘要
- ❌ **上下文断裂**：模型可能忘记之前的决策
- ❌ **依赖关系丢失**：工具调用的因果关系被简化

---

## 🚀 无损记忆：三种实现方案

### 方案 1：分层上下文（Layered Context）

```
┌─────────────────────────────────────┐
│ 活跃层（Active Layer）               │
│ - 最近 20 轮对话（完整）             │
│ - 当前工具调用                       │
│ - 2,000 tokens                      │
└─────────────┬───────────────────────┘
              │
              ↓
┌─────────────────────────────────────┐
│ 索引层（Index Layer）                │
│ - 之前对话的索引（主题+关键词）      │
│ - 工具调用的索引（文件+操作）        │
│ - 5,000 tokens                      │
└─────────────┬───────────────────────┘
              │
              ↓
┌─────────────────────────────────────┐
│ 存储层（Storage Layer）              │
│ - 完整对话历史（磁盘）               │
│ - 完整工具调用记录                   │
│ - 按需加载                          │
└─────────────────────────────────────┘
```

**优势**：
- ✅ 活跃层保证当前任务的完整上下文
- ✅ 索引层提供快速检索能力
- ✅ 存储层保证不丢失任何信息

### 方案 2：图结构上下文（Graph Context）

```
对话图（Conversation Graph）：

[Node 1: 创建爬虫]
  └─→ [Node 2: write(spider.py)]
        └─→ [Node 3: 添加异常处理]
              └─→ [Node 4: read(spider.py)]
                    └─→ [Node 5: edit(spider.py)]
```

**优势**：
- ✅ 保留因果关系
- ✅ 可以追溯决策链
- ✅ 按需加载相关节点

### 方案 3：向量化上下文（Vector Context）

```
向量数据库（Vector Database）：

Message 1 → Embedding → [0.1, 0.2, 0.3, ...]
Message 2 → Embedding → [0.4, 0.5, 0.6, ...]
...

当前问题 → Embedding → [0.2, 0.3, 0.4, ...]
           ↓
      向量搜索（相似度 > 0.8）
           ↓
   返回相关的历史消息
```

**优势**：
- ✅ 语义搜索，找到真正相关的内容
- ✅ 不受关键词限制
- ✅ 支持跨会话检索

---

## 🛠️ 如何实现 Context Engine 插件？

### 插件清单（Manifest）

```json
{
  "id": "lossless-context-engine",
  "kind": "context-engine",
  "version": "1.0.0",
  "name": "Lossless Context Engine",
  "description": "无损记忆上下文引擎",
  "configSchema": {
    "type": "object",
    "properties": {
      "maxActiveTokens": {
        "type": "number",
        "default": 10000,
        "description": "活跃层最大 token 数"
      },
      "enableVectorSearch": {
        "type": "boolean",
        "default": true,
        "description": "启用向量搜索"
      }
    }
  }
}
```

### 核心接口

```typescript
interface ContextEngine {
  // 1. 上下文组装
  assembleContext(session: Session, params: AgentParams): Promise<Context>;
  
  // 2. 压缩（可选）
  compact?(session: Session): Promise<void>;
  
  // 3. 摄入新消息
  ingest?(session: Session, message: Message): Promise<void>;
  
  // 4. 生命周期钩子
  onSessionStart?(session: Session): Promise<void>;
  onSessionEnd?(session: Session): Promise<void>;
}
```

### 实现示例（向量化上下文）

```typescript
export class LosslessContextEngine implements ContextEngine {
  private vectorDB: VectorDB;
  
  constructor(config: any) {
    this.vectorDB = new LanceDB(config.dbPath);
  }
  
  async assembleContext(session: Session, params: AgentParams): Promise<Context> {
    // 1. 活跃层：最近的对话
    const activeMessages = session.history.slice(-20);
    
    // 2. 向量检索：找到相关的历史消息
    const queryVector = await this.embed(params.message);
    const relevantMessages = await this.vectorDB.search({
      vector: queryVector,
      topK: 10,
      filter: { sessionId: session.id }
    });
    
    // 3. 合并并返回
    return {
      systemPrompt: await this.buildSystemPrompt(session, params),
      messages: [...relevantMessages, ...activeMessages]
    };
  }
  
  async ingest(session: Session, message: Message): Promise<void> {
    // 将新消息添加到向量索引
    await this.vectorDB.add({
      id: message.id,
      vector: await this.embed(message.content),
      content: message.content,
      timestamp: message.timestamp
    });
  }
}
```

---

## 📊 性能对比

### Legacy vs 无损记忆

| 指标 | Legacy 引擎 | 无损记忆引擎 |
|------|------------|-------------|
| **上下文保留** | 压缩后丢失细节 | 完整保留 |
| **检索能力** | 无 | 向量搜索 |
| **Token 使用** | 较低 | 较高（但更智能） |
| **响应速度** | 快 | 稍慢 |
| **适用场景** | 短对话、简单任务 | 长对话、复杂项目 |

### 实际效果对比

**场景：100 轮对话，用户问第 5 轮的话题**

**Legacy 引擎**：
```
上下文：30K tokens
问题：无法回答第 5 轮的话题（已被压缩）
```

**无损记忆引擎**：
```
上下文：28K tokens
优势：可以准确回答第 5 轮的话题（向量检索）
```

---

## 🎯 最佳实践

### 何时使用无损记忆？

**推荐场景**：
- ✅ 长期项目（多天/多周的对话）
- ✅ 复杂任务（需要追溯决策链）
- ✅ 多文件协作（需要记住文件关系）
- ✅ 用户偏好记忆（个性化服务）

**不推荐场景**：
- ❌ 简单问答（不需要历史上下文）
- ❌ 一次性任务（不需要长期记忆）
- ❌ Token 预算有限（向量搜索会增加开销）

### 配置建议

```json
{
  "plugins": {
    "slots": {
      "memory": "memory-lancedb",
      "contextEngine": "lossless-context-engine"
    },
    "entries": {
      "lossless-context-engine": {
        "enabled": true,
        "config": {
          "maxActiveMessages": 30,
          "enableVectorSearch": true,
          "embeddingModel": "text-embedding-3-small"
        }
      }
    }
  }
}
```

---

## 📚 总结

Context Engine 是 OpenClaw 的核心插件插槽，负责管理 AI Agent 的上下文。

**默认的 Legacy 引擎**通过压缩来处理长对话，但会丢失细节。

**无损记忆引擎**通过向量搜索、分层存储等技术，在 token 限制内最大化保留上下文信息，适用于长期项目和复杂任务。

如果你想开发自己的 Context Engine 插件，可以参考本文的代码示例，结合 LanceDB、OpenAI Embeddings 等技术，打造适合自己场景的无损记忆引擎。

---

**参考资料**：
- [OpenClaw Context 概念](https://docs.openclaw.ai/concepts/context)
- [OpenClaw Plugin 开发指南](https://docs.openclaw.ai/tools/plugin)
- [LanceDB 向量数据库](https://lancedb.github.io/lancedb/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

---

**作者**：小J
**发布日期**：2026-03-09
**标签**：#OpenClaw #ContextEngine #无损记忆 #向量搜索 #AI记忆
