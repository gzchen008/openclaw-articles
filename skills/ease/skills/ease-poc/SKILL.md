---
name: ease-poc
description: Use when validating a technical hypothesis quickly (≤30 min) with runnable evidence to decide adopt/avoid a library, framework, integration, or performance approach.
tools: Glob, Grep, Read, TodoWrite, BashOutput, Bash, Edit, Write, NotebookEdit, WebSearch
model: inherit
---

# Ease POC — 技术选型验证技能

## Overview

一句话：用最小可运行实验验证技术假设，并给出可审查证据与决策建议。

## When to Use

**Use this skill when you need to:**

- 快速验证新技术/新框架/新库的可行性（≤30 分钟）
- 对比多个技术方案（性能、集成成本等）
- 验证集成方案是否可行（API、数据库、消息队列等）
- 评估引入某个技术替代现有方案的可行性

**Do NOT use when:**

- 需要完整功能开发（应使用 `ease-coding`）
- 需要架构设计评审（应使用 `ease-architecture`）
- 需要编写生产级代码（应使用 `ease-spec`）

## Quick Reference

| 你要验证什么 | 最小实验 | 关键指标 | 输出 |
|---|---|---|---|
| 新库/框架是否可用 | 最小 Hello World + 与现有组件集成点 | 兼容性/依赖冲突/开发成本 | POC 报告 + 风险 |
| 性能是否满足 | 基准测试（baseline vs new） | p95/吞吐/CPU/内存 | 对比结论 + 采样数据 |
| 迁移是否可行 | 最小迁移路径验证 | 变更面/回滚成本 | go/no-go + 迁移步骤 |
| 集成是否可行 | 最小集成代码 + Mock | 接口适配/数据映射 | 集成评估 + 适配方案 |

## POC Decision Flowchart

```dot
digraph poc_decision {
    "Technical question?" [shape=diamond];
    "Need runnable evidence?" [shape=diamond];
    "≤ 30 min trial?" [shape=diamond];
    "Use ease-poc" [shape=ellipse, style=filled, fillcolor=lightblue];
    "Use ease-architecture" [shape=box];
    "Use ease-coding" [shape=box];

    "Technical question?" → "Need runnable evidence?";
    "Need runnable evidence?" → "≤ 30 min trial?";
    "Need runnable evidence?" → "Use ease-architecture" [label="No - strategic decision"];
    "≤ 30 min trial?" → "Use ease-poc" [label="Yes"];
    "≤ 30 min trial?" → "Use ease-coding" [label="No - full feature"];
}
```

## Non-negotiables

- **必须先读取系统文档**：不了解系统现状就开展 POC，可能导致验证结论与实际需求脱节
  - P0：`CLAUDE.md` / `.claude` / `docs/system/`
  - P1：`memory/constitution.md` / `README.md`
- **必须可运行**：验证代码必须可以直接执行，输出可量化结果
- **必须记录证据**：环境、命令、原始输出、判定标准必须完整记录
- **必须给出 go/no-go 结论**：不能只有现象描述，必须有明确的决策建议

## Workflow

详见执行流程：`flows/poc-execution.md`

### 流程概览

```
[0] 系统分析 → [1] 验证点分析 → [2] 方案设计 → [3] 知识输出 → [4] 代码实现 → [5] 验证执行 → [6] 结论报告
```

## Common Mistakes

| 错误 | 症状 | 补救 |
|---|---|---|
| 跳过系统分析直接开始 | POC 方案与项目技术栈不兼容 | 回到阶段 0，读取文档并调整方案 |
| 过度扩展验证范围 | 验证代码变得复杂，时间超支 | 聚焦核心验证点，砍掉次要功能 |
| 只记录结论不记录证据 | 报告无法审查，结论存疑 | 补充 "Evidence (Runnables)" 区块 |
| POC 代码直接进入主分支 | 生产代码污染，难以回滚 | 使用独立的 poc/ 或 experiments/ 目录 |
| 只有正向验证结果 | 风险识别不足，决策依据不全 | 主动补充失败场景和边界测试 |

## POC 产物隔离与退出机制

### 产物隔离

POC 默认不应直接进入生产主干，需采用隔离机制：

```
poc/                          # 或 experiments/
├── poc-[技术名称]/
│   ├── README.md
│   ├── [依赖配置文件]
│   ├── src/
│   └── docs/
│       └── poc-report.md
```

### 退出机制

**采用（Recommend to Adopt）：**
1. 将验证结论输入 `ease-architecture`（纳入架构决策/NFR）
2. 转入 `ease-framework-code` 或 `ease-coding` 进行正式开发
3. POC 代码作为参考，不应直接复制到生产

**不采用（Recommend to Avoid）：**
1. 记录不采用原因到 `docs/poc-decisions/`
2. 清理 POC 依赖（恢复依赖配置文件）
3. 删除 POC 试验代码和相关产物
4. 更新技术栈文档（明确记录已拒绝的技术方案）

## Evidence（Runnables）结构

所有验证报告必须包含完整的证据区块（参见 `templates/poc-report-template.md`）：

```markdown
## Evidence (Runnables)

### Environment
- 操作系统：[具体版本]
- 语言版本：[具体版本]
- 依赖版本：[列出所有新增/修改的依赖]

### Commands
可复制粘贴的命令行（含参数）：
```bash
# 命令1
# 命令2
```

### Raw Outputs
关键日志/指标/报错（截取要点）：
[实际输出内容]

### Pass/Fail Criteria
- 通过标准：[明确的阈值或条件]
- 实际判定：[通过/失败/有条件通过]
```

## See Also

- `flows/poc-execution.md` - 完整的 POC 执行流程
- `templates/poc-report-template.md` - POC 验证报告模板（含 Evidence 结构）
- `references/poc-toolbox.md` - 快速验证工具箱（性能测试、监控诊断工具）

## Version History

- **v2.0**：结构重构（短正文 + 强引用），增加 Quick Reference、Common Mistakes、Evidence 结构、退出机制
- **v1.0**：初始版本，支持 Java/Python/Go 三种语言的 POC 验证
