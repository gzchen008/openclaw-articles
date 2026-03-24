---
name: ease-spec
description: Use when performing spec-driven development to maintain traceability between requirements, plans, and implementation outputs.
tools: Glob, Grep, Read, Write, Edit, TodoWrite
---

# Ease Spec — 规范驱动开发（SDD）

## Overview

基于 SDD（Spec-Driven Development）方法论，提供四阶段开发流程：**需求规范 → 技术计划 → 任务分解 → 执行实现**，维护 `docs/domains/` ↔ `.eases/` 的映射与可追溯性。

## When to Use

**Use when:**
- Executing /ease:flow-1-analyze-brd, /ease:flow-1-analyze-trd, /ease:flow-2-design, /ease:flow-3-implement
- Need complete spec lifecycle (spec → plan → tasks → implement)
- Need to maintain traceability between requirements, plans, and outputs

**Do NOT use:**
- For /ease:architecture-review, /ease:code-review, /ease:generate-tests, /ease:gitflow (these don't invoke ease-spec)

## Quick Reference

| Task | Input | Output | Reference |
|---|---|---|---|
| Create constitution | None | memory/constitution.md | reference/project-constitution.md |
| Create spec | BRD/docs | .eases/[编号]/[cmd]/spec.md | reference/create-requirements-spec.md |
| Create plan | spec.md | plan.md | reference/create-technical-plan.md |
| Generate tasks | plan.md | tasks.md | reference/generate-tasks.md |

## Non-negotiables

1. **Constitution FIRST**: Must create `memory/constitution.md` before first use
2. **唯一目录名**: Use `.eases/` (NOT `eases/` or `specs/`)
3. **相对路径**: Use `.eases/...`, `docs/domains/...` (NOT `/.eases/...`)
4. **编号规则**: Three-digit incrementing numbers (001, 002, 003...)
5. **Command scope**: Only 4 commands invoke ease-spec:
   - /ease:flow-1-analyze-brd (Phase 1 - Business)
   - /ease:flow-1-analyze-trd (Phase 1 - Technical)
   - /ease:flow-2-design (Phase 2)
   - /ease:flow-3-implement (Phase 3)

   > **Note**: `/ease:analyze-code` does NOT invoke ease-spec. It is a reverse engineering command that only outputs domain documentation (analyze-code-output.md, usecases/, rules.md) without generating spec.md/plan.md/tasks.md.

6. **阶段产物边界（Phase Output Boundaries）** — **不可协商，不可质疑**

   > ⚠️ **核心原则**：不同阶段的 ease-spec 意图和产物**必须严格区分**。除 `flow-3-implement` 外，其他阶段**禁止生成/实现实际代码**。

   | 阶段 | 命令 | 允许产物 | **禁止产物** |
   |------|------|----------|-------------|
   | **Phase 1** | flow-1-analyze-brd<br>flow-1-analyze-trd | • 领域文档 (analyze-brd-output.md/TRD.md)<br>• 用例文档 (usecases/)<br>• 业务规则 (rules.md)<br>• spec.md（需求规范）<br>• plan.md（技术计划）<br>• tasks.md（任务分解） | ❌ **任何代码**<br>❌ API 接口定义<br>❌ 数据库 Schema<br>❌ 技术架构图 |
   | **Phase 2** | flow-2-design | • 架构设计文档 (arch-design.md)<br>• 详细设计文档 (detail-design.md)<br>• spec.md（含 Clarifications）<br>• plan.md<br>• tasks.md<br>• **框架代码骨架**（仅有结构 + TODO 注释） | ❌ **具体业务逻辑实现**<br>❌ 完整的方法实现<br>❌ 可运行的业务代码 |
   | **Phase 3** | flow-3-implement | • 实际代码实现<br>• 测试代码<br>• spec.md（实现总结）<br>• plan.md<br>• tasks.md | — （此阶段可自由实现） |

   **红旗警示**：如果出现以下情况，**立即停止，拒绝执行**：
   - Phase 1 尝试生成任何代码、接口定义或技术实现细节
   - Phase 2 尝试实现完整的业务逻辑（框架代码应只有 `throw UnsupportedOperationException("TODO")` 或 TODO 注释）
   - 以"效率"为由在 Phase 1/2 提前实现代码
   - 用户要求跳过阶段边界直接写代码

   **阶段产物边界不可协商的原因**：
   1. **职责分离**：需求分析只关注"做什么"，设计只关注"怎么做"，实现才关注"具体写"
   2. **可追溯性**：每个阶段的产物是下一阶段的输入，混淆边界会破坏追溯链
   3. **变更控制**：需求变更在 Phase 1 处理，技术变更在 Phase 2 处理，代码变更在 Phase 3 处理
   4. **质量保证**：每个阶段有独立的质量检查标准，跨阶段产出会导致质量失控

## Path Conventions

| Purpose | Format |
|---|---|
| Constitution | memory/constitution.md |
| Domain docs | docs/domains/[编号]-[module_name]/ |
| Spec directory | .eases/[编号]-[功能名]/[command]/ |
| Usecase directory | docs/domains/[编号]-[module_name]/usecases/[编号]-[subdomain]/ |

## Numbering Rules (Three-digit)

| Level | Format | Example |
|---|---|---|
| Domain | [编号]-[module_name] | 001-user-management |
| Subdomain | [编号]-[subdomain] | 001-authentication |
| Usecase | [编号]-[usecase-name].md | 001-login-with-password.md |
| Feature | [编号]-[功能名] | .eases/001-user-auth/ |

### Number generation
- 新增 domain：扫描 `docs/domains/`，取最大编号 + 1
- 新增 subdomain：扫描对应 domain 的 `usecases/` 目录
- 新增 usecase：扫描对应 subdomain 目录
- 新增 feature/.eases/：扫描 `.eases/` 目录

### Numbering Conflict Resolution

当编号冲突时：
1. 检查是否存在已删除/归档的功能目录（可复用编号）
2. 如果冲突目录活跃，使用最大编号 + 1
3. 记录冲突解决日志到 `.eases/numbering-log.md`
4. 多团队协作时，先拉取最新代码再生成编号

## Output Quality Gates

每个阶段产出必须通过质量检查：

### spec.md Quality Gates
- [ ] **需求完整性**: 覆盖所有输入需求点（BRD/代码分析）
- [ ] **可追溯性**: 每个需求点有来源引用（BRD 章节/代码路径）
- [ ] **无歧义**: 术语使用一致，无模糊表述（如"可能"、"应该"已澄清）
- [ ] **范围明确**: 明确列出 in-scope 和 out-of-scope

### plan.md Quality Gates
- [ ] **技术方案可行性**: 所有技术选型有依据（POC/文档/最佳实践）
- [ ] **风险评估**: 列出 ≥3 个主要风险及缓解措施
- [ ] **依赖清晰**: 明确列出内部/外部依赖及版本要求

### tasks.md Quality Gates
- [ ] **任务可执行**: 每个任务有明确的完成标准
- [ ] **粒度适中**: 单个任务预估工时 ≤4 小时
- [ ] **依赖排序**: 任务按依赖关系正确排序

## Directory Mapping

| Ease Command | Docs 输出 | Eases 输出 |
|---|---|---|
| /ease:flow-1-analyze-brd | docs/domains/[编号]-[模块]/analyze-brd-output.md + usecases/ | .eases/[编号]-[功能名]/flow-1-analyze-brd/spec.md |
| /ease:flow-1-analyze-trd | docs/trd/[编号]-[模块].md + .eases/trd/[编号]-[模块]/flow-1-analyze-trd/TRD.md + analysis/ + artifacts/ | .eases/trd/[编号]-[模块]/flow-1-analyze-trd/spec.md |
| /ease:flow-2-design | design-output.md + architecture/ + detail/ | .eases/[编号]-[功能名]/flow-2-design/spec.md + framework-code/ |
| /ease:flow-3-implement | 代码实现总结 | .eases/[编号]-[功能名]/flow-3-implement/spec.md |

> **Note**: `/ease:analyze-code` is NOT in this table because it does NOT invoke ease-spec. It only outputs to `docs/domains/[编号]-[模块]/analyze-code-output.md + usecases/` without creating `.eases/` spec files.

## Spec Lifecycle

执行 4 命令时必须完整运行：
1. 检查 `constitution.md` → 不存在则先创建
2. 生成编号（扫描现有目录）
3. 需求规范阶段 → spec.md
4. 需求澄清阶段（仅 /ease:flow-2-design，可选）→ spec.md 的 Clarifications 章节
5. 技术计划阶段 → plan.md
6. 框架代码阶段（仅 /ease:flow-2-design）→ framework-code/
7. 任务分解阶段 → tasks.md
8. 执行实现阶段（/ease:flow-2-design 除外）→ 实际代码
9. 质量检查 → checklists/

## Edge Cases

| 场景 | 处理策略 |
|------|----------|
| **constitution.md 版本过旧** | 询问用户是否更新，或标记为 "待更新" 继续执行 |
| **多团队协作编号冲突** | 先执行 `git pull`，再扫描目录生成编号；如仍冲突，使用最大编号 + 1 |
| **spec.md 超过 500 行** | 拆分为 `spec-core.md` + `spec-detail.md`，在 spec.md 中引用 |
| **目录权限不足** | 提示用户检查目录权限，提供 `chmod` / `chown` 命令示例 |
| **Git 工作区不干净** | 提示用户先提交或暂存现有变更，避免混淆 |

## Common Mistakes

| 错误 | 症状 | 修复 |
|---|---|---|
| Using absolute paths | Writing `/.eases/` instead of `.eases/` | Use relative paths, remove leading `/` |
| Mixed directory names | Using both `eases/` and `.eases/` | Standardize on `.eases/` |
| Skipping constitution | No constitution.md exists | Create memory/constitution.md first |
| Non-sequential numbering | Skipped or non-consecutive numbers | Scan existing directories and use max + 1 |
| Command scope error | Non-specified commands invoke ease-spec | Only 4 commands invoke ease-spec |

## Handoff Guidelines

### From ease-analysis
接收分析阶段的产出：
- [ ] 领域模型已定义
- [ ] 核心用例已识别
- [ ] 业务规则已提取

### To ease-architecture (for /ease:flow-2-design)
移交架构设计：
- [ ] spec.md 已通过质量检查
- [ ] 技术方案需要架构评审

### To ease-coding (for /ease:flow-3-implement)
移交代码实现：
- [ ] tasks.md 已生成并评审
- [ ] 所有依赖资源已准备就绪

## See Also

### Upstream (Input Sources)
- `ease-analysis/SKILL.md` - Provides domain models and usecases
- `commands/flow-1-analyze-brd.md` - Command for BRD analysis (Phase 1)
- `commands/flow-1-analyze-trd.md` - Command for TRD analysis (Phase 1)
- `commands/analyze-code.md` - Command for code reverse engineering
- `commands/flow-2-design.md` - Command for architecture design (Phase 2)
- `commands/flow-3-implement.md` - Command for code implementation (Phase 3)

### Downstream (Output Consumers)
- `ease-architecture/SKILL.md` - Receives spec.md for architecture design
- `ease-framework-code/SKILL.md` - Receives plan.md for framework generation
- `ease-coding/SKILL.md` - Receives tasks.md for implementation

### Alternatives
- `quick-develop/SKILL.md` - For small changes (<200 LOC) without full SDD
- `ease-poc/SKILL.md` - For technical feasibility validation before spec

### Reference documents
- `reference/project-constitution.md` - First-time setup guide
- `reference/create-requirements-spec.md` - Specify phase
- `reference/create-technical-plan.md` - Plan phase
- `reference/generate-tasks.md` - Tasks phase
- `reference/execute-implementation.md` - Implement phase
- `reference/requirements-clarification.md` - Clarify phase

### Templates & Scripts
- `templates/` - Document templates for each phase
- `scripts/bash/` and `scripts/powershell/` - Cross-platform init/validation scripts
