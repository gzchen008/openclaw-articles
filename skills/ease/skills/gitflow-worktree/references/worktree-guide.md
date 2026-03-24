# Git Worktree 使用指南

## 概述

本指南介绍两种 Worktree 使用模式：

1. **Claude Code 原生模式**（推荐）- 使用 `claude -w` 命令
2. **裸仓库模式**（可选）- 完全控制 worktree 位置

---

## 模式一：Claude Code 原生 Worktree（推荐）

### 基本使用

```bash
# 在已存在的 GitFlow 分支上创建 worktree
claude -w feature/user-auth

# Claude 会自动：
# 1. 在 .claude/worktrees/feature-user-auth/ 创建 worktree
# 2. 检出 feature/user-auth 分支
# 3. 启动新的 Claude 会话
```

### 目录结构

```
project/
├── .git/
├── .claude/
│   └── worktrees/             # Claude Code 原生 worktree 目录
│       ├── feature-user-auth/
│       ├── release-v1.2.0/
│       └── hotfix-login-fix/
├── src/
└── ...
```

### 常用命令

```bash
# 查看所有 worktree
git worktree list

# 删除 worktree
git worktree remove .claude/worktrees/feature-user-auth

# 清理无效引用
git worktree prune
```

### 优势

- ✅ 零配置，开箱即用
- ✅ 与 Claude Code 深度集成
- ✅ 自动管理 worktree 生命周期
- ✅ 支持 Agent 隔离

---

## 模式二：裸仓库模式（可选）

适用于需要完全控制 worktree 位置的场景。

### 为什么使用裸仓库模式？

#### 传统 Worktree 的问题

```bash
# 传统方式：主仓库绑定在一个分支上
project/                  # 主仓库，绑定 develop 分支
├── .git/                 # 完整的 Git 目录
├── src/
└── ...

# 问题：
# 1. 主仓库和 worktree 分散在不同位置
# 2. 需要记住哪个目录是"主仓库"
# 3. 删除主仓库会影响所有 worktree
```

#### 裸仓库模式的优势

```bash
# 裸仓库模式：所有分支平等
my-app-workspace/         # 统一的工作空间
├── .bare/               # 裸仓库（所有 Git 数据）
├── .git                 # 指向 .bare 的文件
├── master/              # master 分支
├── develop/             # develop 分支
├── feature/
│   └── user-auth/       # feature 分支
└── release/
    └── v1.0.0/          # release 分支

# 优势：
# 1. 所有分支在同一个目录下，结构清晰
# 2. 没有"主仓库"概念，所有 worktree 平等
# 3. 便于管理和备份
```

### 裸仓库模式初始化

#### 完整初始化步骤

```bash
# 假设原项目目录是 my-app，远程仓库地址是 git@github.com:user/my-app.git

# 1. 获取仓库地址（在原项目目录中）
cd my-app
REMOTE_URL=$(git remote get-url origin)
echo $REMOTE_URL

# 2. 在项目同级创建工作空间目录
cd ..
mkdir my-app-workspace
cd my-app-workspace

# 3. 克隆裸仓库
git clone --bare $REMOTE_URL .bare

# 4. 创建 .git 文件指向裸仓库（关键步骤）
echo "gitdir: ./.bare" > .git

# 5. 配置裸仓库
cd .bare
git config core.bare false
git config core.worktree "../"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
cd ..

# 6. 创建 master worktree
git worktree add master master

# 7. 进入 master 目录初始化 git flow
cd master
git flow init
cd ..

# 8. 创建 develop worktree
git worktree add develop develop
```

### 裸仓库模式目录结构详解

```
my-app-workspace/                # 工作空间根目录
├── .bare/                       # 裸仓库
│   ├── config                   # Git 配置
│   ├── HEAD                     # 当前 HEAD 引用
│   ├── objects/                 # Git 对象存储
│   ├── refs/                    # 分支和标签引用
│   │   ├── heads/              # 本地分支
│   │   └── remotes/            # 远程分支
│   └── worktrees/              # worktree 元数据
│       ├── master/
│       ├── develop/
│       └── feature-xxx/
├── .git                         # 指向 .bare 的文件（内容: "gitdir: ./.bare"）
├── master/                      # master 分支 worktree
│   ├── .git                    # 指向 .bare/worktrees/master
│   ├── src/
│   └── ...
├── develop/                     # develop 分支 worktree
│   ├── .git
│   └── ...
├── feature/                     # feature 分支目录
│   └── user-auth/              # feature/user-auth 分支
│       ├── .git
│       └── ...
├── release/                     # release 分支目录
│   └── v1.0.0/
└── hotfix/                      # hotfix 分支目录
    └── critical-fix/
```

### .git 文件说明

在裸仓库模式中，`.git` 是一个**文件**而不是目录：

```bash
# 工作空间根目录的 .git 文件
cat my-app-workspace/.git
# 输出: gitdir: ./.bare

# worktree 中的 .git 文件
cat my-app-workspace/master/.git
# 输出: gitdir: /path/to/my-app-workspace/.bare/worktrees/master
```

## 裸仓库模式日常操作

### 创建新分支

```bash
cd my-app-workspace

# 创建 feature 分支
git worktree add feature/user-auth -b feature/user-auth develop
cd feature/user-auth
# 开始开发...

# 创建 release 分支
git worktree add release/v1.0.0 -b release/v1.0.0 develop

# 创建 hotfix 分支
git worktree add hotfix/critical-fix -b hotfix/critical-fix master
```

### 查看所有 worktree

```bash
cd my-app-workspace
git worktree list

# 输出示例:
# /path/to/my-app-workspace/.bare         (bare)
# /path/to/my-app-workspace/master        abc1234 [master]
# /path/to/my-app-workspace/develop       def5678 [develop]
# /path/to/my-app-workspace/feature/user-auth  ghi9012 [feature/user-auth]
```

### 删除分支和 worktree

```bash
cd my-app-workspace

# 删除 worktree
git worktree remove feature/user-auth

# 如果有未提交的更改，强制删除
git worktree remove --force feature/user-auth

# 清理无效的 worktree 引用
git worktree prune
```

### 同步代码

```bash
cd my-app-workspace

# 在任意 worktree 中拉取更新
cd develop
git fetch origin
git pull origin develop

# 更新所有分支（在根目录执行）
cd ..
for dir in master develop feature/* release/* hotfix/*; do
    if [ -d "$dir" ]; then
        echo "Updating $dir..."
        cd "$dir"
        git pull origin $(git branch --show-current) 2>/dev/null || true
        cd ..
    fi
done
```

## 高级用法

### 快速切换上下文

```bash
# 不需要 git checkout，直接 cd 到不同目录
cd my-app-workspace/develop      # 开发功能
cd ../feature/user-auth          # 切换到 feature
cd ../master                     # 查看生产代码

# 可以在不同终端窗口同时工作于不同分支
```

### 并行构建

```bash
# 在 CI/CD 中并行构建多个分支
cd my-app-workspace

# 并行运行测试
(cd master && npm test) &
(cd develop && npm test) &
(cd feature/user-auth && npm test) &
wait
```

### 代码对比

```bash
# 直接使用文件对比工具
diff my-app-workspace/master/src my-app-workspace/develop/src

# 或使用 IDE 对比
code --diff my-app-workspace/master/src/app.ts my-app-workspace/develop/src/app.ts
```

## 注意事项

### 1. 不要在 worktree 中切换分支

```bash
# ❌ 错误做法
cd feature/user-auth
git checkout develop  # 不要这样做！

# ✅ 正确做法
cd ../develop        # 直接切换目录
```

### 2. 每个分支只能有一个 worktree

```bash
# 一个分支不能同时在两个 worktree 中检出
git worktree add new-develop develop
# fatal: 'develop' is already checked out at '/path/to/develop'
```

### 3. 依赖需要分别安装

```bash
# 每个 worktree 需要独立安装依赖
cd feature/user-auth
npm install  # 或 yarn install
```

### 4. IDE 配置

每个 worktree 作为独立项目打开：

```bash
# VSCode
code my-app-workspace/feature/user-auth

# IntelliJ IDEA
idea my-app-workspace/feature/user-auth
```

## 常见问题

### Q: 如何迁移现有项目到裸仓库模式？

```bash
# 1. 获取仓库地址
cd my-app
REMOTE_URL=$(git remote get-url origin)

# 2. 创建工作空间
cd ..
mkdir my-app-workspace
cd my-app-workspace

# 3. 克隆裸仓库
git clone --bare $REMOTE_URL .bare
echo "gitdir: ./.bare" > .git

# 4. 配置并创建 worktree
cd .bare
git config core.bare false
git config core.worktree "../"
git fetch origin
cd ..
git worktree add master master
git worktree add develop develop

# 5. 可以删除或保留原项目目录
```

### Q: 如何备份整个工作空间？

```bash
# 只需备份 .bare 目录即可，它包含所有 Git 数据
tar -czf backup.tar.gz my-app-workspace/.bare

# 恢复时重新创建 worktree
cd my-app-workspace
git worktree add master master
git worktree add develop develop
```

### Q: worktree 目录可以移动位置吗？

```bash
# 可以使用 git worktree move
git worktree move feature/old-name feature/new-name
```

### Q: 如何处理子模块？

```bash
# 每个 worktree 需要初始化子模块
cd feature/user-auth
git submodule update --init --recursive
```

## 命令速查表

| 命令 | 说明 |
|------|------|
| `git worktree add <path> <branch>` | 添加已存在分支的 worktree |
| `git worktree add <path> -b <new-branch> <start>` | 创建新分支并添加 worktree |
| `git worktree list` | 列出所有 worktree |
| `git worktree remove <path>` | 删除 worktree |
| `git worktree prune` | 清理无效的 worktree 引用 |
| `git worktree move <old> <new>` | 移动 worktree |
| `git worktree lock <path>` | 锁定 worktree |
| `git worktree unlock <path>` | 解锁 worktree |

## 参考资源

- [Git Worktree 官方文档](https://git-scm.com/docs/git-worktree)
- [Git Bare Repository](https://git-scm.com/book/en/v2/Git-on-the-Server-Getting-Git-on-a-Server)
