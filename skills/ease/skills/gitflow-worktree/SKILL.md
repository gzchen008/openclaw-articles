---
name: gitflow-worktree
description: GitFlow 分支管理方案，配合 Claude Code 原生 Worktree 实现开发隔离。严格遵循 GitFlow 分支命名规范，使用 Claude Code 原生 worktree 进行开发环境隔离。
tools: Glob, Grep, Read, TodoWrite, BashOutput, Bash, Edit, Write
model: inherit
---

## Quick Reference

| 目标 | 入口 | 必要检查 | 关键风险 |
|---|---|---|---|
| 开新 feature | `/ease:gitflow feature start <name>` | `develop` 是否最新；分支是否重名 | 会创建分支；避免在错误目录执行 |
| 完成 feature | `/ease:gitflow feature finish <name>` | 工作区必须 clean；是否已 PR/评审 | 会合并分支（不可逆） |
| 开 release | `/ease:gitflow release start vX.Y.Z` | 版本号格式；`develop` 是否最新 | 版本号/Tag/合并策略需确认 |
| 开 hotfix | `/ease:gitflow hotfix start <name>` | 基线分支（master/main）正确性 | 影响生产修复；必须最小改动 |
| 查看状态 | `/ease:gitflow status` | - | - |
| 清理分支 | `/ease:gitflow cleanup` | 确认不会误删活跃分支 | 会删除已合并分支 |

# GitFlow Worktree

GitFlow 分支管理方案，配合 Claude Code 原生 Worktree 实现开发隔离。

## 核心理念

```
┌────────────────────────────────────────────────────────────┐
│                    职责分离                                 │
├────────────────────────────────────────────────────────────┤
│  ease:gitflow          │  分支生命周期管理                  │
│                        │  - 命名规范 (feature/*, release/*) │
│                        │  - 创建/合并/打标签                │
│                        │  - GitFlow 流程控制                │
├────────────────────────────────────────────────────────────┤
│  Claude Code 原生      │  开发环境隔离                      │
│  -w / --worktree       │  - Worktree 创建/清理              │
│                        │  - Agent 会话隔离                  │
│                        │  - 并行开发支持                    │
└────────────────────────────────────────────────────────────┘
```

## 两种模式

本技能支持两种工作模式：

### 模式 A：标准仓库 + Claude 原生 Worktree（推荐）

```bash
# 1. 创建 GitFlow 分支
/ease:gitflow feature start user-auth

# 2. 使用 Claude Code 原生 worktree 进行隔离开发
claude -w feature/user-auth

# 3. Claude 会在 .claude/worktrees/ 下创建隔离环境
```

### 模式 B：裸仓库模式（可选）

适用于需要完全控制 worktree 位置的场景。详见 `references/worktree-guide.md`。

---

## 安全护栏（不可协商）

执行任何具有破坏性的 Git 操作前，**必须**遵守以下规则：

### 默认禁止

除非用户显式确认，否则禁止执行以下操作：
- `git push --force*`（包括 `--force-with-lease`）
- `git branch -D ...`
- `rm -rf ...` 或 `Remove-Item -Recurse -Force ...`

### 允许条件（执行前必须全部满足）

执行破坏性操作前，必须：
1. 显示**目标对象清单**：将要影响的分支名、远程分支
2. 检查并展示 `git status --porcelain`：必须为空，或用户明确接受丢弃更改
3. **对于 force push**：明确该分支是否为个人分支；共享分支默认禁止 rebase + force push

### 确认方式

必须采用**二次确认**机制：
- 要求用户输入分支名作为确认 token
- 例如："请输入要删除的分支名以确认"

### 补救说明

执行破坏性操作前，必须提示用户如何补救：
- **删除本地分支前**：提示 `git fetch origin <branch> && git checkout <branch>` 从远程恢复
- **force push 前**：提示如何保留旧 SHA（如 `git reflog`）以及如何回滚

## 前置条件检查

执行前必须检查：
- [ ] Git 版本 >= 2.15
- [ ] 当前目录是 Git 仓库
- [ ] Claude Code 版本 >= 2.1.49（支持原生 worktree）

## 分支命名规范（不可协商）

| 类型 | 格式 | 示例 |
|------|------|------|
| Feature | `feature/<name>` | `feature/user-auth` |
| Release | `release/v<X.Y.Z>` | `release/v1.2.0` |
| Hotfix | `hotfix/<name>` | `hotfix/login-fix` |
| Master/Main | 取决于仓库默认分支 | `master` 或 `main`（自动检测） |
| Develop | `develop` | - |

**禁止使用**：`feat/`、`fix/`、`rel/`、`dev`

## 命令

| 命令 | 说明 |
|------|------|
| `feature start <name>` | 从 develop 创建 feature 分支 |
| `feature finish <name>` | 合并到 develop，删除分支 |
| `release start v<X.Y.Z>` | 从 develop 创建 release 分支 |
| `release finish v<X.Y.Z>` | 合并到 master 和 develop，打 tag |
| `hotfix start <name>` | 从 master 创建 hotfix 分支 |
| `hotfix finish <name>` | 合并到 master 和 develop，打 tag |
| `status` | 显示分支状态和 Claude worktree |
| `cleanup` | 清理已合并分支的 worktree |

## 详细流程

参考：
- `flows/feature-workflow.md`
- `flows/release-workflow.md`
- `flows/hotfix-workflow.md`
- `flows/cleanup-workflow.md`

## Hooks（可选）

配置 Claude Code WorktreeCreate 钩子，自动验证分支名是否符合 GitFlow 规范：

```json
// .claude/settings.json
{
  "hooks": {
    "WorktreeCreate": {
      "command": "~/.claude/hooks/gitflow-worktree-hook.sh"
    }
  }
}
```

详见 `hooks/README.md`。

## Claude Code 原生 Worktree 使用

### 启动隔离开发环境

创建 GitFlow 分支后，使用 Claude Code 原生 worktree 进行隔离开发：

```bash
# 创建 feature 分支
/ease:gitflow feature start user-auth

# 启动 Claude Code 原生 worktree
claude -w feature/user-auth

# Claude 会在 .claude/worktrees/feature-user-auth/ 创建隔离环境
```

### Worktree 目录结构

```
project/
├── .git/
├── .claude/
│   └── worktrees/             # Claude Code 原生 worktree 目录
│       ├── feature-user-auth/ # feature 分支 worktree
│       ├── release-v1.2.0/    # release 分支 worktree
│       └── hotfix-login-fix/  # hotfix 分支 worktree
├── src/
└── ...
```

### 查看活跃的 Worktree

```bash
# 查看 Claude Code 原生 worktree
git worktree list

# 或使用 status 命令
/ease:gitflow status
```

## 参考文档

- `references/gitflow-guide.md` - GitFlow 分支模型指南
- `references/worktree-guide.md` - Git Worktree 使用指南（裸仓库模式）

---

## Common Mistakes

| 错误现象 | 原因 | 修复方法 |
|---|---|---|
| 分支名不符合规范 | 使用了 `feat/` 或 `fix/` | 使用 `feature/`、`release/`、`hotfix/` 前缀 |
| `claude -w` 创建随机分支名 | 未指定已存在的分支 | 先用 GitFlow 创建分支，再用 `claude -w <branch>` |
| force push 后同事无法拉取 | 强推覆盖了远程分支历史 | 立即执行 `git fetch origin && git reset --hard origin/<branch>` 同步 |
| worktree 冲突 | 同一分支已有 worktree | 先删除旧 worktree 或使用不同分支 |

## See Also

- `flows/feature-workflow.md` - Feature 分支工作流
- `flows/release-workflow.md` - Release 分支工作流
- `flows/hotfix-workflow.md` - Hotfix 分支工作流
- `references/gitflow-guide.md` - GitFlow 分支模型指南
- `references/worktree-guide.md` - Git Worktree 使用指南
