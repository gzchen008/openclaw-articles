# 如何构建 OpenClaw 知识库？从零到精通的完整指南

你的 AI 助手会"失忆"吗？

每次重启会话，它就忘了你的偏好、项目进展、重要决策...这谁顶得住？

今天教你用 OpenClaw 构建一个**永不失忆的知识库**，让你的 AI 越用越聪明！

---

## 一、OpenClaw 记忆架构长啥样？

OpenClaw 的记忆系统很简单：**全部用 Markdown 文件存储**。

```
~/.openclaw/workspace/
├── MEMORY.md              # 长期记忆（决策、偏好、事实）
├── memory/
│   ├── 2026-03-30.md      # 每日笔记
│   ├── 2026-03-29.md
│   └── weekly/            # 周度汇总（可选）
```

**加载规则**：
- MEMORY.md：每次私聊启动时自动加载
- memory/*.md：今天 + 昨天的文件自动加载
- 群聊不加载 MEMORY.md（保护隐私）

**核心理念**：文件即记忆。只要写进文件，AI 就能记住。

---

## 二、三种 Memory Search 后端

OpenClaw 提供三种记忆搜索后端：

### 1️⃣ Builtin（默认推荐）

**特点**：SQLite + FTS5 + 向量搜索，零配置

**自动启用条件**（有任一 API Key）：
- OpenAI
- Gemini
- Voyage
- Mistral

**适合人群**：大多数用户

### 2️⃣ QMD（高级搜索）

**特点**：
- Reranking（重排序）
- Query Expansion（查询扩展）
- 可索引 workspace 外的目录
- 可索引会话记录（回忆历史对话）
- 完全本地运行

**安装**：
```bash
bun install -g https://github.com/tobi/qmd
```

**适合人群**：需要搜索项目文档、历史对话的用户

### 3️⃣ Honcho（知识图谱）

**特点**：
- AI 原生跨会话记忆
- 自动用户建模
- 多代理感知

**安装**：
```bash
openclaw plugins install honcho
```

**适合人群**：多代理系统、知识密集型应用

---

## 三、自动记忆机制

### Pre-compaction Memory Flush

**工作原理**：当会话接近 compaction 阈值时，OpenClaw 自动执行一次静默 turn，提醒模型保存重要内容到记忆文件。

**配置示例**：
```json
{
  "agents": {
    "defaults": {
      "compaction": {
        "memoryFlush": {
          "enabled": true,
          "softThresholdTokens": 4000
        }
      }
    }
  }
}
```

### 三层 Cron 自动记忆（社区方案）

GitHub 上有个 `openclaw-memory-fusion` 项目，实现了三层自动记忆：

- L1 hourly（每天 5 次）：微同步 → memory/YYYY-MM-DD.md
- L2 daily（23:30）：当天 canonical → MEMORY.md
- L3 weekly（每天 00:20）：分类治理 + 剪枝 → MEMORY.md

**特点**：
- 事实源来自 session JSONL
- 去噪、防套娃、幂等
- Telegram 通知面板

---

## 四、快速上手方案

### 方案 A：零配置（新手推荐）

**步骤**：

1. 配置 API Key（任一）：
```bash
export OPENAI_API_KEY="sk-..."
```

2. 手动写入记忆：
告诉 AI："记住这个..."
AI 会自动写入 MEMORY.md

3. 搜索记忆：
AI 会自动使用 memory_search 查找

### 方案 B：QMD 高级搜索

**步骤**：

1. 安装 QMD：
```bash
bun install -g https://github.com/tobi/qmd
```

2. 配置：
```json
{
  "memory": {
    "backend": "qmd",
    "qmd": {
      "paths": [
        { "name": "notes", "path": "~/notes" }
      ],
      "sessions": { "enabled": true }
    }
  }
}
```

3. 重启：
```bash
openclaw gateway restart
```

### 方案 C：三层 Cron 自动记忆

**步骤**：

1. 克隆仓库：
```bash
cd ~/.openclaw/workspace
git clone https://github.com/dztabel-happy/openclaw-memory-fusion.git
```

2. 运行安装脚本：
```bash
bash scripts/setup.sh --tz Asia/Shanghai
```

---

## 五、最佳实践

### 写入规则

| 内容类型 | 写入位置 | 示例 |
|------|------|------|
| 决策、偏好、事实 | MEMORY.md | "用户喜欢 TypeScript" |
| 每日笔记 | memory/YYYY-MM-DD.md | "今天完成了 X 功能" |
| 临时观察 | memory/YYYY-MM-DD.md | "项目 A 正在迁移到 K8s" |

### 搜索优化

**Hybrid Search 权重调优**：
```json
{
  "memorySearch": {
    "query": {
      "hybrid": {
        "vectorWeight": 0.7,
        "textWeight": 0.3,
        "mmr": { "enabled": true, "lambda": 0.7 },
        "temporalDecay": { "enabled": true, "halfLifeDays": 30 }
      }
    }
  }
}
```

**参数说明**：
- vectorWeight 高：语义相似更重要
- textWeight 高：精确匹配更重要
- mmr.lambda：0 = 最大多样性，1 = 最大相关性
- halfLifeDays：每 N 天分数减半

### 索引额外目录

有项目文档在外面？配置一下：
```json
{
  "memorySearch": {
    "extraPaths": ["../team-docs", "/srv/shared-notes"]
  }
}
```

---

## 六、常用 CLI 命令

```bash
# 查看状态
openclaw memory status

# 搜索记忆
openclaw memory search "项目部署"

# 强制重建索引
openclaw memory index --force

# 查看 QMD 状态
openclaw memory status --agent main --index
```

---

## 七、总结：如何选择方案？

| 需求 | 推荐方案 |
|------|------|
| 快速上手 | Builtin + API Key |
| 需要搜索项目文档 | QMD + paths 配置 |
| 需要回忆历史对话 | QMD + sessions.enabled |
| 完全自动化记忆 | 三层 Cron 方案 |
| 多代理知识图谱 | Honcho |

---

**关键点**：

✅ 文件即记忆，只要写进文件就能记住
✅ 有 API Key 就能启用向量搜索
✅ 需要高级功能就用 QMD
✅ 想完全自动化就用三层 Cron

你的 AI 助手，从此拥有"长期记忆"！

---

**相关资源**：

- OpenClaw 官方文档：https://docs.openclaw.ai
- openclaw-memory-fusion：https://github.com/dztabel-happy/openclaw-memory-fusion
- QMD 项目：https://github.com/tobi/qmd
