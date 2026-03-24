# GitFlow 分支模型指南（裸仓库 + Worktree 模式）

## 概述

GitFlow 是由 Vincent Driessen 在 2010 年提出的一种 Git 分支管理模型。本指南结合 **裸仓库 + Worktree** 模式，实现更高效的并行开发体验。

## 工作空间结构

```
my-app-workspace/                # 工作空间根目录
├── .bare/                       # 裸仓库（Git 数据中心）
├── .git                         # 指向 .bare 的文件
├── master/                      # 生产分支 worktree
├── develop/                     # 开发分支 worktree
├── feature/                     # 功能分支目录
│   ├── user-auth/
│   └── payment/
├── release/                     # 发布分支目录
│   └── v1.0.0/
└── hotfix/                      # 热修复分支目录
    └── critical-fix/
```

## 分支类型

### 主要分支（长期存在）

#### 1. master

- **用途**：存储正式发布的历史
- **Worktree 位置**：`<workspace>/master/`
- **特点**：
  - 每个提交都是一个可部署的版本
  - 每个提交都应该有对应的版本标签
  - 只接受来自 release 或 hotfix 的合并
- **保护规则**：禁止直接推送，只能通过 PR 合并

#### 2. develop

- **用途**：日常开发的集成分支
- **Worktree 位置**：`<workspace>/develop/`
- **特点**：
  - 包含下一个版本的最新开发代码
  - 是 feature 分支的基础
  - 相对稳定，但不是生产就绪
- **保护规则**：建议通过 PR 合并

### 支持分支（临时存在）

#### 3. feature/*

- **用途**：开发新功能
- **来源**：从 develop 分支创建
- **去向**：合并回 develop
- **Worktree 位置**：`<workspace>/feature/<name>/`
- **命名**：`feature/<name>`
- **生命周期**：功能开发完成后删除

#### 4. release/*

- **用途**：准备新版本发布
- **来源**：从 develop 分支创建
- **去向**：合并到 master 和 develop
- **Worktree 位置**：`<workspace>/release/v<X.Y.Z>/`
- **命名**：`release/v<X.Y.Z>`
- **生命周期**：发布完成后删除

#### 5. hotfix/*

- **用途**：紧急修复生产问题
- **来源**：从 master 分支创建
- **去向**：合并到 master 和 develop
- **Worktree 位置**：`<workspace>/hotfix/<name>/`
- **命名**：`hotfix/<name>`
- **生命周期**：修复完成后删除

## 分支流程图

```
时间轴 →

master    ──●─────────────────────────●────────●──────────────●──
            │                         │        │              │
            │   Tag: v1.0.0          Tag: v1.1.0  Tag: v1.1.1 Tag: v1.2.0
            │                         ↑        ↑              ↑
            │                         │        │              │
release     │        ┌────────────────┘        │              │
            │        │ release/v1.1.0          │    ┌─────────┘
            │        │                         │    │ release/v1.2.0
            │        │                         │    │
hotfix      │        │                    ┌────┘    │
            │        │                    │ hotfix/ │
            │        │                    │ fix-bug │
            │        │                    │         │
develop   ──●────●───●────●───●──────────●─────────●────●──────●──
            │    ↑   ↓    ↑   │          │               ↑    ↓
            │    │   │    │   │          │               │    │
feature     │    │   │    │   │          │               │    │
            └────┘   │    └───┘          │               └────┘
         feature/a   │  feature/b        │            feature/c
                     │                   │
                     └───────────────────┘
                        合并 release 和 hotfix 的更改
```

## 工作流程详解（裸仓库模式）

### 初始化工作空间

```bash
# 在原项目目录中执行
cd my-app
/ease:gitflow init

# 或手动执行
cd ..
mkdir my-app-workspace && cd my-app-workspace
git clone --bare <repo-url> .bare
echo "gitdir: ./.bare" > .git
git worktree add master master
cd master && git flow init && cd ..
git worktree add develop develop
```

### Feature 流程

```bash
cd my-app-workspace

# 1. 更新 develop 分支
cd develop
git pull origin develop
cd ..

# 2. 创建 feature 分支和 worktree
git worktree add feature/user-auth -b feature/user-auth develop

# 3. 进入 feature 目录开发
cd feature/user-auth

# 4. 开发功能（多次提交）
git add .
git commit -m "feat: add login form"
git add .
git commit -m "feat: implement authentication logic"

# 5. 保持与 develop 同步
git fetch origin
git rebase origin/develop

# 6. 推送分支
git push -u origin feature/user-auth

# 7. 完成后合并到 develop（在 develop 目录中操作）
cd ../develop
git merge --no-ff feature/user-auth -m "Merge branch 'feature/user-auth' into develop"
git push origin develop

# 8. 清理 feature 分支和 worktree
cd ..
git worktree remove feature/user-auth
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```

### Release 流程

```bash
cd my-app-workspace

# 1. 更新 develop 分支
cd develop
git pull origin develop
cd ..

# 2. 创建 release 分支和 worktree
git worktree add release/v1.2.0 -b release/v1.2.0 develop

# 3. 进入 release 目录
cd release/v1.2.0

# 4. 更新版本号和 CHANGELOG
# 编辑 package.json, CHANGELOG.md 等
git commit -m "chore: bump version to 1.2.0"

# 5. 进行最终测试，修复发现的 bug
git commit -m "fix: resolve edge case in payment flow"

# 6. 完成后合并到 master
cd ../../master
git pull origin master
git merge --no-ff release/v1.2.0 -m "Merge branch 'release/v1.2.0' into master"
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin master --tags

# 7. 合并回 develop
cd ../develop
git pull origin develop
git merge --no-ff release/v1.2.0 -m "Merge branch 'release/v1.2.0' into develop"
git push origin develop

# 8. 清理 release 分支和 worktree
cd ..
git worktree remove release/v1.2.0
git branch -d release/v1.2.0
git push origin --delete release/v1.2.0
```

### Hotfix 流程

```bash
cd my-app-workspace

# 1. 更新 master 分支
cd master
git pull origin master
cd ..

# 2. 创建 hotfix 分支和 worktree
git worktree add hotfix/critical-bug -b hotfix/critical-bug master

# 3. 进入 hotfix 目录修复问题
cd hotfix/critical-bug
git commit -m "fix: resolve critical authentication bypass"

# 4. 更新版本号（递增 patch）
git commit -m "chore: bump version to 1.2.1"

# 5. 完成后合并到 master
cd ../../master
git pull origin master
git merge --no-ff hotfix/critical-bug -m "Merge hotfix 'critical-bug' into master"
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git push origin master --tags

# 6. 合并到 develop（或当前的 release 分支）
cd ../develop
git pull origin develop
git merge --no-ff hotfix/critical-bug -m "Merge hotfix 'critical-bug' into develop"
git push origin develop

# 7. 清理 hotfix 分支和 worktree
cd ..
git worktree remove hotfix/critical-bug
git branch -d hotfix/critical-bug
git push origin --delete hotfix/critical-bug
```

## 合并策略

### --no-ff（No Fast-Forward）

始终使用 `--no-ff` 选项合并，保留分支历史：

```bash
# 推荐
git merge --no-ff feature/xxx

# 不推荐（会丢失分支信息）
git merge feature/xxx
```

**对比**：

```
# 使用 --no-ff
* Merge branch 'feature/xxx' into develop
|\
| * feat: add feature C
| * feat: add feature B
| * feat: add feature A
|/
* Previous commit

# 不使用 --no-ff（Fast-Forward）
* feat: add feature C
* feat: add feature B
* feat: add feature A
* Previous commit
```

### Rebase vs Merge

| 场景 | 推荐策略 |
|------|---------|
| 同步 develop 到 feature | Rebase（保持历史整洁） |
| 合并 feature 到 develop | Merge --no-ff（保留分支信息） |
| 多人协作同一 feature | Merge（避免强制推送） |

## 标签管理

### 语义化版本（SemVer）

```
v主版本号.次版本号.修订号
v  MAJOR   . MINOR .PATCH
```

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向下兼容的功能新增
- **PATCH**：向下兼容的问题修复

### 标签创建

```bash
# 在 master 目录中创建标签
cd my-app-workspace/master

# 附注标签（推荐）
git tag -a v1.0.0 -m "Release v1.0.0"

# 推送标签
git push origin v1.0.0
# 或推送所有标签
git push origin --tags
```

## 并行开发优势

使用裸仓库 + Worktree 模式的最大优势是**真正的并行开发**：

```bash
# 同时处理多个任务

# 终端 1：开发新功能
cd my-app-workspace/feature/user-auth
npm run dev

# 终端 2：修复紧急 bug
cd my-app-workspace/hotfix/critical-fix
npm run test

# 终端 3：准备发布
cd my-app-workspace/release/v1.2.0
npm run build

# 无需 stash，无需切换分支，每个目录完全独立
```

## 常见问题

### Q1: 什么时候应该创建 release 分支？

当 develop 分支的功能足够发布时，创建 release 分支。在 release 分支上：
- 只修复 bug
- 更新版本号
- 更新文档
- 不添加新功能

### Q2: hotfix 完成后，如果正在进行 release，应该合并到哪里？

合并到 release 分支而不是 develop，因为 release 最终会合并到 develop。

### Q3: 如何处理长期运行的 feature 分支？

```bash
# 定期同步 develop
cd my-app-workspace/feature/long-running
git fetch origin
git rebase origin/develop
git push --force-with-lease  # 如果已推送到远程
```

### Q4: 可以同时有多个 release 分支吗？

通常不建议。如果需要维护多个版本，考虑：
- 为每个主要版本创建长期分支（如 `v1.x`, `v2.x`）
- 使用 cherry-pick 在版本间移植修复

## 命令速查表

| 操作 | 命令 |
|------|------|
| 创建 feature | `git worktree add feature/<name> -b feature/<name> develop` |
| 创建 release | `git worktree add release/v<X.Y.Z> -b release/v<X.Y.Z> develop` |
| 创建 hotfix | `git worktree add hotfix/<name> -b hotfix/<name> master` |
| 删除 worktree | `git worktree remove <path>` |
| 查看所有 worktree | `git worktree list` |
| 合并分支 | `git merge --no-ff <branch>` |
| 创建标签 | `git tag -a v<X.Y.Z> -m "Release v<X.Y.Z>"` |

## 参考资源

- [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) - 原始文章
- [git-flow cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)
- [Atlassian GitFlow Workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
