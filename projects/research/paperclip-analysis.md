# Paperclip 深度研究报告

**研究日期**：2026-03-16  
**项目地址**：https://github.com/paperclipai/paperclip  
**官网**：https://paperclip.ing  
**最新版本**：v0.3.1（2026-03-12 发布）  
**Stars**：⭐ 24,886  

---

## 📌 核心定位

> **If OpenClaw is an _employee_, Paperclip is the _company_**

Paperclip 是一个开源的 AI Agent 编排平台，用于构建"零人工公司"。它不是一个 Agent 框架，而是一个公司运营系统——协调多个 AI Agent（OpenClaw、Codex、Claude Code、Cursor 等）像一个真正的公司一样运作。

**核心理念**：
- 不是管理 Pull Requests，而是管理业务目标
- 不是 Chatbot，而是有工作职责的员工
- 不是单一 Agent，而是有组织架构的团队

---

## 🎯 解决的问题

### 没有 Paperclip 的痛点
| 痛点 | 描述 |
|------|------|
| ❌ 管理混乱 | 20个 Claude Code 标签页打开，无法追踪谁在做什么 |
| ❌ 上下文丢失 | 重启后所有状态丢失，需要手动恢复上下文 |
| ❌ 成本失控 | Agent 无限循环浪费数百美元 Token |
| ❌ 缺乏协调 | 文件夹里的 Agent 配置混乱，重复造轮子 |
| ❌ 需要人工干预 | 定期任务（客服、社交媒体、报告）需要手动启动 |

### 有 Paperclip 的解决方案
| 解决方案 | 价值 |
|----------|------|
| ✅ Ticket 系统 | 任务基于 Ticket，对话线程化，会话持久化 |
| ✅ 目标对齐 | 上下文从任务流向项目和公司目标 |
| ✅ 成本控制 | Token 预算追踪，超出预算自动停止 |
| ✅ 组织架构 | 自带组织架构、Ticket 系统、委派、治理 |
| ✅ 心跳机制 | 定期工作自动执行，管理层监督 |

---

## 🏗️ 核心功能

### 1. 🔌 Bring Your Own Agent（自带 Agent）
- 支持任何 Agent：OpenClaw、Claude Code、Codex、Cursor、Bash、HTTP
- 只要能接收心跳，就可以被雇佣
- 统一的组织架构管理

### 2. 🎯 Goal Alignment（目标对齐）
- 每个任务追溯到公司使命
- Agent 知道"做什么"和"为什么做"
- 目标层次：Company → Project → Task

### 3. 💓 Heartbeats（心跳机制）
- Agent 按计划唤醒
- 检查工作并采取行动
- 委派流向上下级

### 4. 💰 Cost Control（成本控制）
- 每个 Agent 月度预算
- 达到限制时停止
- 防止成本失控

### 5. 🏢 Multi-Company（多公司）
- 一个部署，多个公司
- 完全数据隔离
- 一个控制面板管理投资组合

### 6. 🎫 Ticket System（工单系统）
- 每个对话可追溯
- 每个决策有解释
- 完整工具调用追踪和审计日志

### 7. 🛡️ Governance（治理）
- 你是董事会
- 批准雇佣、覆盖策略、暂停或终止任何 Agent
- 配置变更有版本控制，可回滚

### 8. 📊 Org Chart（组织架构）
- 层级、角色、汇报线
- Agent 有老板、头衔、职位描述

### 9. 📱 Mobile Ready（移动端支持）
- 从任何地方监控和管理自主业务

---

## 🔧 技术架构

### 技术栈
| 组件 | 技术 |
|------|------|
| 后端 | Node.js + Express |
| 前端 | React + Vite |
| 数据库 | PostgreSQL（开发用 PGlite 嵌入式） |
| ORM | Drizzle |
| 语言 | TypeScript |

### 项目结构
```
paperclip/
├── server/          # Express REST API 和编排服务
├── ui/              # React + Vite 看板 UI
├── packages/db/     # Drizzle schema、迁移、DB 客户端
├── packages/shared/ # 共享类型、常量、验证器
├── doc/             # 运营和产品文档
└── cli/             # 命令行工具
```

### 关键技术特性
| 特性 | 说明 |
|------|------|
| **原子执行** | 任务检出和预算强制是原子的，防止重复工作和成本失控 |
| **持久化 Agent 状态** | Agent 在心跳之间恢复相同的任务上下文 |
| **运行时技能注入** | Agent 在运行时学习 Paperclip 工作流和项目上下文 |
| **目标感知执行** | 任务携带完整的目标祖先，Agent 始终看到"为什么" |
| **可移植公司模板** | 导出/导入组织、Agent 和技能，自动清理密钥 |
| **真正的多公司隔离** | 每个实体都有公司作用域 |

---

## 🚀 快速开始

### 方式 1：一键启动
```bash
npx paperclipai onboard --yes
```

### 方式 2：手动安装
```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

**启动后**：
- API 服务器：`http://localhost:3100`
- 自动创建嵌入式 PostgreSQL 数据库（无需设置）

**要求**：Node.js 20+, pnpm 9.15+

### 开发命令
```bash
pnpm dev              # 完整开发（API + UI，watch 模式）
pnpm dev:once         # 完整开发（无文件监视）
pnpm dev:server       # 仅服务器
pnpm build            # 构建所有
pnpm typecheck        # 类型检查
pnpm test:run         # 运行测试
pnpm db:generate      # 生成 DB 迁移
pnpm db:migrate       # 应用迁移
```

---

## 🆚 与 OpenClaw 的关系

### 定位对比
| 项目 | 定位 | 关系 |
|------|------|------|
| **OpenClaw** | AI 员工（个人助手） | 被 Paperclip 编排 |
| **Paperclip** | AI 公司（组织管理） | 编排多个 Agent |

### Paperclip 不是什么
| 不是 | 说明 |
|------|------|
| ❌ 不是 Chatbot | Agent 有工作，不是聊天窗口 |
| ❌ 不是 Agent 框架 | 不告诉你如何构建 Agent，而是如何运营由 Agent 组成的公司 |
| ❌ 不是工作流构建器 | 没有拖拽式管道，而是模拟公司（组织架构、目标、预算、治理） |
| ❌ 不是提示词管理器 | Agent 自带提示词、模型、运行时，Paperclip 管理组织 |
| ❌ 不是单 Agent 工具 | 用于团队，一个 Agent 不需要 Paperclip，20 个就需要 |
| ❌ 不是代码审查工具 | 编排工作，不是 Pull Requests |

### 为什么不用 Asana/Trello + OpenClaw？
Agent 编排在以下方面有微妙之处：
- 协调谁检出了工作
- 如何维护会话
- 监控成本
- 建立治理

Paperclip 为你处理这些。

---

## 📈 最新版本亮点（v0.3.1）

**发布日期**：2026-03-12（4天前）

### 新功能
1. **Gemini CLI 适配器** - 完整支持 Google Gemini CLI
2. **运行转录优化** - Markdown 渲染、命令输出折叠、敏感信息脱敏
3. **收件箱改进** - 标签行为、徽章计数、移动端布局优化
4. **改进的入职向导** - Claude Code 和 Codex 作为推荐适配器

### 改进
- 实例心跳设置侧边栏
- 项目和 Agent 配置标签页
- Agent 运行标签页
- 可配置附件内容类型（`PAPERCLIP_ALLOWED_ATTACHMENT_TYPES`）
- 默认最大 turns 提升到 300
- 问题创建者显示在侧边栏
- Worktree 工作流支持（隔离开发实例）

### 修复
- Gemini Docker 构建
- 批准重试幂等性
- 心跳成本记录
- Claude Code 环境变量泄漏
- IME 组合 Enter 键问题
- 默认跳过权限（无人值守 Agent）

---

## 🔮 路线图

| 状态 | 功能 |
|------|------|
| ⚪ | 简化 OpenClaw 入职 |
| ⚪ | 支持云端 Agent（Cursor / e2b agents） |
| ⚪ | **ClipMart** - 一键下载并运行整个公司 |
| ⚪ | 简化 Agent 配置 |
| ⚪ | 更好的 harness 工程支持 |
| 🟢 | 插件系统（知识库、自定义追踪、队列等） |
| ⚪ | 更好的文档 |

**ClipMart**（即将推出）：浏览预构建的公司模板（完整的组织结构、Agent 配置、技能），一键导入到 Paperclip 实例。

---

## 💡 使用场景

### 适合 Paperclip 的场景
- ✅ 构建自主 AI 公司
- ✅ 协调多个 Agent（OpenClaw、Codex、Claude、Cursor）朝共同目标工作
- ✅ 同时打开 20 个 Claude Code 终端，不知道谁在做什么
- ✅ Agent 24/7 自主运行，但需要审计工作并在需要时介入
- ✅ 监控成本并强制预算
- ✅ 想要一个感觉像任务管理器的 Agent 管理流程
- ✅ 从手机管理自主业务

### 典型设置
1. **本地开发**：单个 Node.js 进程管理嵌入式 Postgres 和本地文件存储
2. **生产环境**：指向自己的 Postgres，随意部署（Vercel 等）
3. **远程访问**：使用 Tailscale 在移动中访问 Paperclip

---

## 🔗 相关资源

- **GitHub**：https://github.com/paperclipai/paperclip
- **官网**：https://paperclip.ing
- **文档**：https://paperclip.ing/docs
- **Discord**：https://discord.gg/m4HZY7xNG3
- **许可证**：MIT

### 重要文档
- `doc/GOAL.md` - 项目目标
- `doc/PRODUCT.md` - 产品定义
- `doc/SPEC-implementation.md` - V1 实现规范
- `doc/DEVELOPING.md` - 开发指南
- `doc/DATABASE.md` - 数据库设计
- `doc/OPENCLAW_ONBOARDING.md` - OpenClaw 集成指南

---

## 📊 总结评价

### 优势
1. **定位清晰**：不是 Agent 框架，而是公司运营系统
2. **解决真实痛点**：多 Agent 协调、成本控制、状态管理
3. **技术栈现代**：TypeScript + React + PostgreSQL
4. **开源免费**：MIT 许可证，自托管
5. **生态完善**：支持多种 Agent（OpenClaw、Codex、Claude、Cursor）
6. **活跃开发**：最新版本 4 天前发布

### 潜在挑战
1. **学习曲线**：需要理解组织架构、目标对齐等概念
2. **依赖多个 Agent**：需要先配置好 OpenClaw、Claude Code 等
3. **生产部署**：需要自己管理 PostgreSQL 和部署

### 适用性评估
| 场景 | 适用性 |
|------|--------|
| 单一 Agent 用户 | ❌ 不适合 |
| 多 Agent 协调（5+） | ✅ 强烈推荐 |
| 构建 AI 初创公司 | ✅ 非常适合 |
| 需要成本控制 | ✅ 核心功能 |
| 需要移动管理 | ✅ 支持 |

---

## 🚀 下一步行动建议

1. **本地测试**：运行 `npx paperclipai onboard --yes` 体验
2. **阅读文档**：重点关注 `doc/GOAL.md` 和 `doc/PRODUCT.md`
3. **集成 OpenClaw**：参考 `doc/OPENCLAW_ONBOARDING.md`
4. **关注路线图**：ClipMart 功能即将推出

---

**研究完成时间**：2026-03-16 11:15  
**下一步**：等待 Jason哥 指示是否需要进一步研究或实际部署测试
