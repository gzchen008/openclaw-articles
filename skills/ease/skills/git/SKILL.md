---
name: git
description: Use when managing Git branches via GitFlow workflow with bare-repo and worktree setup.
tools: Glob, Grep, Read, TodoWrite, BashOutput, Bash, Edit, Write
model: inherit
---

# Git 分支管理

> ⚠️ **重要声明**：本技能是 `gitflow-worktree` 技能的代理入口。
> 
> 所有 Git 分支管理操作**必须严格遵守** `gitflow-worktree/SKILL.md` 中定义的目录结构和执行流程，**不可协商**。

## 强制透传规则

当用户或模型调用本技能时，**必须**：

1. 完整读取并遵守 `gitflow-worktree/SKILL.md` 的所有规范
2. 使用 `<project>-workspace/` 目录结构（**禁止**使用其他目录结构）
3. 基于裸仓库（bare repository）模式执行所有操作

## 目录结构（不可协商）

```
<project>-workspace/                # 工作空间根目录
├── .bare/                          # 裸仓库（包含所有 Git 数据）
├── .git                            # 指向 .bare 的文件
├── master/                         # master 分支 worktree
├── develop/                        # develop 分支 worktree
├── feature/<name>/                 # feature 分支 worktree
├── release/v<X.Y.Z>/               # release 分支 worktree
└── hotfix/<name>/                  # hotfix 分支 worktree
```

## 分支命名（不可协商）

| 类型 | 格式 | 示例 |
|------|------|------|
| Feature | `feature/<name>` | `feature/user-auth` |
| Release | `release/v<X.Y.Z>` | `release/v1.2.0` |
| Hotfix | `hotfix/<name>` | `hotfix/login-fix` |
| Master | `master` | - |
| Develop | `develop` | - |

**禁止使用**：`feat/`、`fix/`、`rel/`、`main`、`dev` 等变体

## 执行要求

执行任何 Git 操作前**必须**：

1. 读取 `gitflow-worktree/SKILL.md` 获取完整规范
2. 检查前置条件（git-flow 已安装、Git >= 2.15、工作空间已初始化）
3. 展示执行计划给用户确认
4. 严格按照 `gitflow-worktree` 定义的流程执行

## Quick Reference

| 命令 | 说明 | 详细文档 |
|---|---|---|
| `init` | 初始化工作空间 | `gitflow-worktree/SKILL.md` |
| `feature start <name>` | 创建 feature 分支 | `gitflow-worktree/flows/feature-workflow.md` |
| `feature finish <name>` | 完成 feature 分支 | `gitflow-worktree/flows/feature-workflow.md` |
| `release start v<X.Y.Z>` | 创建 release 分支 | `gitflow-worktree/flows/release-workflow.md` |
| `hotfix start <name>` | 创建 hotfix 分支 | `gitflow-worktree/flows/hotfix-workflow.md` |

## See Also

- **`gitflow-worktree/SKILL.md`** - 主规范文档，定义所有规则和流程
- `gitflow-worktree/flows/feature-workflow.md` - Feature 分支工作流
- `gitflow-worktree/flows/release-workflow.md` - Release 分支工作流
- `gitflow-worktree/flows/hotfix-workflow.md` - Hotfix 分支工作流
- `gitflow-worktree/references/gitflow-guide.md` - GitFlow 分支模型指南
- `gitflow-worktree/references/worktree-guide.md` - Git Worktree 使用指南
