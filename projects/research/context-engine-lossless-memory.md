# Context Engine 插件研究 - 无损记忆

> 研究日期：2026-03-09
> 研究目标：理解 OpenClaw 的 Context Engine 插件机制，探索无损记忆的实现方案

---

## 🎯 什么是 Context Engine？

### 核心概念

**Context Engine** 是 OpenClaw 的一个**独占插件插槽**（exclusive plugin slot），负责管理 AI Agent 的上下文（Context）。

**什么是上下文？**
- 上下文 = **所有发送给 AI 模型的内容**
- 包括：System Prompt、对话历史、工具调用、附件等
- 上下文受模型的 **token 限制**（如 GPT-4 的 128K tokens）

**Context Engine 的职责**：
1. **Context Assembly**（上下文组装）：构建发送给模型的完整上下文
2. **Compaction**（压缩）：当上下文接近 token 限制时，压缩旧对话
3. **Session Context Orchestration**（会话上下文编排）：管理会话的生命周期
4. **Ingest**（摄入）：处理新的消息和工具结果

### 插件插槽机制

```json5
// openclaw.json 配置
{
  plugins: {
    slots: {
      memory: "memory-core",        // 记忆插件（默认）
      contextEngine: "legacy",      // 上下文引擎（默认：legacy）
    },
  },
}
```

**独占插槽的特点**：
- ✅ 同一时间只能激活一个插件
- ✅ 其他同类型插件会被自动禁用
- ✅ 通过 `plugins.slots` 配置选择

---

## 📦 默认引擎：Legacy Context Engine

### Legacy 引擎的特点

**OpenClaw 默认使用 `legacy` 上下文引擎**，这是一个内置引擎，提供基本的上下文管理功能。

**核心功能**：

#### 1. 上下文组装

```javascript
// Legacy 引擎的上下文组装流程
function assembleContext(session, params) {
  return {
    // 1. System Prompt
    systemPrompt: buildSystemPrompt({
      tools: getToolList(),
      skills: getSkillList(),
      workspace: getWorkspaceFiles(),
      runtime: getRuntimeMetadata()
    }),
    
    // 2. 对话历史
    messages: session.history,
    
    // 3. 工具调用和结果
    toolCalls: session.toolCalls,
    
    // 4. 附件
    attachments: session.attachments
  };
}
```

**注入的 Workspace 文件**：
- `AGENTS.md` - 工作区规则
- `SOUL.md` - 角色定义
- `TOOLS.md` - 工具说明
- `IDENTITY.md` - 身份信息
- `USER.md` - 用户信息
- `HEARTBEAT.md` - 心跳任务
- `BOOTSTRAP.md` - 首次运行（仅首次）

#### 2. 压缩机制（Compaction）

```javascript
// Legacy 引擎的压缩逻辑
function compact(session) {
  // 1. 检查 token 使用量
  const tokens = countTokens(session);
  
  // 2. 如果接近限制（80%），触发压缩
  if (tokens > modelLimit * 0.8) {
    // 3. 提取关键信息
    const summary = summarizeOldMessages(session.history);
    
    // 4. 替换旧消息为摘要
    session.history = [
      { role: 'system', content: summary },
      ...recentMessages
    ];
  }
}
```

**压缩示例**：
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

## 🔍 无损记忆的概念

### 问题：为什么需要无损记忆？

**传统压缩的问题**：
```
场景：长对话（100+ 轮）

用户（第 1 轮）：创建一个爬虫，爬取 example.com
助手：好的，已创建 spider.py

...（中间 98 轮对话被压缩）...

用户（第 100 轮）：修改爬虫，改用异步
助手：好的，我来修改...

问题：
❌ 助手忘记了 spider.py 的具体实现
❌ 助手不知道之前的架构决策
❌ 需要重新读取文件，浪费 token
```

**无损记忆的目标**：
- ✅ 保留所有对话细节
- ✅ 保留所有工具调用和结果
- ✅ 智能组织上下文，避免信息丢失
- ✅ 在 token 限制内最大化上下文利用

### 无损记忆的实现思路

#### 方案 1：分层上下文（Layered Context）

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

**实现示例**：
```javascript
class LayeredContextEngine {
  async assembleContext(session, params) {
    // 1. 活跃层：最近 20 轮对话
    const activeLayer = session.history.slice(-20);
    
    // 2. 索引层：之前的对话索引
    const indexLayer = await this.buildIndex(session.history.slice(0, -20));
    
    // 3. 如果用户提问涉及旧话题，从存储层加载
    if (this.needsHistoricalContext(params.message, indexLayer)) {
      const relevantHistory = await this.loadRelevant(session, params.message);
      return [...relevantHistory, ...activeLayer];
    }
    
    return [...indexLayer, ...activeLayer];
  }
  
  buildIndex(history) {
    // 为每段对话生成索引（主题+关键词）
    return history.map(msg => ({
      role: msg.role,
      topic: extractTopic(msg.content),
      keywords: extractKeywords(msg.content),
      timestamp: msg.timestamp,
      pointer: msg.id  // 指向存储层的指针
    }));
  }
}
```

#### 方案 2：图结构上下文（Graph Context）

```
对话图（Conversation Graph）：

[Node 1: 创建爬虫]
  └─→ [Node 2: write(spider.py)]
        └─→ [Node 3: 添加异常处理]
              └─→ [Node 4: read(spider.py)]
                    └─→ [Node 5: edit(spider.py)]

依赖关系：
- Node 5 依赖 Node 4（需要先读取）
- Node 4 依赖 Node 2（需要知道文件内容）
- Node 2 依赖 Node 1（需要知道爬虫需求）
```

**优势**：
- ✅ 保留因果关系
- ✅ 可以追溯决策链
- ✅ 按需加载相关节点

**实现示例**：
```javascript
class GraphContextEngine {
  async assembleContext(session, params) {
    // 1. 构建对话图
    const graph = this.buildGraph(session.history);
    
    // 2. 找到当前话题相关的节点
    const relevantNodes = this.findRelevantNodes(graph, params.message);
    
    // 3. 加载依赖链
    const context = [];
    for (const node of relevantNodes) {
      const dependencies = this.getDependencies(graph, node);
      context.push(...dependencies, node);
    }
    
    return context;
  }
  
  buildGraph(history) {
    const nodes = new Map();
    const edges = [];
    
    for (const msg of history) {
      const node = {
        id: msg.id,
        content: msg.content,
        type: msg.role === 'user' ? 'user' : 'assistant',
        tools: msg.toolCalls || []
      };
      
      nodes.set(node.id, node);
      
      // 构建依赖关系
      if (msg.toolCalls) {
        for (const tool of msg.toolCalls) {
          // 工具调用依赖之前的文件创建/修改
          if (tool.name === 'read' || tool.name === 'edit') {
            const fileNode = this.findFileNode(nodes, tool.params.path);
            if (fileNode) {
              edges.push({ from: fileNode.id, to: node.id });
            }
          }
        }
      }
    }
    
    return { nodes, edges };
  }
}
```

#### 方案 3：向量化上下文（Vector Context）

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

**实现示例**：
```javascript
class VectorContextEngine {
  constructor() {
    this.vectorDB = new LanceDB('~/.openclaw/context-vectors');
  }
  
  async assembleContext(session, params) {
    // 1. 将当前问题向量化
    const queryVector = await this.embed(params.message);
    
    // 2. 搜索相关的历史消息
    const relevantMessages = await this.vectorDB.search({
      vector: queryVector,
      topK: 10,
      filter: { sessionId: session.id }
    });
    
    // 3. 组装上下文
    const recentMessages = session.history.slice(-10);
    const context = [...relevantMessages, ...recentMessages];
    
    return context;
  }
  
  async embed(text) {
    // 使用 OpenAI Embedding API
    const response = await openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: text
    });
    return response.data[0].embedding;
  }
  
  async addToIndex(session, message) {
    // 将新消息添加到向量索引
    const vector = await this.embed(message.content);
    await this.vectorDB.add({
      id: message.id,
      vector,
      content: message.content,
      timestamp: message.timestamp,
      sessionId: session.id
    });
  }
}
```

---

## 🛠️ 如何实现 Context Engine 插件？

### 插件注册

```typescript
// my-context-engine/index.ts
import { ContextEngineFactory } from './engine';

export default function register(api) {
  // 注册 Context Engine
  api.registerContextEngine('my-context-engine', ContextEngineFactory);
  
  // 可选：注册 Hook
  api.registerHook('before_prompt_build', async (context) => {
    // 在 Prompt 组装前注入自定义上下文
    const additionalContext = await myEngine.getAdditionalContext(context.session);
    context.prependContext = additionalContext;
  });
}
```

### 插件清单（Manifest）

```json
{
  "id": "my-context-engine",
  "kind": "context-engine",
  "version": "1.0.0",
  "name": "My Context Engine",
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
  },
  "uiHints": {
    "maxActiveTokens": {
      "label": "活跃层 Token 限制",
      "help": "活跃层保留的最大 token 数量"
    },
    "enableVectorSearch": {
      "label": "启用向量搜索",
      "help": "使用向量搜索找到相关的历史消息"
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

interface Context {
  systemPrompt: string;
  messages: Message[];
  toolCalls?: ToolCall[];
  attachments?: Attachment[];
}
```

### 完整实现示例

```typescript
// engine.ts
import { ContextEngine, Context, Session, AgentParams, Message } from 'openclaw';

export class LosslessContextEngine implements ContextEngine {
  private config: any;
  private vectorDB: VectorDB;
  
  constructor(config: any) {
    this.config = config;
    this.vectorDB = new LanceDB(config.dbPath || '~/.openclaw/context-vectors');
  }
  
  async assembleContext(session: Session, params: AgentParams): Promise<Context> {
    // 1. 活跃层：最近的对话
    const activeMessages = session.history.slice(-this.config.maxActiveMessages || 20);
    
    // 2. 索引层：向量化检索
    let indexedMessages: Message[] = [];
    if (this.config.enableVectorSearch) {
      indexedMessages = await this.searchRelevantMessages(session, params.message);
    }
    
    // 3. 去重并合并
    const allMessages = this.mergeAndDeduplicate(indexedMessages, activeMessages);
    
    // 4. 构建 system prompt
    const systemPrompt = await this.buildSystemPrompt(session, params);
    
    return {
      systemPrompt,
      messages: allMessages
    };
  }
  
  async compact(session: Session): Promise<void> {
    // 无损压缩：不删除消息，而是建立索引
    const oldMessages = session.history.slice(0, -20);
    
    // 向量化并存储
    for (const msg of oldMessages) {
      await this.vectorDB.add({
        id: msg.id,
        vector: await this.embed(msg.content),
        content: msg.content,
        timestamp: msg.timestamp,
        sessionId: session.id
      });
    }
    
    // 从内存中移除旧消息（但保留在向量数据库中）
    session.history = session.history.slice(-20);
  }
  
  async ingest(session: Session, message: Message): Promise<void> {
    // 将新消息添加到向量索引
    if (this.config.enableVectorSearch) {
      await this.vectorDB.add({
        id: message.id,
        vector: await this.embed(message.content),
        content: message.content,
        timestamp: message.timestamp,
        sessionId: session.id
      });
    }
  }
  
  private async searchRelevantMessages(session: Session, query: string): Promise<Message[]> {
    const queryVector = await this.embed(query);
    
    const results = await this.vectorDB.search({
      vector: queryVector,
      topK: 10,
      filter: { sessionId: session.id }
    });
    
    return results.map(r => ({
      id: r.id,
      role: 'assistant',  // 或从存储中读取
      content: r.content,
      timestamp: r.timestamp
    }));
  }
  
  private async embed(text: string): Promise<number[]> {
    // 使用 OpenAI Embedding API
    const response = await openai.embeddings.create({
      model: 'text-embedding-3-small',
      input: text
    });
    return response.data[0].embedding;
  }
  
  private mergeAndDeduplicate(indexed: Message[], active: Message[]): Message[] {
    const seen = new Set<string>();
    const result: Message[] = [];
    
    // 先添加索引消息
    for (const msg of indexed) {
      if (!seen.has(msg.id)) {
        result.push(msg);
        seen.add(msg.id);
      }
    }
    
    // 再添加活跃消息（去重）
    for (const msg of active) {
      if (!seen.has(msg.id)) {
        result.push(msg);
        seen.add(msg.id);
      }
    }
    
    return result;
  }
  
  private async buildSystemPrompt(session: Session, params: AgentParams): Promise<string> {
    // 构建 system prompt（与 legacy 引擎类似）
    let prompt = `你是 OpenClaw AI 助手。\n\n`;
    
    // 添加工具列表
    prompt += `可用工具：${params.tools.map(t => t.name).join(', ')}\n\n`;
    
    // 添加技能列表
    prompt += `已加载技能：${params.skills.map(s => s.name).join(', ')}\n\n`;
    
    // 添加上下文引擎说明
    prompt += `\n[上下文引擎：无损记忆]\n`;
    prompt += `本会话使用无损记忆上下文引擎，可以检索到之前对话的相关内容。\n`;
    
    return prompt;
  }
}

export const ContextEngineFactory = (config: any) => new LosslessContextEngine(config);
```

---

## 📊 性能对比

### Legacy vs 无损记忆

| 指标 | Legacy 引擎 | 无损记忆引擎 |
|------|------------|-------------|
| **上下文保留** | 压缩后丢失细节 | 完整保留 |
| **检索能力** | 无（只能看最近 N 轮） | 向量搜索，语义检索 |
| **Token 使用** | 较低（压缩后） | 较高（但更智能） |
| **响应速度** | 快 | 稍慢（需要向量搜索） |
| **适用场景** | 短对话、简单任务 | 长对话、复杂项目 |

### Token 使用示例

**场景：100 轮对话，用户问第 5 轮的话题**

**Legacy 引擎**：
```
上下文内容：
- System Prompt: 10K tokens
- 压缩摘要: 5K tokens
- 最近 20 轮: 15K tokens
- 总计: 30K tokens

问题：无法回答第 5 轮的话题（已被压缩）
```

**无损记忆引擎**：
```
上下文内容：
- System Prompt: 10K tokens
- 向量检索结果（第 5 轮相关）: 3K tokens
- 最近 20 轮: 15K tokens
- 总计: 28K tokens

优势：可以准确回答第 5 轮的话题
```

---

## 🎯 最佳实践

### 1. 何时使用无损记忆？

**推荐场景**：
- ✅ 长期项目（多天/多周的对话）
- ✅ 复杂任务（需要追溯决策链）
- ✅ 多文件协作（需要记住文件关系）
- ✅ 用户偏好记忆（个性化服务）

**不推荐场景**：
- ❌ 简单问答（不需要历史上下文）
- ❌ 一次性任务（不需要长期记忆）
- ❌ Token 预算有限（向量搜索会增加开销）

### 2. 配置建议

```json5
// 推荐配置
{
  plugins: {
    slots: {
      contextEngine: "lossless-context-engine",
    },
    entries: {
      "lossless-context-engine": {
        enabled: true,
        config: {
          maxActiveMessages: 30,        // 活跃层消息数
          enableVectorSearch: true,     // 启用向量搜索
          maxSearchResults: 10,         // 最大搜索结果
          embeddingModel: "text-embedding-3-small"  // 便宜且快速
        }
      }
    }
  }
}
```

### 3. 与 Memory 插件配合

```json5
{
  plugins: {
    slots: {
      memory: "memory-lancedb",        // 长期记忆
      contextEngine: "lossless-context-engine",  // 无损上下文
    }
  }
}
```

**配合方式**：
- **Memory 插件**：存储跨会话的长期记忆（用户偏好、重要决策）
- **Context Engine**：管理当前会话的上下文（对话历史、工具调用）
- 两者互补，提供完整的记忆能力

---

## 🚀 下一步研究方向

### 1. 实现原型

- [ ] 实现基于向量搜索的 Context Engine 插件
- [ ] 集成 LanceDB 作为向量数据库
- [ ] 测试与 Legacy 引擎的对比

### 2. 优化策略

- [ ] 分层缓存（活跃层 + 索引层 + 存储层）
- [ ] 智能预加载（预测用户可能提问的话题）
- [ ] 动态调整（根据 token 预算自动调整层数）

### 3. 用户界面

- [ ] 可视化上下文结构（图/树结构）
- [ ] 手动标记重要消息（永久保留）
- [ ] 上下文搜索功能（用户可以搜索历史对话）

---

## 📚 参考资料

### OpenClaw 官方文档
- [Context 概念](https://docs.openclaw.ai/concepts/context)
- [Plugin 开发指南](https://docs.openclaw.ai/tools/plugin)
- [Compaction 机制](https://docs.openclaw.ai/concepts/compaction)

### 相关技术
- [LanceDB](https://lancedb.github.io/lancedb/) - 向量数据库
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) - 文本向量化
- [RAG (Retrieval-Augmented Generation)](https://docs.anthropic.com/claude/docs/retrieval-augmented-generation) - 检索增强生成

---

**研究总结**：
Context Engine 是 OpenClaw 的核心插件插槽，负责管理 AI Agent 的上下文。默认的 Legacy 引擎通过压缩来处理长对话，但会丢失细节。无损记忆引擎通过向量搜索、分层存储等技术，在 token 限制内最大化保留上下文信息，适用于长期项目和复杂任务。

**作者**：小J
**研究日期**：2026-03-09
**标签**：#OpenClaw #ContextEngine #无损记忆 #向量搜索
