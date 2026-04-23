# OpenClaw Session 管理：如何让 AI 拥有长期记忆？

> 本文是 OpenClaw 源码解读系列第 4 篇，深入剖析会话状态管理和上下文工程。

---

## 你是否遇到过这些问题？

让 AI 帮你处理任务，第二天再问它：

> "昨天我们讨论的那个项目..."

AI 一脸懵："不好意思，我没有之前对话的记录。"

或者对话长了之后：

> "抱歉，上下文太长了，我记不住之前的内容..."

**AI 的记忆问题**：
- 重启就失忆
- 上下文窗口有限
- 重要信息被淹没

**OpenClaw 的解决方案**：
- 持久化 Session（重启不丢记忆）
- 上下文压缩（智能保留关键信息）
- 长期记忆（MEMORY.md + daily notes）

---

## 📝 Session 生命周期

### 完整流程

```
创建 Session
    ↓
持久化到磁盘
    ↓
[使用中] ← → [加载到内存]
    ↓
上下文膨胀？
    ↓
自动压缩（Prune）
    ↓
归档（Archive）
```

### 状态转换

| 状态 | 说明 | 触发条件 |
|------|------|---------|
| **Active** | 正在使用 | 有新消息 |
| **Idle** | 空闲中 | 超过 30 分钟无活动 |
| **Pruned** | 已压缩 | 上下文超过阈值 |
| **Archived** | 已归档 | 用户手动归档 |

---

## 🧠 上下文管理策略

### 1. Memory.md - 长期记忆

**作用**：存储用户偏好、重要决策、长期任务

**示例结构**：
```markdown
# MEMORY.md

## 用户偏好
- 语言：中文
- 风格：简洁
- 时区：Asia/Shanghai

## 重要决策
- 2026-03-01：选择 OpenClaw 作为 AI 平台
- 2026-03-05：配置 GitHub 自动化

## 长期任务
- 公众号文章系列（28 天）
- OpenClaw 源码解读（8 篇）
```

**加载时机**：
- 主会话（直接聊天）→ 自动加载
- 共享会话（Discord/群聊）→ 不加载（安全考虑）

### 2. Daily Notes - 短期记忆

**作用**：记录当天的工作、临时决策

**示例**：
```markdown
# 2026-03-11 工作记录

## 完成的任务
- ✅ 学习 PUA Skill
- ✅ 写公众号文章
- ✅ 推送到 GitHub

## 遇到的问题
- GitHub 推送失败（网络问题）
- 微信草稿 ID 失效（已重新创建）
```

**清理策略**：
- 每周整理一次
- 重要信息迁移到 MEMORY.md
- 旧的 daily notes 可以删除

### 3. Context Engine - 动态上下文

**作用**：根据当前任务动态加载相关上下文

**加载流程**：
```
1. 分析当前消息
2. 搜索相关文件（memory_search）
3. 提取关键片段
4. 注入到 prompt
```

**示例**：
```
用户问："我们昨天的项目进度如何？"

→ 搜索 memory/2026-03-10.md
→ 提取项目相关段落
→ 注入到 prompt
→ AI 回答时带有上下文
```

---

## 💾 持久化设计

### 文件结构

```
~/.openclaw/
├── sessions/
│   ├── session-abc123.json      # Session 元数据
│   └── session-abc123-transcript.jsonl  # 对话记录
├── workspace/
│   ├── MEMORY.md                # 长期记忆
│   └── memory/
│       ├── 2026-03-11.md        # 每日记录
│       └── heartbeat-state.json # 状态数据
```

### Session 元数据

```json
{
  "sessionKey": "session-abc123",
  "createdAt": "2026-03-11T10:00:00Z",
  "lastActive": "2026-03-11T14:00:00Z",
  "model": "zai/glm-5",
  "status": "active",
  "messageCount": 42,
  "contextSize": 15000
}
```

### 对话记录（JSONL）

```jsonl
{"role":"user","content":"帮我写一篇文章","timestamp":"2026-03-11T10:00:00Z"}
{"role":"assistant","content":"好的，请问主题是什么？","timestamp":"2026-03-11T10:00:05Z"}
{"role":"user","content":"OpenClaw 源码解读","timestamp":"2026-03-11T10:01:00Z"}
```

---

## 🔄 上下文压缩（Prune）

### 触发条件

- 上下文超过模型窗口的 80%
- Session 空闲超过 24 小时
- 手动触发 prune

### 压缩策略

**1. 保留系统消息**
```
System Prompt + Skills + MEMORY.md
```

**2. 保留最近 N 轮对话**
```
最近 10 轮对话（用户 + AI）
```

**3. 压缩中间对话**
```
中间对话 → 摘要（Summary）
```

**压缩前**：
```
User: 帮我写文章
AI: 好的，主题？
User: OpenClaw 源码
AI: 好的，开始写...
... (50 轮对话)
User: 加上代码示例
AI: 好的...
```

**压缩后**：
```
[Summary] 用户要求写一篇 OpenClaw 源码解读文章，
已完成初稿，现在添加代码示例。

User: 加上代码示例
AI: 好的...
```

---

## 🛠️ Session 工具

### session tool

**查看 Session 状态**：
```
session_status()
```

**列出所有 Session**：
```
sessions_list()
```

**发送消息到其他 Session**：
```
sessions_send(sessionKey, message)
```

### 清理工具

**删除旧 Session**：
```bash
# 保留最近 7 天
find ~/.openclaw/sessions -mtime +7 -delete
```

**归档 Session**：
```bash
# 移动到归档目录
mv ~/.openclaw/sessions/session-old.json ~/.openclaw/sessions/archive/
```

---

## 🎯 最佳实践

### 1. 分层记忆策略

```
┌─────────────────┐
│   System Prompt │ (AI 身份 + 能力)
├─────────────────┤
│    MEMORY.md    │ (长期记忆 - 用户偏好)
├─────────────────┤
│   Daily Notes   │ (短期记忆 - 今天的工作)
├─────────────────┤
│  Recent Chat    │ (最近对话 - 当前上下文)
└─────────────────┘
```

### 2. 定期整理

**每天**：
- 更新 daily notes
- 记录重要决策

**每周**：
- 整理 daily notes
- 迁移重要信息到 MEMORY.md
- 清理旧 Session

**每月**：
- 备份 MEMORY.md
- 归档旧 Session
- 检查上下文使用情况

### 3. 安全考虑

**不要在共享会话中加载 MEMORY.md**：
- Discord 群聊 → 不加载
- 私聊 → 加载

**敏感信息加密**：
```json
// ~/.openclaw/openclaw.json
{
  "secrets": {
    "api_key": "encrypted:..."
  }
}
```

---

## 📊 性能优化

### 1. 延迟加载

```javascript
// 只在需要时加载 Session
async function loadSession(sessionKey) {
  if (!cache.has(sessionKey)) {
    const data = await readFile(`sessions/${sessionKey}.json`);
    cache.set(sessionKey, data);
  }
  return cache.get(sessionKey);
}
```

### 2. 增量写入

```javascript
// 对话记录追加写入，不重写整个文件
function appendMessage(sessionKey, message) {
  const line = JSON.stringify(message) + '\n';
  appendFileSync(`sessions/${sessionKey}-transcript.jsonl`, line);
}
```

### 3. 内存缓存

```javascript
// 热点 Session 保存在内存
const cache = new LRU({
  max: 100,  // 最多 100 个 Session
  maxAge: 30 * 60 * 1000  // 30 分钟过期
});
```

---

## 🚀 实战案例

### 案例 1：长期项目跟踪

**场景**：28 天公众号文章系列

**Session 设计**：
```
MEMORY.md
├── 当前任务清单
│   ├── 公众号内容创作（进行中）
│   ├── 每日工作回顾（进行中）
│   └── GitHub 项目推荐（进行中）
├── 文章进度
│   ├── 第 1 周：100%
│   ├── 第 2 周：86%
│   └── 第 3 周：14%
└── 已犯的错误
    └── 2026-02-02：泄露 Token（已修复）
```

**效果**：
- 重启后继续工作
- 跨 Session 保持上下文
- 自动追踪进度

### 案例 2：多 Session 协作

**场景**：Cron 任务 + 主会话

**架构**：
```
主会话 (session-main)
    ↓
Cron 任务 (session-cron-xxx)
    ↓
完成后通知主会话
    ↓
sessions_send(session-main, "任务完成")
```

**代码示例**：
```javascript
// Cron 任务完成后
async function onTaskComplete(result) {
  // 更新 MEMORY.md
  await updateMemory(result);
  
  // 通知主会话
  await sessions_send('session-main', {
    type: 'task_complete',
    task: 'daily-article',
    result: result
  });
}
```

---

## 🔧 配置选项

### Session 配置

```json
// ~/.openclaw/openclaw.json
{
  "session": {
    "maxContextSize": 50000,  // 最大上下文（tokens）
    "pruneThreshold": 0.8,    // 压缩阈值（80%）
    "archiveAfterDays": 30,   // 30 天后归档
    "memoryFile": "MEMORY.md" // 长期记忆文件
  }
}
```

### 上下文配置

```json
{
  "context": {
    "loadMemory": true,       // 加载 MEMORY.md
    "loadDailyNotes": true,   // 加载 daily notes
    "maxDailyNotes": 2,       // 最多加载 2 天
    "searchMemory": true      // 搜索历史记忆
  }
}
```

---

## 📚 相关源码

### 核心文件

| 文件 | 说明 |
|------|------|
| `/docs/concepts/session.md` | Session 概念文档 |
| `/docs/concepts/memory.md` | 记忆系统文档 |
| `/docs/concepts/context.md` | 上下文引擎文档 |
| `/docs/tools/session.md` | Session 工具文档 |

### 关键 API

```javascript
// Session 管理
sessions_list()
sessions_history(sessionKey)
sessions_send(sessionKey, message)
session_status()

// 记忆管理
memory_search(query)
memory_get(path, from, lines)
```

---

## 总结

OpenClaw 的 Session 管理设计哲学：

1. **持久化优先**：重启不丢记忆
2. **分层记忆**：长期 + 短期 + 动态
3. **智能压缩**：自动管理上下文窗口
4. **安全隔离**：共享会话不加载敏感信息

**核心价值**：
- AI 拥有"长期记忆"
- 跨 Session 保持上下文
- 自动追踪项目进度
- 安全可控的信息访问

---

下一篇：**技能系统架构设计** - OpenClaw 如何实现可扩展的 AI 能力？

---

<p style="text-align: center; color: #666; font-size: 14px; margin-top: 24px;">如果觉得有用，点个"在看"吧 👇</p>
