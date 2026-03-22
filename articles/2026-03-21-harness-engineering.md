# 给 AI 套上缰绳：Harness Engineering 实战指南

## 你是不是也遇到过这些问题？

Claude Code 写代码很猛，但有时候像脱缰的野马——改错了文件、花了太多 token、甚至搞崩了项目...

要是能有个"缰绳"，既让它发挥能力，又能控制方向，该多好？

这就是 **Harness Engineering** 要解决的问题。

---

## 🎯 什么是 Harness Engineering？

**Harness = 缰绳 / 马具**

在 AI Agent 领域，Harness 指的是**控制/监督/编排 AI Agent 的框架层**——就像给野马套上缰绳，让 AI 按照预期方式工作。

核心目标：
- **可控** - 权限控制、预算限制、API 变更保护
- **可观测** - 实时日志、可视化监督
- **可扩展** - 多 worker 并行、动态扩展

---

## 📊 5 种主流 Harness 方案

### 1️⃣ cc-godmode - 最完善的质量门

**定位**：8 个专业化 Agent 编排，双质量门验证

**架构**：
```
用户 → @researcher → @architect → @builder → @validator + @tester → @scribe
                                    ↓
                              @api-guardian (API 变更必须经过)
```

**8 个专业化 Agent**：

| Agent | 角色 | 职责 |
|-------|------|------|
| @researcher | 知识发现 | 技术研究、文档查找 |
| @architect | 系统架构 | 架构设计、技术决策 |
| @api-guardian | API 生命周期 | API 变更影响分析 |
| @builder | 全栈开发 | 实现代码 |
| @validator | 代码质量 | TypeScript/测试/Lint |
| @tester | UX 质量 | E2E测试、性能、A11y |
| @scribe | 技术写作 | 文档更新、CHANGELOG |
| @github-manager | GitHub 管理 | Issue/PR/Release |

**核心特性**：
- ✅ 双质量门 - @validator 和 @tester 并行运行，40% 更快
- ✅ API 变更强制审批 - @api-guardian 必须参与
- ✅ 10 条黄金规则 - 严格的流程约束

**安装**：
```bash
npx clawhub@latest install cc-godmode
```

**适用场景**：需要严格质量控制的团队项目

---

### 2️⃣ claude-team - 最直观的可视化监督

**定位**：通过 iTerm2 编排多个 Claude Code worker

**核心能力**：
```
┌─────────────────────────────────────────────────┐
│  iTerm2 窗口                                     │
│  ┌─────────┬─────────┬─────────┬─────────┐      │
│  │ Groucho │ Harpo   │ Chico   │ Zeppo   │      │
│  │ (worker)│ (worker)│ (worker)│ (worker)│      │
│  └─────────┴─────────┴─────────┴─────────┘      │
└─────────────────────────────────────────────────┘
```

**核心特性**：
- ✅ 实时可见 - 真实的 Claude Code 终端会话，可随时介入
- ✅ Git Worktree - 每个 worker 独立分支，并行提交
- ✅ 上下文隔离 - coordinator 上下文干净，不污染

**安装**：
```bash
npx clawhub@latest install claude-team
# 需要配置 mcporter 和 iTerm2 Python API
```

**适用场景**：macOS 用户，需要可视化监督并行开发

---

### 3️⃣ codex-orchestration - 最轻量灵活

**定位**：PTY 后台运行 Codex workers，6 种工作流模式

**6 种编排模式**：

| 模式 | 流程 | 用例 |
|------|------|------|
| A: 三角评审 | reviewer × 3 → 合并 | 多角度审视 |
| B: 评审→修复 | reviewer → implementer → verifier | 清理漏斗 |
| C: 侦察→行动→验证 | scout → orchestrator → implementer → verifier | 缺乏上下文 |
| D: 分片处理 | worker × N → 合并 | 可分割工作 |
| E: 研究→综合 | researcher × N → synthesizer | 网络搜索 |
| F: 选项冲刺 | worker × N → 选择 | 方向决策 |

**核心原则**：
- 🎯 编排者不实现 - 只分解、监督、综合
- 🎯 并行读者，单一写者 - 避免冲突
- 🎯 精简计划 - 3-6 步，每步一句话

**安装**：
```bash
npx clawhub@latest install codex-orchestration
```

**适用场景**：熟悉命令行的用户，需要灵活编排

---

### 4️⃣ openclaw-claude-code-skill - 最深度集成

**定位**：通过 MCP 协议控制 Claude Code

**核心能力**：
- 🔌 MCP Protocol - 直接访问 Claude Code 所有工具
- 💾 持久化会话 - 跨多次交互保持上下文
- 🤝 Agent Teams - 部署多个专业化 Agent
- 🌐 多模型代理 - 支持 GPT-4o、Gemini 等替代
- 📊 Budget Limits - API 费用上限控制

**使用示例**：
```bash
# 启动持久会话
claude-code-skill session-start myproject -d ~/project \
  --permission-mode plan \
  --allowed-tools "Bash,Read,Edit,Write"

# 发送任务
claude-code-skill session-send myproject "Fix all TODOs" --stream

# 切换 agent
claude-code-skill session-send team "@developer implement the design"
claude-code-skill session-send team "@reviewer review the implementation"
```

**安装**：
```bash
git clone https://github.com/Enderfga/openclaw-claude-code-skill.git
cd openclaw-claude-code-skill
npm install && npm run build && npm link
```

**适用场景**：需要 MCP 深度集成或使用非 Anthropic 模型

---

### 5️⃣ coding-agent (OpenClaw 内置) - 最快速启动

**定位**：统一接口运行 Codex、Claude Code、OpenCode、Pi

**核心特性**：
- ✅ 已内置，无需额外安装
- ✅ 支持多种编码 Agent
- ✅ 简单直接

**使用方式**：
```bash
# 一键执行
bash pty:true workdir:~/project command:"claude 'Add error handling'"

# 后台运行长任务
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor auth'"

# 监控进度
process action:log sessionId:XXX
```

**适用场景**：快速启动编码任务

---

## 🔑 Harness 设计的 4 个核心原则

### 1. Orchestrator ≠ Implementer

编排者只分解、监督、综合，**不亲自实现**

就像项目经理不会自己写代码，但知道如何分配任务。

### 2. 并行读者，单一写者

- 多个 worker 可以并行**读取**代码
- 但**写入**必须串行或分片

避免多个 AI 同时改同一个文件导致冲突。

### 3. 质量门（Quality Gates）

```
代码 → @validator (TS/Lint/测试)
       @tester (E2E/性能/A11y)
            ↓
         并行验证
            ↓
         合并结果
```

**cc-godmode 的双质量门**比串行验证快 40%！

### 4. 上下文隔离

- 每个 worker 独立上下文
- 避免污染 orchestrator

这样 orchestrator 可以专注于调度，不会被大量代码细节淹没。

---

## 🆚 选型指南

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| 严格质量控制 | cc-godmode | 双质量门、API监护 |
| 可视化并行开发 | claude-team | iTerm2 可见、git worktree |
| 轻量灵活编排 | codex-orchestration | 6种模式、无依赖 |
| MCP 深度集成 | openclaw-claude-code-skill | MCP协议、多模型 |
| 快速启动 | coding-agent (内置) | 已安装、即用 |
| macOS 用户 | claude-team | iTerm2 集成 |
| Linux 用户 | codex-orchestration | 无 macOS 依赖 |

---

## 🚀 快速开始

### 最简单的方式（OpenClaw 内置）

```bash
# 一键启动 Claude Code
bash pty:true workdir:~/project command:"claude 'Add error handling'"
```

### 最高级的方式（cc-godmode）

```bash
npx clawhub@latest install cc-godmode
```

---

## 💡 总结

**Harness Engineering 的本质**：

> 构建一个**可控、可观测、可扩展**的 AI Agent 运行环境

**关键要素**：
1. 🎯 **可控** - 权限、预算、API 变更保护
2. 👀 **可观测** - 实时日志、可视化监督
3. 🔧 **可扩展** - 多 worker 并行、动态扩展

AI Agent 很强大，但需要 Harness 来约束和引导。就像野马需要缰绳才能跑得又快又稳。

---

**如果觉得有用，点个'在看'吧 👇**
