---
name: git-branch-merge
description: 批量审查多个 git 分支的修改，理解每个分支的功能，帮助用户选择合并哪些分支到当前分支。使用 git worktree 进行分支隔离。
tools: Glob, Grep, Read, BashOutput, Bash, Edit, Write
model: inherit
---

# Git Branch Merge

## Overview

智能批量分支审查与合并助手。扫描远程仓库的多个新分支，使用 git worktree 隔离检出每个分支，分析修改内容并生成功能摘要，汇总展示后让用户选择要合并的分支，最终合并到当前分支。

## When to Use

**Use when:**
- 需要批量审查多个远程分支的修改内容
- 想理解每个分支具体做了什么功能
- 需要从多个分支中选择性地合并到当前分支
- 希望使用 worktree 方式隔离分支，避免污染当前工作区

**Do NOT use:**
- 单个分支的简单合并 → 直接使用 `git merge`
- 只想查看某个分支的 diff → 使用 `git diff`
- 分支已经本地检出 → 不需要 worktree 隔离
- 需要解决复杂合并冲突 → 手动处理更合适

## Quick Reference

| 你想做... | 第一步 | 然后... |
|-----------|--------|---------|
| 批量审查多个远程分支 | 扫描远程分支 | 使用 worktree 隔离检出 |
| 理解分支功能 | 分析 diff 和 commit | 生成功能摘要 |
| 选择合并分支 | 展示分支列表 | 用户选择 + 确认 |
| 合并到当前分支 | 执行 merge | 验证合并结果 |

## Workflow

### 0. 前置检查

**基线分支自动检测（main vs master）：**
```bash
# 检测远程默认分支
BASE_BRANCH=$(git remote show origin | grep 'HEAD branch' | awk '{print $NF}')
echo "检测到基线分支: $BASE_BRANCH"
```

**工作区状态检查：**
```bash
# 确保当前工作区干净
git status --porcelain
# 如果有未提交更改，提���用户先处理
```

**前置条件：**
- [ ] Git 版本 >= 2.15（支持 worktree）
- [ ] 当前工作区无未提交更改（或用户确认可以继续）
- [ ] 远程仓库可访问（`git ls-remote origin` 成功）
- [ ] /tmp 目录有足够磁盘空间

### 1. 扫描远程分支

首先获取远程分支列表，识别需要审查的分支：

```bash
# 获取所有远程分支（排除已合并的）
git fetch origin --prune
git branch -r --no-merged "$BASE_BRANCH" | grep -v HEAD
```

**过滤建议：**
- 排除已经合并到当前分支的分支
- 可以按命名模式过滤（如 `feature/*`, `fix/*`）
- 可以指定时间范围（最近 N 天的分支）
- 排除 `dependabot/*`、`renovate/*` 等自动化分支（除非用户指定）

### 2. Worktree 隔离检出

**核心原则：** 使用 git worktree 隔离每个分支，避免污染当前工作区

```bash
# 为每个分支创建独立的 worktree
WORKTREE_BASE="/tmp/git-branch-review-$(date +%s)"
mkdir -p "$WORKTREE_BASE"

# 示例：检出 feature/user-auth 分支
git worktree add "$WORKTREE_BASE/feature-user-auth" origin/feature/user-auth

# 示例：检出 fix/login-bug 分支  
git worktree add "$WORKTREE_BASE/fix-login-bug" origin/fix/login-bug
```

**Worktree 优势：**
- 完全隔离：每个分支在独立目录，互不干扰
- 并行分析：可以同时查看多个分支的代码
- 安全：原仓库工作区保持干净
- 易清理：完成后一次性删除临时目录

### 3. 分析分支内容

对每个 worktree 中的分支进行分析：

**A. 基础信息收集**
```bash
# 提交数量（相对于基线分支）
git log --oneline "$BASE_BRANCH"..HEAD | wc -l

# 修改的文件列表
git diff --name-only "$BASE_BRANCH"...HEAD

# 统计变更行数
git diff --stat "$BASE_BRANCH"...HEAD

# 最近提交的作者和时间
git log --format="%an (%ar)" "$BASE_BRANCH"..HEAD | head -5
```

**B. 功能理解**
分析以下方面生成摘要：
- **主要功能**：这个分支实现了什么功能/修复了什么 bug
- **影响范围**：修改了哪些模块/文件
- **风险等级**：高风险（核心逻辑）/ 中风险（次要功能）/ 低风险（文档、样式）
- **合并冲突可能性**：基于修改文件与主分支的重叠度
- **测试覆盖**：是否有测试文件修改

### 4. 汇总展示

生成格式化的分支摘要报告：

```
┌─────────────────────────────────────────────────────────┐
│              分支审查报告 (共 3 个分支)                   │
├─────────────────────────────────────────────────────────┤
│ [1] feature/user-auth                                   │
│     功能：实现用户认证系统（JWT + Session）               │
│     影响：src/auth/, src/middleware/ (12 个文件)         │
│     风险：⚠️ 高（核心安全功能）                          │
│     冲突：🟡 中等（与 main 有 3 个文件重叠）              │
│     提交：8 个 (+420, -85 行)                           │
│     测试：✅ 包含完整测试覆盖                            │
├─────────────────────────────────────────────────────────┤
│ [2] fix/login-redirect                                  │
│     功能：修复登录后重定向 URL 错误                      │
│     影响：src/auth/login.ts                             │
│     风险：🟢 低（单行修复）                              │
│     冲突：🟢 低（无重叠）                                │
│     提交：2 个 (+5, -3 行)                              │
│     测试：✅ 包含回归测试                                │
├─────────────────────────────────────────────────────────┤
│ [3] docs/api-update                                     │
│     功能：更新 API 文档，添加新的端点说明                │
│     影响：docs/api/*.md                                 │
│     风险：🟢 低（仅文档）                                │
│     冲突：🟢 低（无重叠）                                │
│     提交：3 个 (+120, -20 行)                           │
│     测试：❌ 不涉及代码                                  │
└─────────────────────────────────────────────────────────┘
```

### 5. 用户选择

提供交互式选择界面：

```
请选择要合并的分支（输入数字，多个用逗号分隔）：
- 输入 "all" 合并所有分支
- 输入 "none" 取消操作
- 输入分支编号如 "1,3" 选择性合并

你的选择: _
```

### 5.5 合并顺序策略

用户选择后，按以下优先级排序合并顺序：

1. **低风险优先**：文档、样式等低风险分支先合并
2. **无冲突优先**：与当前分支无文件重叠的分支先合并
3. **小范围优先**：修改文件少的分支先合并
4. **依赖关系**：如果分支间有依赖，被依赖的先合并

### 5.6 合并前冲突预检

对每个选中的分支执行 dry-run 检测：

```bash
# 冲突预检（不实际合并）
git merge --no-commit --no-ff "origin/$BRANCH" 2>&1
MERGE_STATUS=$?

# 检查结果
if [ $MERGE_STATUS -ne 0 ]; then
    echo "⚠️ 分支 $BRANCH 存在合并冲突"
    git diff --name-only --diff-filter=U  # 列出冲突文件
    git merge --abort  # 回滚 dry-run
else
    echo "✅ 分支 $BRANCH 可以无冲突合并"
    git merge --abort  # 回滚 dry-run
fi
```

**冲突处理策略：**
- 无冲突：直接合并
- 有冲突：警告用户，提供冲突文件列表，让用户决定是否继续
- 多个分支有冲突：建议用户逐个处理，而非批量合并

### 6. 执行合并

**安全合并流程：**

```bash
# 1. 回到原仓库目录
cd /path/to/original/repo

# 2. 确保当前分支正确
CURRENT=$(git branch --show-current)
echo "当前分支: $CURRENT"

# 3. 创建备份分支（安全网）
git branch "backup-${CURRENT}-$(date +%Y%m%d%H%M%S)"

# 4. 拉取最新代码
git pull origin "$CURRENT"

# 5. 按排序后的顺序逐个合并
for branch in $SORTED_BRANCHES; do
    echo "━━━ 正在合并: $branch ━━━"

    # 使用 --no-ff 保留合并历史
    git merge --no-ff "origin/$branch" -m "Merge branch '$branch' into $CURRENT"

    if [ $? -ne 0 ]; then
        echo "⚠️ 合并 $branch 时出现冲突"
        echo "冲突文件："
        git diff --name-only --diff-filter=U
        echo ""
        echo "选项："
        echo "  1. 手动解决冲突后继续"
        echo "  2. 放弃本次合并 (git merge --abort)"
        echo "  3. 停止所有后续合并"
        break
    fi

    echo "✅ $branch 合并成功"
done
```

### 7. 清理 Worktree

合并完成后清理临时 worktree：

```bash
# 移除 worktree
git worktree remove "$WORKTREE_BASE/feature-user-auth"
git worktree remove "$WORKTREE_BASE/fix-login-bug"
# ...

# 删除临时目录
rm -rf "$WORKTREE_BASE"

# 清理远程分支引用（可选）
git worktree prune
```

## Post-Merge Verification

合并完成后必须验证：

- [ ] **合并成功**：`git log --oneline -5` 显示正确的合并提交
- [ ] **无残留冲突**：`git diff --check` 无冲突标记
- [ ] **Worktree 已清理**：`git worktree list` 无临时 worktree
- [ ] **工作区干净**：`git status --porcelain` 为空
- [ ] **提示用户验证**：建议运行项目测试确认合并后代码正常

## Non-negotiables

### Safety Rules (MUST Follow)

**NEVER 自动合并：**
- 必须经过用户明确确认后才执行 merge
- 高风险分支（修改核心逻辑）需要额外确认
- 显示完整的合并预览（哪些文件会被修改）

**冲突预警：**
- 在合并前检测可能的冲突
- 如果检测到冲突，提前警告用户
- 提供冲突文件的详细信息

**Worktree 隔离：**
- 必须使用 git worktree 隔离分支
- 禁止直接在原仓库 checkout 其他分支
- 临时目录必须位于 /tmp 或类似位置

**备份提醒：**
- 提醒用户在合并前确保当前分支已 push
- 建议创建备份分支：`git branch backup-main`

### 禁止操作

- NEVER 使用 `--force` 或 `-f` 选项
- NEVER 自动删除远程分支
- NEVER 在 merge 时自动使用 `--no-verify` 跳过 hooks
- NEVER 在检测到冲突时自动选择 "theirs" 或 "ours"

## Edge Cases

| 场景 | 处理策略 |
|------|---------|
| **分支已被合并** | 跳过该分支，提示用户 |
| **分支不存在** | 报告错误，继续处理其他分支 |
| **Worktree 创建失败** | 检查磁盘空间、权限，重试或报错 |
| **磁盘空间不足** | 提前检查可用空间，清理旧 worktree |
| **合并冲突** | 停止合并，提供冲突解决指导 |
| **网络问题** | fetch 失败时重试 3 次，然后报错 |
| **同名 worktree 已存在** | 使用时间戳命名，避免冲突 |

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 直接 checkout 分支 | 污染当前工作区，丢失未提交更改 | 使用 git worktree 隔离 |
| 自动合并所有分支 | 可能合并不需要或有问题的代码 | 总是让用户选择 |
| 不检查冲突风险 | 合并时出现大量冲突 | 提前分析文件重叠度 |
| 忘记清理 worktree | 磁盘空间被占用 | 合并后自动清理 |
| 不验证合并结果 | 合并后代码可能无法运行 | 提示用户验证测试 |

## Examples

### 示例 1：批量审查 feature 分支

```
用户：帮我审查所有 feature 分支，选择合并到 develop

执行流程：
1. git fetch origin --prune
2. 发现 5 个 feature/* 分支
3. 创建 worktree: /tmp/git-branch-review-1700000000/
   ├── feature-user-auth/
   ├── feature-payment/
   ├── feature-notification/
   ├── feature-dashboard/
   └── feature-search/
4. 分析每个分支 → 生成摘要报告
5. 用户选择: "1,2,5"（user-auth, payment, search）
6. 冲突预检 → 全部通过
7. 按风险排序合并: search → payment → user-auth
8. 清理 worktree + 删除临时目录
9. 提示用户运行测试验证
```

### 示例 2：处理紧急修复分支

```
用户：审查所有 fix 分支，尽快合并到 main

执行流程：
1. 扫描发现 3 个 fix/* 分支
2. 分析结果：
   - fix/login-redirect: 1 文件, +5/-3 行, 低风险
   - fix/memory-leak: 4 文件, +45/-12 行, 中风险
   - fix/data-corruption: 8 文件, +120/-80 行, 高风险
3. 建议合并顺序: login-redirect → memory-leak → data-corruption
4. 对 data-corruption 额外警告：修改了核心数据层，建议单独审查
5. 用户选择: "all"
6. 逐个合并，每个合并后确认
```

### 示例 3：发布前合并

```
用户：准备发布 v2.0，审查所有待合并分支

执行流程：
1. 扫描所有未合并到 release/v2.0 的分支
2. 自动排除: WIP 分支、dependabot 分支
3. 生成详细报告（含测试覆盖率信息）
4. 用户逐一确认每个分支
5. 批量合并 + 验证无冲突
6. 提示用户: "建议运行完整测试套件后再推送"
```

## Commands

### Command: git-branch-review

**描述**：启动完整的分支审查流程

**用法**：
```bash
# 审查所有远程未合并分支
git-branch-review

# 审查指定模式的分支
git-branch-review --pattern "feature/*"
git-branch-review --pattern "fix/*"

# 审查最近 N 天的分支
git-branch-review --since "7 days ago"
```

**交互流程**：
1. 显示发现的分支列表
2. 创建 worktree（显示进度）
3. 分析分支内容（显示进度）
4. 展示摘要报告
5. 用户选择要合并的分支
6. 显示合并预览
7. 执行合并
8. 清理并总结

### Command: git-branch-cleanup

**描述**：清理所有临时 worktree

**用法**：
```bash
# 列出所有临时 worktree
git-branch-cleanup --list

# 清理所有临时 worktree
git-branch-cleanup --all

# 清理特定分支的 worktree
git-branch-cleanup --branch feature/test
```

## See Also

### Upstream (Related Skills)
- `gitflow-worktree/SKILL.md` - Git worktree 操作基础
- `git-commit/SKILL.md` - 提交规范

### Downstream (Next Steps)
- 合并后可能需要运行测试
- 可能需要更新版本号和 changelog

### References
- `commands/git-branch-review.md` - 命令详细说明
- Git worktree 文档: https://git-scm.com/docs/git-worktree
