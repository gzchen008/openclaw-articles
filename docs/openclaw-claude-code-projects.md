# OpenClaw 控制 Claude Code 的开源项目

> 研究日期：2026-02-15
> 
> 核心需求：通过 OpenClaw **操作/控制/监督** Claude Code 去写代码

---

## 📊 项目总览

| 项目 | Stars | 控制方式 | 核心能力 |
|------|-------|----------|----------|
| [cc-godmode](#1-cc-godmode) | - | 8 Agent 编排 | 自动编排、双质量门、API监护 |
| [claude-team](#2-claude-team) | - | iTerm2 多窗口 | 并行 worker、git worktree、beads 集成 |
| [codex-orchestration](#3-codex-orchestration) | - | PTY 后台会话 | 并行子任务、工作流模式 |
| [openclaw-claude-code-skill](#4-openclaw-claude-code-skill) | 7 ⭐ | MCP 协议 | 会话管理、多模型代理、Agent Teams |
| [coding-agent (内置)](#5-coding-agent-内置技能) | - | PTY 后台 | 支持 Codex/CC/OpenCode/Pi |

---

## 🔍 详细对比

### 1. cc-godmode

**位置**: `openclaw/skills/skills/cubetribe/cc-godmode`

**定位**: 自编排多 Agent 开发工作流 —— **你说 WHAT，AI 决定 HOW**

**架构**:
```
                    ┌──▶ @validator (代码质量) ──┐
用户 ──▶ @researcher ──▶ @architect ──▶ @builder ──────────────────┼──▶ @scribe
                    └──▶ @tester (UX质量)   ──┘
                          (并行执行)
```

**8 个专业化 Agent**:

| Agent | 角色 | 模型 | 职责 |
|-------|------|------|------|
| `@researcher` | 知识发现 | haiku | 技术研究、文档查找 |
| `@architect` | 系统架构 | opus | 架构设计、技术决策 |
| `@api-guardian` | API 生命周期 | sonnet | API 变更影响分析 |
| `@builder` | 全栈开发 | sonnet | 实现代码 |
| `@validator` | 代码质量 | sonnet | TypeScript/测试/Lint |
| `@tester` | UX 质量 | sonnet | E2E测试、性能、A11y |
| `@scribe` | 技术写作 | sonnet | 文档更新、CHANGELOG |
| `@github-manager` | GitHub 管理 | haiku | Issue/PR/Release |

**核心特性**:
- ✅ **双质量门** - @validator 和 @tester 并行运行，40% 更快
- ✅ **API 变更强制审批** - @api-guardian 必须参与
- ✅ **版本优先** - 所有工作开始前先确定版本号
- ✅ **10 条黄金规则** - 严格的流程约束

**工作流模式**:

| 模式 | 流程 | 适用场景 |
|------|------|----------|
| **New Feature** | research → architect → builder → validator+tester → scribe | 新功能开发 |
| **Bug Fix** | builder → validator+tester | 快速修复 |
| **API Change** | architect → api-guardian → builder → ... | API 变更（必须过 api-guardian） |
| **Refactoring** | architect → builder → validator+tester | 重构 |
| **Release** | scribe → github-manager | 发布 |

**优势**:
- 🏆 最完善的监督体系
- 🏆 双质量门并行验证
- 🏆 API 变更保护机制

**劣势**:
- ⚠️ 流程较重，适合大型项目
- ⚠️ 需要 MCP 服务器（playwright、github 等）

**适用场景**: 需要严格质量控制的团队项目

---

### 2. claude-team

**位置**: `openclaw/skills/skills/jalehman/claude-team`
**GitHub**: https://github.com/Martian-Engineering/claude-team

**定位**: 通过 iTerm2 编排多个 Claude Code worker，支持 git worktree 并行开发

**核心能力**:
```
┌─────────────────────────────────────────────────┐
│  iTerm2 窗口                                     │
│  ┌─────────┬─────────┬─────────┬─────────┐      │
│  │ Groucho │ Harpo   │ Chico   │ Zeppo   │      │
│  │ (worker)│ (worker)│ (worker)│ (worker)│      │
│  │ bead:A  │ bead:B  │ bead:C  │ bead:D  │      │
│  └─────────┴─────────┴─────────┴─────────┘      │
└─────────────────────────────────────────────────┘
        │
        ▼
   mcporter call claude-team.*
```

**核心工具** (通过 `mcporter call claude-team.<tool>`):

| 工具 | 功能 |
|------|------|
| `spawn_workers` | 创建多个 Claude Code worker |
| `list_workers` | 列出所有 worker |
| `message_workers` | 向 worker 发送消息 |
| `check_idle_workers` | 检查 worker 是否空闲 |
| `wait_idle_workers` | 等待 worker 完成 |
| `read_worker_logs` | 读取 worker 日志 |
| `examine_worker` | 详细状态 |
| `close_workers` | 关闭 worker |

**并行开发流程**:
```bash
# 1. 启动多个 worker 并行处理不同任务
mcporter call claude-team.spawn_workers \
  workers='[
    {"project_path": "auto", "bead": "cp-123", "annotation": "Auth module"},
    {"project_path": "auto", "bead": "cp-124", "annotation": "API routes"},
    {"project_path": "auto", "bead": "cp-125", "annotation": "Unit tests"}
  ]' \
  layout="new"

# 2. 等待所有完成
mcporter call claude-team.wait_idle_workers \
  session_ids='["Groucho","Harpo","Chico"]' \
  mode="all"

# 3. 关闭并合并
mcporter call claude-team.close_workers \
  session_ids='["Groucho","Harpo","Chico"]'
```

**核心特性**:
- ✅ **实时可见** - 真实的 Claude Code 终端会话，可随时介入
- ✅ **Git Worktree** - 每个 worker 独立分支，并行提交
- ✅ **Beads 集成** - 自动关联 issue、标记状态、关闭 issue
- ✅ **上下文隔离** - coordinator 上下文干净，不污染

**优势**:
- 🏆 最直观的可视化监督
- 🏆 真正的并行开发能力
- 🏆 可随时接管 worker

**劣势**:
- ⚠️ 只支持 macOS + iTerm2
- ⚠️ 需要配置 mcporter

**适用场景**: macOS 用户，需要可视化监督并行开发

---

### 3. codex-orchestration

**位置**: `openclaw/skills/skills/shanelindsay/codex-orchestration`

**定位**: 通用编排，用 PTY 后台运行 Codex workers

**核心模式**: Orchestrator（编排者） + Workers（执行者）

**编排模式**:

| 模式 | 流程 | 适用场景 |
|------|------|----------|
| **A: 三角评审** | 多 reviewer → 合并 | 多角度审视同一产物 |
| **B: 评审→修复** | reviewer → implementer → verifier | 清理漏斗 |
| **C: 侦察→行动→验证** | scout → orchestrator → implementer → verifier | 缺乏上下文时 |
| **D: 分片处理** | 每个 worker 一块 → 合并 | 可分割的工作 |
| **E: 研究→综合** | 多 researcher → synthesizer | 网络搜索任务 |
| **F: 选项冲刺** | 多 worker 生成选项 → 选择 | 方向决策 |

**Worker 启动方式**:
```bash
codex exec --skip-git-repo-check --output-last-message /tmp/w1.txt "CONTEXT: WORKER
ROLE: You are a sub-agent run by the ORCHESTRATOR. Do only the assigned task.
RULES: No extra scope, no other workers.
Your final output will be provided back to the ORCHESTRATOR.
TASK: <what to do>
SCOPE: read-only"
```

**核心原则**:
- 🎯 **编排者不实现** - 只分解、监督、综合
- 🎯 **并行读者，单一写者** - 避免冲突
- 🎯 **精简计划** - 3-6 步，每步一句话
- 🎯 **上下文包** - 给 worker 提供必要上下文

**优势**:
- 🏆 最轻量
- 🏆 模式丰富
- 🏆 不依赖额外工具

**劣势**:
- ⚠️ 无可视化界面
- ⚠️ 需要手动管理会话

**适用场景**: 熟悉命令行的用户，需要灵活编排

---

### 4. openclaw-claude-code-skill

**GitHub**: https://github.com/Enderfga/openclaw-claude-code-skill
**Stars**: 7 ⭐
**语言**: JavaScript
**创建时间**: 2026-01-30

**定位**: 通过 MCP 协议控制 Claude Code

**核心能力**:
- 🔌 **MCP Protocol** - 直接访问 Claude Code 所有工具
- 💾 **持久化会话** - 跨多次交互保持上下文
- 🤝 **Agent Teams** - 部署多个专业化 Agent
- 🌐 **多模型代理** - 支持 GPT-4o、Gemini 等替代
- 📊 **Budget Limits** - API 费用上限控制

**会话管理**:
```bash
# 启动持久会话
claude-code-skill session-start myproject -d ~/project \
  --permission-mode plan \
  --allowed-tools "Bash,Read,Edit,Write"

# 发送任务
claude-code-skill session-send myproject "Fix all TODOs" --stream

# 会话操作
claude-code-skill session-list
claude-code-skill session-history myproject -n 50
claude-code-skill session-fork myproject exp
claude-code-skill session-pause myproject
claude-code-skill session-resume-paused myproject
```

**多模型支持**:
```bash
# 使用 Gemini
claude-code-skill session-start gemini-task -d ~/project \
  --model gemini-2.0-flash \
  --base-url http://127.0.0.1:8082

# 使用 GPT-4o
claude-code-skill session-start gpt-task -d ~/project \
  --model gpt-4o \
  --base-url https://api.openai.com/v1
```

**Agent Teams**:
```bash
claude-code-skill session-start team -d ~/project \
  --agents '{
    "architect": {"prompt": "Design system architecture"},
    "developer": {"prompt": "Implement features"},
    "reviewer": {"prompt": "Review code quality"}
  }' \
  --agent architect

# 切换 agent
claude-code-skill session-send team "@developer implement the design"
claude-code-skill session-send team "@reviewer review the implementation"
```

**权限模式**:

| 模式 | 说明 |
|------|------|
| `acceptEdits` | 自动接受文件编辑（默认） |
| `plan` | 预览变更后再应用 |
| `default` | 每次操作询问 |
| `bypassPermissions` | 跳过所有提示（危险！） |

**优势**:
- 🏆 真正的 MCP 集成
- 🏆 支持多模型后端
- 🏆 会话 fork/pause/resume/search

**劣势**:
- ⚠️ 非常新（2026-01-30）
- ⚠️ 需要单独部署后端服务
- ⚠️ Stars 少，生态不成熟

**适用场景**: 需要 MCP 深度集成或使用非 Anthropic 模型

---

### 5. coding-agent (内置技能)

**位置**: OpenClaw 内置技能

**定位**: 统一接口运行 Codex、Claude Code、OpenCode、Pi

**支持**:
- ✅ Codex CLI (OpenAI)
- ✅ Claude Code (Anthropic)
- ✅ OpenCode
- ✅ Pi Coding Agent

**关键点**:
- ⚠️ **必须用 `pty:true`** - 编码 Agent 需要 PTY 终端
- `workdir` 隔离 - Agent 只看目标目录
- `background:true` - 后台运行长任务

**使用方式**:
```bash
# 一键执行
bash pty:true workdir:~/project command:"claude 'Add error handling'"

# 后台长任务
bash pty:true workdir:~/project background:true command:"codex --yolo 'Refactor auth'"

# 监控进度
process action:log sessionId:XXX
process action:poll sessionId:XXX
```

**并行 git worktree**:
```bash
# 创建多个 worktree
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

# 并行运行
bash pty:true workdir:/tmp/issue-78 background:true command:"codex --yolo 'Fix #78'"
bash pty:true workdir:/tmp/issue-99 background:true command:"codex --yolo 'Fix #99'"
```

**优势**:
- 🏆 已内置，无需额外安装
- 🏆 支持多种编码 Agent
- 🏆 简单直接

**劣势**:
- ⚠️ 无高级编排功能
- ⚠️ 需要手动管理会话

**适用场景**: 快速启动编码任务

---

## 🆚 选型指南

| 场景 | 推荐方案 | 理由 |
|------|----------|------|
| **严格质量控制** | cc-godmode | 双质量门、API监护 |
| **可视化并行开发** | claude-team | iTerm2 可见、git worktree |
| **轻量灵活编排** | codex-orchestration | 6种模式、无依赖 |
| **MCP 深度集成** | openclaw-claude-code-skill | MCP协议、多模型 |
| **快速启动** | coding-agent (内置) | 已安装、即用 |
| **macOS 用户** | claude-team | iTerm2 集成 |
| **Linux 用户** | codex-orchestration 或 coding-agent | 无 macOS 依赖 |

---

## 📦 安装命令

### cc-godmode
```bash
npx clawhub@latest install cc-godmode
```

### claude-team
```bash
npx clawhub@latest install claude-team
# 需要配置 mcporter 和 iTerm2 Python API
```

### codex-orchestration
```bash
npx clawhub@latest install codex-orchestration
```

### openclaw-claude-code-skill
```bash
git clone https://github.com/Enderfga/openclaw-claude-code-skill.git
cd openclaw-claude-code-skill
npm install && npm run build && npm link
```

---

## 🔗 相关链接

- **OpenClaw 官方技能仓库**: https://github.com/openclaw/skills
- **ClawHub**: https://www.clawhub.ai
- **cc-godmode SKILL.md**: https://github.com/openclaw/skills/tree/main/skills/cubetribe/cc-godmode
- **claude-team GitHub**: https://github.com/Martian-Engineering/claude-team
- **openclaw-claude-code-skill**: https://github.com/Enderfga/openclaw-claude-code-skill

---

*文档维护：小J | 最后更新：2026-02-15*
