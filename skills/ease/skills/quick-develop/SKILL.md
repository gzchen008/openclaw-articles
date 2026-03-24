---
name: quick-develop
description: Use when implementing a small, low-risk change (≤5 files, ≤200 LOC, single module) with evidence requirements for tests and minimal documentation.
tools: Glob, Grep, Read, Write, Edit, NotebookEdit, Bash, TodoWrite, mcp__ide__getDiagnostics
---

# Quick Develop — 快速开发全流程自动化

基于 **Superpower 设计理念** 与 **文档同步闭环** 的小需求快速开发解决方案，提供**验证驱动**、**质量守底**、**自动同步**的完整开发体验。

> **定位**：介于 flow-1-analyze-brd 和 flow-1-analyze-trd 之间的小需求快速通道，适用于 2-8 小时内可完成、代码改动少于 200 行的任务。

## When to Use

基于量化指标的判定场景：

| 维度 | 阈值 |
|------|------|
| 代码量 | ≤ 200 LOC |
| 涉及文件 | ≤ 5 个 |
| 预估工时 | < 4 小时 |
| 影响范围 | 单模块/单领域 |

**适用场景**：
- 小功能增强（2-8 小时）
- Bug 修复（1-4 小时）
- 简单重构（2-6 小时）
- 配置调整（1-2 小时）
- 枚举扩展、字段新增、逻辑调整

### Do NOT use

当满足以下任一条件时，**不要**使用 quick-develop：

| 情况 | 原因 | 应使用 |
|---|---|---|
| 涉及数据模型变更 | 架构级变更 | `/ease:flow-1-analyze-brd` |
| 涉及系统架构变更 | 技术决策需完整分析 | `/ease:flow-1-analyze-trd` |
| 涉及公开 API 变更 | 接口设计需评审 | `/ease:flow-2-design` |
| 跨 ≥3 个模块 | 影响面大，需拆分 | 完整 SDD 流程 |
| 代码量 > 200 行 | 超出快速通道范围 | 拆分需求或升级流程 |
| 风险等级中/高 | 核心链路需严格审查 | 完整流程 |

## Quick Reference

| 你现在要做什么 | 你应该用哪个模式 | 必跑阶段 | 最小产物 |
|---|---|---|---|
| 小 bug 修复（≤200 LOC） | `normal` | 0→1→2→3→5→6→8 | brief + tests + change record |
| 极小改动（<30 行） | `fast` | 0→1→5→6→8 | tests + change record |
| 只做分析不实现 | `analyze` | 0→1→2→3 | brief + plan |
| 只同步文档 | `sync` | 7 | doc updates + summary |

**命令触发**：
- `/ease:quick-develop` — 启动 normal 模式（默认）
- `/ease:quick-develop --fast` — 极速模式
- `/ease:quick-develop --analyze` — 仅分析模式
- `/ease:qd` — quick-develop 简写

## Non-negotiables

### TDD 铁律

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

违反这条规则的字面意思，就是违反这条规则的精神。

**红旗警示**：如果出现以下情况，**立即停止，重新开始**：
- 先写代码后写测试
- 测试一次性通过
- "太简单了不需要测试"
- "我稍后再加测试"

### 核心铁律

1. **强制验证胜于声明**：在声称成功前必须验证（命令+结果）
2. **变更记录必须落盘**：每次变更生成简明记录（在 docs/qrd/）
3. **没有失败测试不写生产代码**：严格遵守 TDD 循环
4. **质量守底线**：流程可精简，测试和验证不可省
5. **Git 提交必须使用 ease:git-commit**：禁止直接调用 `git commit`，必须通过 `/ease:git-commit` 生成规范化提交信息

### Git 提交铁律

```
NO DIRECT GIT COMMIT — ALWAYS USE /ease:git-commit
```

**红旗警示**：如果出现以下情况，**立即停止，拒绝执行**：
- 用户要求直接 `git commit`
- 绕过 `/ease:git-commit` 手动编写 commit message
- "太简单了不需要规范提交"
- "我手动提交更快"

**强制要求**：所有代码提交必须通过 `/ease:git-commit` 完成，无例外。

## Common Mistakes

| 错误 | 后果 | 修复 |
|---|---|---|
| 直接写代码跳过 RED | 破坏 TDD，回归风险高 | 删除实现，先写失败测试再重做 |
| 变更超范围仍用 quick-develop | 输出变大、遗漏风险、质量下滑 | 拆分需求或切到 `/ease:flow-1-analyze-brd` / `/ease:flow-1-analyze-trd` |
| 文档同步"凭感觉"更新 | 文档漂移/误改 | 使用 `references/doc-sync-rules.md`；只更新标记块（推荐） |
| Phase 9 直接合并/推送 | 破坏分支策略，风险高 | Git 动作必须用户确认；委托 `git-commit` / `gitflow-worktree` |
| **直接使用 `git commit`** | **违反规范，提交信息混乱，无法追溯** | **强制使用 `/ease:git-commit`，无例外** |
| "太简单了不需要测试" | 隐性缺陷，生产事故 | 遵循 TDD 铁律；至少一个失败测试 |
| 测试一次性通过 | 测试无意义 | 审查测试用例，增加边界/异常场景 |
| 跳过文档同步 | 代码文档分离，后续维护困难 | Phase 7 必须执行；生成同步报告 |

## Workflow

完整的九阶段工作流程（Phase 0-9）详见：**`references/workflow.md`**

### 阶段概览

```
Phase 0: 前置检查 → Phase 1: 需求分析 → Phase 2: 影响分析 → Phase 3: 快速设计与审查
    ↓               ↓               ↓               ↓
Phase 4: 上下文保存 → Phase 5: 代码实现 → Phase 6: 测试验证 → Phase 7: 文档同步
    ↓               ↓               ↓               ↓
Phase 8: 变更总结 → Phase 9: Git 提交与收尾
```

### 快捷模式

| 模式 | 调用方式 | 执行阶段 |
|------|----------|----------|
| normal | `/ease:quick-develop` 或 `/ease:qd` | 0→1→2→3→5→6→8 |
| fast | `--fast` | 0→1→5→6→8 （跳过分析/设计/文档） |
| analyze | `--analyze` | 0→1→2→3 （仅分析不实现） |
| sync | `--sync` | 7 （仅文档同步） |

## 前置确认

在执行完整流程前，向用户确认适用范围（可通过 `--auto_confirm` 跳过）：

```
🔔 快速开发模式适用于 <200行、单模块、低风险的小需求

根据您的需求描述，初步分析如下：
- 变更点: [一句话概括]
- 预估代码量: [预估行数]
- 影响范围: [模块/文件列表]
- 风险评估: [低/中/高]

判定结果: [✅ 小需求 / ⚠️ 建议使用完整流程 / ⚠️ 建议拆分]

请选择:
- 继续快速开发流程
- 切换到完整 SDD 流程 (/ease:flow-2-design)
- 拆分需求后重新评估
- 使用其他命令: /ease:flow-1-analyze-brd / /ease:flow-1-analyze-trd
```

**自动确认条件**: 当用户使用 `/ease:qd` 命令或设置 `--auto_confirm=true` 时，可跳过确认直接进入流程。

## 协作技能集成

| 阶段 | 协作技能 | 触发场景 |
|------|----------|----------|
| Phase 0 | `ease-spec` | 创建 constitution.md |
| Phase 1 | `ease:flow-1-analyze-brd` / `ease:flow-1-analyze-trd` | 需求超出快速通道范围 |
| Phase 4 | `ease:gitflow` | 创建 feature 分支 |
| Phase 9 | `ease:git-commit` | **【强制】** 创建规范提交，禁止直接 `git commit` |

## 目录结构

```
.ease/qrd/          # 临时分析文件（上下文）
.ease/quick/       # 快速开发输出（brief/plan/report）
docs/qrd/           # 变更记录
```

## 参考资源

- **完整工作流**: `references/workflow.md`
- **需求分级指南**: `references/requirement-classification.md`
- **文档同步规则**: `references/doc-sync-rules.md`

## 版本历史

### v2.0.0 - 重构版
- **架构重构**: SKILL.md 改为入口页，详细流程下沉到 references/workflow.md
- **可扫描性优化**: 顶部新增 Quick Reference 和 Common Mistakes
- **Description 优化**: 重写为 "Use when …" 触发条件格式
- **安全边界**: 明确 Phase 9 只产建议，Git 动作交由专用 skill
