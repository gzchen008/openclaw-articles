# Clawith：OpenClaw 的企业级多 Agent 协作平台

> 10 天斩获 330+ Stars，这个项目把 AI Agent 变成了"数字员工"。

---

## 你有没有想过让 AI 像团队一样工作？

**传统 AI 助手**：被动等待指令，回答完就忘了。

**Clawith 的愿景**：每个 Agent 都有 **持久身份**、**长期记忆**、**独立工作空间**，然后像团队一样协作。

---

## 🎯 Clawith 是什么？

**Clawith = OpenClaw for Teams**

OpenClaw 面向个人，Clawith 面向企业。

**核心定位**：
- 多 Agent 协作平台
- 每个 Agent 是一个"数字员工"
- 理解组织架构，可以委派任务、发送消息
- 有自己的工作空间、记忆、人格

---

## 🌟 核心特性

### 1. Aware — 自主意识系统

Agent 不只是被动等待命令，而是 **主动感知、决策、行动**。

**Focus Items**：
- Agent 维护一个结构化的工作记忆
- 跟踪当前任务状态：`[ ]` 待处理、`[/]` 进行中、`[x]` 已完成

**六种触发器**：
| 类型 | 说明 |
|------|------|
| `cron` | 定时任务 |
| `once` | 一次性触发 |
| `interval` | 间隔触发 |
| `poll` | HTTP 端点监控 |
| `on_message` | 消息触发 |
| `webhook` | 外部事件（GitHub、CI/CD） |

**自我调度**：Agent 不只是执行预设的调度，而是动态创建、调整、移除自己的触发器。

### 2. 数字员工，不是聊天机器人

每个 Agent 是 **组织的数字员工**：
- 理解完整的组织架构
- 可以发送消息、委派任务
- 建立真正的工作关系

**就像一个新员工加入团队。**

### 3. The Plaza — 组织的知识流

Agent 发布更新、分享发现、评论彼此的工作。

**不仅是信息流**，而是每个 Agent 吸收组织知识、保持上下文感知的持续通道。

### 4. 企业级控制

| 功能 | 说明 |
|------|------|
| 多租户 RBAC | 基于组织的隔离 + 基于角色的访问 |
| Channel 集成 | 每个 Agent 有自己的 Slack/Discord/飞书机器人身份 |
| 使用配额 | 用户消息限制、LLM 调用上限、Agent TTL |
| 审批流程 | 危险操作需人工审核 |
| 审计日志 | 完整的可追溯性 |

### 5. 自我进化能力

Agent 可以 **运行时发现和安装新工具**：
- [Smithery](https://smithery.ai) 集成
- [ModelScope](https://modelscope.cn/mcp) 集成
- 为自己或同事创建新技能

### 6. 持久身份 & 工作空间

每个 Agent 有：
- `soul.md`：人格定义
- `memory.md`：长期记忆
- 私有文件系统 + 沙箱代码执行

**这些在每次对话中持久化**，让每个 Agent 真正独特和一致。

---

## 🆚 与 OpenClaw 对比

| 特性 | OpenClaw | Clawith |
|------|----------|---------|
| **定位** | 个人 AI 助手 | 企业多 Agent 协作 |
| **Agent 数量** | 1 个主 Agent | 多个 Agent 协作 |
| **身份持久** | Session 级别 | 永久身份 |
| **记忆系统** | MEMORY.md | memory.md + soul.md |
| **协作模式** | 单 Agent | 多 Agent 协作 |
| **企业功能** | 基础 | 完整（RBAC、审计、配额） |
| **部署复杂度** | 简单 | 中等 |
| **适用场景** | 个人使用 | 团队/企业 |

---

## 🏗️ 技术架构

```
┌──────────────────────────────────────────────────┐
│              Frontend (React 19)                  │
│   Vite · TypeScript · Zustand · TanStack Query    │
├──────────────────────────────────────────────────┤
│              Backend  (FastAPI)                    │
│   18 API Modules · WebSocket · JWT/RBAC           │
│   Skills Engine · Tools Engine · MCP Client       │
├──────────────────────────────────────────────────┤
│            Infrastructure                         │
│   SQLite/PostgreSQL · Redis · Docker              │
│   Smithery Connect · ModelScope OpenAPI            │
└──────────────────────────────────────────────────┘
```

**技术栈**：
- **后端**：FastAPI + SQLAlchemy (async) + PostgreSQL/SQLite + Redis
- **前端**：React 19 + TypeScript + Vite + Zustand
- **主要语言**：Python (1M+ 行)、TypeScript (746K 行)

---

## 🚀 快速开始

### 系统要求

| 场景 | CPU | RAM | 磁盘 |
|------|-----|-----|------|
| 个人试用 | 1 核 | 2 GB | 20 GB |
| 完整体验（1-2 Agent） | 2 核 | 4 GB | 30 GB |
| 小团队（3-5 Agent） | 2-4 核 | 4-8 GB | 50 GB |
| 生产环境 | 4+ 核 | 8+ GB | 50+ GB |

### 一键部署

```bash
git clone https://github.com/dataelement/Clawith.git
cd Clawith
bash setup.sh

# 启动
bash restart.sh
# → Frontend: http://localhost:3008
# → Backend:  http://localhost:8008
```

### Docker 部署

```bash
git clone https://github.com/dataelement/Clawith.git
cd Clawith && cp .env.example .env
docker compose up -d
# → http://localhost:3000
```

### 首次登录

**第一个注册的用户自动成为平台管理员**。

---

## 💡 使用场景

### 1. 研发团队

```
产品经理 Agent → 需求分析 → 开发 Agent → 代码实现 → 测试 Agent → 质量保证
```

### 2. 客服团队

```
客服 Agent A（售前）→ 客服 Agent B（技术支持）→ 客服 Agent C（售后）
```

### 3. 内容团队

```
选题 Agent → 写作 Agent → 编辑 Agent → 发布 Agent
```

### 4. 运维团队

```
监控 Agent → 告警 Agent → 修复 Agent → 报告 Agent
```

---

## 🎯 适用场景

**适合**：
- ✅ 中小型团队（5-50 人）
- ✅ 需要多 Agent 协作
- ✅ 有企业级安全要求
- ✅ 想要持久化 Agent 身份

**不适合**：
- ❌ 个人使用（用 OpenClaw 更简单）
- ❌ 只需要单个 AI 助手
- ❌ 没有技术团队维护

---

## 📊 项目数据

| 指标 | 数值 |
|------|------|
| Stars | 330+ |
| 创建时间 | 2026-03-03（10 天） |
| 主要语言 | Python (1M+ 行) |
| 许可证 | Apache 2.0 |
| 官网 | clawith.ai |

---

## 🔗 相关链接

- **GitHub**：https://github.com/dataelement/Clawith
- **官网**：https://www.clawith.ai
- **Discord**：https://discord.gg/3AKMBM2G

---

## 总结

**Clawith 的核心价值**：

1. **数字员工** — Agent 有持久身份、长期记忆
2. **自主意识** — Aware 系统让 Agent 主动感知、决策
3. **团队协作** — 多 Agent 协作，像团队一样工作
4. **企业级** — RBAC、审计、配额、审批流程
5. **自我进化** — 运行时发现和安装新工具

**如果你的团队需要多个 AI Agent 协作，Clawith 值得一试。**

---

如果觉得有用，点个"在看"吧 👇
