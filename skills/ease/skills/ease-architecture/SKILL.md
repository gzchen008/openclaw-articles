---
name: ease-architecture
description: Use when designing or reviewing system architecture and justifying NFR tradeoffs with evidence and specific metrics.
tools: Glob, Grep, Read, TodoWrite, BashOutput, Bash, Edit, Write, NotebookEdit
model: inherit
---

# Ease Architecture

## 异步任务检测

> **优先检测**：在执行本技能前，首先检测用户输入是否包含 `[@ease]` 和 `async` 关键词。

**检测条件**：当用户输入**同时满足**以下条件时，触发 `async-task` 技能：
- 包含 `[@ease]` 标记（或 `[@Ease]`、`[@EASE]`）
- 包含 `async` 关键词（或 `--async` 标记）

**触发示例**：
- `[@ease] async 进行架构评审`
- `/ease:architecture-review [@ease]--async 评估系统设计`
- `[@ease] 异步执行：评审 NFR 指标`

**检测逻辑**：
```bash
# 检测用户输入中是否同时包含 @ease 和 async 关键词
USER_INPUT="$1"  # 用户完整输入
if [[ "$USER_INPUT" =~ @ease|@Ease|@EASE ]] && [[ "$USER_INPUT" =~ async|\[async\]|异步 ]]; then
    # 触发 async-task 技能，将任务提交到云端
    # 任务类型：技术任务 (issue_type=5, 标题前缀=[task])
    # 任务内容：完整的用户输入（包括命令）
fi
```

**触发后的行为**：
1. 将完整的用户输入（如 `/ease:architecture-review [@ease]--async 评审架构`）作为任务描述
2. 使用 `async-task` 技能提交到云端后台
3. 向用户反馈"任务已提交到云端后台"

## Overview

面向"架构设计 / 架构评审"，产出**可落地、可验证**的架构决策与交付物（含风险、权衡与改进建议）。

## When to Use

**Use when:**
- 需要验证新系统/重大变更的架构设计质量
- NFR 诉求不明确（性能/安全/可用性指标缺失）
- 需要评估技术选型的风险与权衡
- 需要输出架构审查报告（评分/风险清单/建议）

**Do NOT use:**
- 只生成框架代码骨架 → `ease-framework-code`（MumbleSDK 项目叠加 `mumblesdk`）
- 只写业务代码/修 bug/补测试 → `ease-coding` / `ease-testing`

## Quick Reference

| 目标 | 触发症状 | 参考 |
|---|---|---|
| 架构评审 | 需要验证设计质量、评估风险 | `flows/architecture-review.md` + `references/architecture-review-guide.md` |
| 用例架构设计 | 有 usecases，需要技术方案 | `flows/design-framework-code.md` |
| 场景化架构设计 | 有 usecases，需要基于场景模板的标准化技术方案 | `commands/flow-2-design.md`（步骤 3.5 场景识别 + 步骤 4 基于模板生成） |
| 框架代码生成 | 有设计，需要骨架代码 | **REQUIRED:** `ease-framework-code`（通用）/ `mumblesdk`（企业框架） |

## Architecture Review (6 dimensions)

1. **业务匹配度与合理性**
2. **非功能性需求（NFR）**：可用性、性能、安全性、一致性等
3. **系统设计与技术选型**
4. **数据架构**
5. **可运维性与可观测性**
6. **风险与灾备**

详见：`references/architecture-review-guide.md`

## Framework Code Generation (Thin)

> 本节只保留"生成骨架代码"的最低原则。具体细节交由 `ease-framework-code`。

### 核心铁律

1. **只生成骨架结构**：类/接口、方法签名、依赖注入声明
2. **方法体只写步骤注释**：`// TODO: Step N. ...`（必须足够详细，可指导实现）
3. **禁止写任何实际逻辑**：不写业务逻辑、条件判断、数据处理
4. **占位必须可移植**：Java 使用 `UnsupportedOperationException`（JDK 标准），避免 `NotImplementedException`

### 最小示例

```java
public OrderDTO findById(String orderId) {
  // TODO: Step 1. Validate input (null/blank) (UC-001, BR-001)
  // TODO: Step 2. Query from repository/DAO (UC-001)
  // TODO: Step 3. Handle not-found (domain error) (BR-002)
  // TODO: Step 4. Return DTO (UC-001)
  throw new UnsupportedOperationException("TODO: implement");
}
```

## Decision Traceability Requirements

所有架构决策必须可追溯：

### Decision Record Format
每个关键决策必须包含：
- [ ] **决策 ID**: `ADR-XXX` (Architecture Decision Record)
- [ ] **上下文**: 决策时的技术/业务背景
- [ ] **方案对比**: ≥2 个备选方案的优缺点
- [ ] **决策依据**: 量化指标、POC 结果、团队共识
- [ ] **风险与缓解**: 决策带来的风险及缓解措施
- [ ] **回滚策略**: 决策失败时的回滚方案

### NFR 指标要求
| NFR 类型 | 必须包含 | 验证方式 |
|---------|---------|---------|
| 性能 | 目标 QPS、延迟 P99 | 压测计划 |
| 可用性 | 目标 SLA (如 99.9%) | 故障演练 |
| 安全 | 合规标准 (如等保) | 安全审计 |
| 一致性 | 强一致/最终一致选择 | 测试用例 |
| 可观测性 | 关键指标、日志、追踪 | 监控配置 |

## Handoff Guidelines

### From ease-analysis
接收分析阶段的产出：
- [ ] 用例文档已通过质量检查
- [ ] 核心业务规则已定义（覆盖 ≥80% 核心场景）
- [ ] 术语表已确定且与业务方达成共识
- [ ] 领域边界已明确划分

### To ease-framework-code
移交框架代码生成：
- [ ] 架构设计已评审通过
- [ ] 技术选型已确定且有决策记录
- [ ] 模块划分已明确
- [ ] NFR 指标已定义且可验证

## Edge Cases

| 场景 | 处理策略 |
|------|----------|
| **云原生架构 (K8s/Istio)** | 增加云原生检查项：服务网格配置、弹性伸缩、健康检查 |
| **微服务依赖复杂** | 绘制服务依赖图，识别循环依赖和单点故障 |
| **遗留系统集成** | 明确集成模式（API/消息/数据库），定义防腐层 |
| **多租户架构** | 明确租户隔离级别（数据/计算/存储），定义租户路由策略 |
| **全球化部署** | 考虑数据主权、时区、多活架构、跨区域复制 |

## Common Mistakes

| 错误 | 症状 | 修复 |
|---|---|---|
| 评审变成个人偏好 | "我觉得这里不对" | 使用 `references/architecture-review-guide.md` 六维度检查 |
| NFR 只有清单 | "需要考虑性能" | 给出目标指标、容量规划、验证方式 |
| 骨架中写业务逻辑 | 方法体有 if/for/业务代码 | 严格只写 TODO 注释占位 |
| 使用非标准占位异常 | `NotImplementedException` 导致编译失败 | 使用 `UnsupportedOperationException` (JDK 标准) |

## See Also

### Upstream (Input Sources)
- `ease-analysis/SKILL.md` - Provides usecases and domain models
- `ease-spec/SKILL.md` - Provides spec.md for /ease:flow-2-design command
- `commands/flow-2-design.md` - Command interface for architecture design

### Downstream (Output Consumers)
- `ease-framework-code/SKILL.md` - Receives architecture for framework generation
- `ease-coding/SKILL.md` - Receives implementation guidelines
- `ease-poc/SKILL.md` - Validates technical decisions

### Alternatives
- `ease-arch-documentation/SKILL.md` - For system documentation (not architecture design)
- `quick-develop/SKILL.md` - For small changes without architecture review

### References
- `references/architecture-review-guide.md` - Architecture review guide
- `ease-framework-code/references/generate-framework-code.md` - Framework code generation
- `ease-framework-code/checklists/framework_verification_checklist.md` - Framework verification
- `mumblesdk/SKILL.md` - MumbleSDK enterprise framework

### Scenario-Driven Design (场景化设计)
- `ease-arch-documentation/references/scenario-classification.md` - 场景分类体系与识别规则
- `ease-arch-documentation/references/scenario-templates/` - 场景架构模板库
- `ease-arch-documentation/references/generate-scenario-templates.md` - 模板生成指南
- `ease-arch-documentation/references/scenario-template-writing-guide.md` - 模板编写指南
