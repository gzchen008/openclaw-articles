# OpenClaw 多 Agent 配置 - 多员工应用场景对照

> 基于官方文档整理，将多 agent 架构映射到企业"多员工"场景

---

## 🏢 核心架构：Coordinator-Worker 模式

### 架构设计

```
┌─────────────────────────────────────────────────────┐
│                  Coordinator Agent                   │
│              (老板/CEO - 长期运行)                    │
│                                                      │
│  • 与人类沟通，接收任务                               │
│  • 分析任务，分配给合适的员工                         │
│  • 汇总结果，回复用户                                │
│  • 维护 MEMORY.md 作为长期记忆                       │
└───────────────────┬─────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Agent 1 │ │ Agent 2 │ │ Agent 3 │
   │ (内容)  │ │ (开发)  │ │ (数据)  │
   └─────────┘ └─────────┘ └─────────┘
        │           │           │
        └───────────┼───────────┘
                    ▼
            任务完成后退出
          (结果返回 Coordinator)
```

### 员工对照表

| 企业角色 | OpenClaw Agent | 会话类型 | 运行模式 |
|---------|---------------|---------|---------|
| CEO/老板 | Coordinator Agent | Main Session | 长期运行 |
| 内容团队 | Content Agent | Subagent | 按需启动 |
| 开发团队 | Dev Agent | Subagent | 按需启动 |
| 数据分析师 | Analyst Agent | Subagent | 按需启动 |
| 运维/定时任务 | Cron Agent | Isolated Session | 定时触发 |

---

## 📁 文件结构：每个"员工"有独立工位

```bash
~/.openclaw/
├── agents/
│   ├── jarvis/              # Coordinator (老板)
│   │   ├── SOUL.md          # 人格：决策者、协调者
│   │   ├── MEMORY.md        # 长期记忆
│   │   └── workspace/
│   │
│   ├── content-bot/         # 内容团队
│   │   ├── SOUL.md          # 人格：文案专家
│   │   └── workspace/
│   │       └── articles/
│   │
│   ├── dev-bot/             # 开发团队
│   │   ├── SOUL.md          # 人格：程序员
│   │   └── workspace/
│   │       └── projects/
│   │
│   └── analyst-bot/         # 数据分析
│       ├── SOUL.md          # 人格：数据分析师
│       └── workspace/
│           └── reports/
```

---

## ⚙️ 配置方法

### 1. 基础配置 (openclaw.json)

```json5
{
  agents: {
    defaults: {
      model: {
        primary: "zai/glm-5",
        fallbacks: ["zai/glm-4.7", "minimax/MiniMax-M2.5"]
      },
      subagents: {
        // 子 agent 配置（员工设置）
        maxConcurrent: 8,        // 最多 8 个员工同时工作
        maxSpawnDepth: 2,        // 允许 2 层嵌套（经理→员工→实习生）
        maxChildrenPerAgent: 5,  // 每个 agent 最多管理 5 个下属
        model: "zai/glm-4.7",    // 员工用更便宜的模型
      },
    },
    
    // 具体的 agent 定义
    list: [
      {
        id: "jarvis",
        name: "Jarvis (协调者)",
        workspace: "/Users/cgz/.openclaw/agents/jarvis/workspace",
        // 可以覆盖默认配置
      },
      {
        id: "content-bot",
        name: "Content Bot (内容团队)",
        subagents: {
          model: "zai/glm-4.7-flash",  // 内容创作用快速模型
        }
      }
    ]
  }
}
```

### 2. 启动 Coordinator

```bash
# 注册 agent
openclaw agents add jarvis --workspace ~/.openclaw/agents/jarvis/workspace

# 启动 gateway（老板开始上班）
openclaw gateway start
```

### 3. 分配任务给员工

**方式 1：自动分配（推荐）**
Coordinator 收到任务后，自动判断应该分配给哪个 subagent：

```markdown
用户：帮我写一篇公众号文章

Coordinator (Jarvis)：
  → 自动调用 sessions_spawn
  → 启动 content-bot subagent
  → content-bot 完成后返回结果
  → Coordinator 汇总并回复用户
```

**方式 2：手动指定**

```bash
# Discord/Telegram 中
/subagents spawn content-bot "写一篇关于 AI Agent 的文章"
```

---

## 🔄 嵌套架构：经理→员工→实习生

当 `maxSpawnDepth: 2` 时，支持 3 层架构：

```
Depth 0: Main Session (Coordinator/老板)
    ↓ spawn
Depth 1: Subagent (经理/Team Lead)
    ↓ spawn (需要权限)
Depth 2: Sub-subagent (实习生/Junior)
```

### 场景示例

```
用户：帮我完成整个内容项目

Coordinator (Depth 0)
  → 分配给 Content Lead (Depth 1)
      → Content Lead 分配给：
          → Writer Bot (写初稿)
          → Editor Bot (审核)
          → SEO Bot (优化)
      → 汇总结果返回 Coordinator
  → Coordinator 返回用户
```

---

## 📊 多员工应用场景对照

### 场景 1：内容创作团队

| 角色 | Agent ID | 职责 | 模型建议 |
|-----|---------|------|---------|
| 内容总监 | content-lead | 规划选题、分配任务 | glm-5（高质量） |
| 写手 | writer-bot | 撰写文章初稿 | glm-4.7-flash（快速） |
| 编辑 | editor-bot | 润色、校对 | glm-5（精准） |
| SEO专员 | seo-bot | 关键词优化 | glm-4.7（标准） |

**工作流程**：
```
用户需求 → Content Lead (Depth 0)
           ↓
       Writer Bot (Depth 1) → Editor Bot (Depth 1) → SEO Bot (Depth 1)
           ↓
       汇总结果返回用户
```

### 场景 2：开发团队

| 角色 | Agent ID | 职责 |
|-----|---------|------|
| Tech Lead | dev-lead | 架构设计、代码审查 |
| Frontend | frontend-bot | 前端开发 |
| Backend | backend-bot | 后端开发 |
| QA | qa-bot | 测试、Bug 修复 |

### 场景 3：个人助理团队

| 角色 | Agent ID | 职责 |
|-----|---------|------|
| 助理 | assistant | 日程管理、邮件处理 |
| 研究员 | researcher | 信息搜索、整理 |
| 秘书 | secretary | 文档整理、提醒 |

---

## 🎯 最佳实践

### 1. 模型选择策略

```json5
// 不同角色用不同模型（成本优化）
{
  agents: {
    list: [
      {
        id: "coordinator",
        model: { primary: "zai/glm-5" },  // 决策用最强模型
      },
      {
        id: "worker",
        model: { primary: "zai/glm-4.7-flash" },  // 执行用快速模型
      }
    ]
  }
}
```

### 2. 工具权限控制

```json5
{
  tools: {
    subagents: {
      tools: {
        // 限制员工只能使用特定工具
        deny: ["gateway", "cron"],  // 不能重启系统
        allow: ["read", "write", "exec", "web_search"],  // 只能干活
      }
    }
  }
}
```

### 3. 防止 Context Overflow

```bash
# 启用自动压缩
openclaw config set agent.compaction.enabled true
openclaw config set agent.compaction.threshold 50000
```

### 4. 定期任务用 Isolated Session

```json5
// cron 配置（独立会话，完成后退出）
{
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    message: "生成每日报告"
  }
}
```

---

## 🚀 快速启动模板

### 创建 3 人团队（协调者+内容+开发）

```bash
# 1. 创建目录结构
mkdir -p ~/.openclaw/agents/{jarvis,content-bot,dev-bot}/workspace

# 2. 创建人格文件
cat > ~/.openclaw/agents/jarvis/SOUL.md << 'EOF'
# Jarvis - 协调者

你是团队的协调者，负责：
- 接收用户任务
- 分析并分配给合适的员工
- 汇总结果回复用户

你有两个团队成员：
- content-bot: 负责内容创作
- dev-bot: 负责技术开发
EOF

cat > ~/.openclaw/agents/content-bot/SOUL.md << 'EOF'
# Content Bot - 内容专家

你是一名内容创作专家，擅长：
- 撰写公众号文章
- 社交媒体文案
- SEO 优化

专注于高质量内容输出。
EOF

cat > ~/.openclaw/agents/dev-bot/SOUL.md << 'EOF'
# Dev Bot - 开发专家

你是一名全栈开发者，擅长：
- 前端/后端开发
- 代码审查
- Bug 修复

专注于代码质量和最佳实践。
EOF

# 3. 注册 agents
openclaw agents add jarvis --workspace ~/.openclaw/agents/jarvis/workspace
openclaw agents add content-bot --workspace ~/.openclaw/agents/content-bot/workspace
openclaw agents add dev-bot --workspace ~/.openclaw/agents/dev-bot/workspace

# 4. 启动
openclaw gateway start
```

---

## 📝 常用命令

```bash
# 查看所有 agents
openclaw agents list

# 查看 subagent 运行状态（在聊天中）
/subagents list

# 手动分配任务
/subagents spawn content-bot "写一篇文章"

# 查看任务日志
/subagents log <id>

# 停止任务
/subagents kill <id>

# 配置多模型
openclaw configure models
```

---

## ⚠️ 注意事项

1. **Sub-agent 有独立 Context**：每个 subagent 的 token 消耗是独立的
2. **Announce 是 Best-effort**：如果 gateway 重启，pending 结果可能丢失
3. **最大嵌套 5 层**：推荐使用 2 层（Coordinator → Worker）
4. **Auth 共享**：Subagent 继承 main agent 的 auth profiles
5. **Memory 隔离**：Subagent 只能看到 AGENTS.md + TOOLS.md，看不到 SOUL.md

---

## 📚 参考资源

- [Sub-Agents 官方文档](https://docs.openclaw.ai/tools/subagents)
- [Multi-Agent Architecture Best Practices](https://www.getopenclaw.ai/help/multi-agent-architecture)
- [Build AI Team in 15 Minutes](https://ai2sql.io/how-to-build-your-own-ai-agent-team-with-openclaw-in-15-minutes)

---

*整理时间：2026-02-20*
