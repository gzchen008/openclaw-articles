# Cleanup 工作流

本文档描述如何清理已合并分支的 worktree 和孤儿 worktree。

## 概述

随着开发进展，可能会积累一些已合并分支的 worktree 或无效的 worktree 引用。定期清理可以保持工作环境整洁。

## 命令

```bash
/ease:gitflow cleanup
```

## 执行步骤

### 1. 检查所有 Worktree

```bash
# 列出所有 worktree
git worktree list
```

### 2. 识别已合并分支

```bash
# 检查 feature 分支是否已合并到 develop
git branch --merged develop | grep feature/

# 检查 release/hotfix 分支是否已合并到 master
git branch --merged master | grep -E 'release/|hotfix/'
```

### 3. 清理 Worktree

```bash
# 删除已合并分支的 worktree
git worktree remove .claude/worktrees/feature-completed-feature

# 清理无效引用
git worktree prune
```

### 4. 删除已合并分支

```bash
# 删除本地分支
git branch -d feature/completed-feature

# 删除远程分支（可选）
git push origin --delete feature/completed-feature
```

## 输出示例

```
🧹 Worktree 清理报告

### Claude 原生 Worktree 状态
| Worktree 路径 | 分支 | 状态 |
|--------------|------|------|
| .claude/worktrees/feature-user-auth | feature/user-auth | 活跃 |
| .claude/worktrees/feature-old-task | feature/old-task | 已合并 ✓ |
| .claude/worktrees/release-v1.1.0 | release/v1.1.0 | 已合并 ✓ |

### 清理建议
以下 worktree 可以安全删除：
  1. .claude/worktrees/feature-old-task (分支已合并到 develop)
  2. .claude/worktrees/release-v1.1.0 (分支已合并到 master)

### 执行清理？
输入 'cleanup' 确认删除上述 worktree：
```

## 安全检查

清理前必须检查：

- [ ] worktree 中没有未提交的更改
- [ ] 分支已合并到目标分支
- [ ] 用户确认删除

## 自动化脚本

```bash
#!/bin/bash
# cleanup-merged-worktrees.sh

echo "🧹 清理已合并分支的 worktree..."

# 获取所有 Claude 原生 worktree
WORKTREES=$(git worktree list | grep '.claude/worktrees' | awk '{print $1}')

for worktree in $WORKTREES; do
    # 提取分支名
    branch=$(git -C "$worktree" branch --show-current)

    # 检查分支是否已合并
    if git branch --merged develop | grep -q "$branch" || \
       git branch --merged master | grep -q "$branch"; then
        echo "🗑️ 删除已合并分支的 worktree: $worktree ($branch)"
        git worktree remove "$worktree" 2>/dev/null || \
        echo "⚠️ 无法删除: $worktree"
    fi
done

# 清理无效引用
git worktree prune

echo "✅ 清理完成"
```

## 定期清理建议

建议每周执行一次 cleanup：

```bash
# 每周清理
/ease:gitflow cleanup
```

## 常见问题

### Q: 误删了正在使用的 worktree 怎么办？

可以重新创建 worktree：

```bash
# 重新创建 worktree
claude -w feature/your-feature
```

### Q: worktree prune 会删除什么？

`git worktree prune` 只删除无效的 worktree 引用（目录已删除但引用还在），不会删除实际的 worktree 目录。

### Q: 如何查看哪些分支还没合并？

```bash
# 查看未合并到 develop 的 feature 分支
git branch --no-merged develop | grep feature/

# 查看未合并到 master 的 release/hotfix 分支
git branch --no-merged master | grep -E 'release/|hotfix/'
```
