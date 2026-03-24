---
name: ease
description: 企业级软件开发插件系统，包含需求分析、架构设计、代码实现、测试、文档生成等完整开发流程。支持三阶段开发流程（分析→设计→实现）+ 代码审查 + 单元测试 + 架构文档生成。
metadata:
  openclaw:
    emoji: 🚀
    subskills:
      - ease-analysis
      - ease-architecture
      - ease-coding
      - ease-testing
      - ease-helper
      - ease-improve
      - ease-spec
      - ease-poc
      - ease-framework-code
      - ease-arch-documentation
---

# Ease - 企业级软件开发插件

Ease 是一个完整的软件开发辅助系统，覆盖从需求分析到代码实现的完整流程。

## 🎯 三阶段开发流程

### 阶段1: 需求分析 (ease-analysis)
- 分析业务需求文档（BRD）
- 生成领域模型、用例与业务规则
- 输出技术需求文档（TRD）

### 阶段2: 架构设计 (ease-architecture)
- 根据用例进行架构设计
- 生成框架代码（Controller/Service/Repository）
- 完整的代码注释与 TODO 标记

### 阶段3: 代码实现 (ease-coding)
- 基于框架代码完成详细实现
- 代码审查与最佳实践指导
- 重构与优化建议

## 📦 核心功能

| Skill | 功能 |
|-------|------|
| `ease-analysis` | 需求分析、领域建模 |
| `ease-architecture` | 架构设计、框架代码生成 |
| `ease-coding` | 代码实现、代码审查 |
| `ease-testing` | 单元测试生成（FIRST 原则） |
| `ease-helper` | 插件知识问答 |
| `ease-improve` | 代码改进建议 |
| `ease-spec` | 规格文档生成 |
| `ease-poc` | POC 原型开发 |
| `ease-framework-code` | 框架代码模板 |
| `ease-arch-documentation` | 架构文档生成 |

## 🔧 使用方式

### 需求分析
```
读取 skills/ease/skills/ease-analysis/SKILL.md
根据文档指引进行需求分析
```

### 架构设计
```
读取 skills/ease/skills/ease-architecture/SKILL.md
根据领域模型生成架构设计
```

### 代码实现
```
读取 skills/ease/skills/ease-coding/SKILL.md
根据设计完成代码实现
```

## 📁 目录结构

```
skills/ease/
├── agents/          # AI 代理配置
├── commands/        # 命令定义
├── skills/          # 子 skills
│   ├── ease-analysis/
│   ├── ease-architecture/
│   ├── ease-coding/
│   ├── ease-testing/
│   └── ...
├── ease-commands-reference.md    # 命令参考手册
├── ease-agent-usage.md           # Agent 使用指南
└── terminology-glossary.md       # 术语表
```

## 📚 文档

- **命令参考**: `ease-commands-reference.md`
- **Agent 使用**: `ease-agent-usage.md`
- **术语表**: `terminology-glossary.md`

## ⚠️ 注意事项

1. 这是 Claude Code 插件移植版本，部分命令（如 `/ease:xxx`）需要在 Claude Code 中使用
2. 在 OpenClaw 中，直接读取对应 skill 的 SKILL.md 文件获取指导
3. 遵循项目的 CLAUDE.md 规范

---

来源: git@code.weoa.com:inf/claude-skills-marketplace.git
