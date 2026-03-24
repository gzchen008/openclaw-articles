# git-branch-review

批量审查多个 git 分支的修改，理解每个分支的功能，帮助用户选择合并哪些分支到当前分支。

## 使用方法

```bash
# 启动完整的分支审查流程
git-branch-review

# 只审查指定模式的分支
git-branch-review --pattern "feature/*"

# 审查最近 7 天的分支
git-branch-review --since "7 days ago"
```

## 工作流程

### 1. 扫描远程分支

自动获取远程仓库中所有未合并到当前分支的分支：

```bash
git fetch origin
git branch -r --no-merged
```

### 2. Worktree 隔离

为每个分支创建独立的 worktree 目录：

```
/tmp/git-branch-review-1707581234/
├── feature-user-auth/
├── fix-login-bug/
└── docs-api-update/
```

**为什么使用 worktree？**
- 完全隔离，不会污染当前工作区
- 可以并行查看多个分支的代码
- 安全，原仓库保持干净

### 3. 分析分支内容

对每个分支进行深度分析：
- **功能摘要**：AI 理解分支的主要目的
- **影响范围**：修改了哪些文件和模块
- **风险等级**：高/中/低
- **冲突预测**：与当前分支的重叠程度
- **变更统计**：提交数、增删行数

### 4. 生成分支报告

示例报告：

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
└─────────────────────────────────────────────────────────┘
```

### 5. 用户选择

交互式选择：

```
请选择要合并的分支：
- 输入 "all" 合并所有分支
- 输入 "none" 取消操作
- 输入分支编号如 "1,3" 选择性合并

你的选择: 1,3
```

### 6. 合并预览

执行合并前显示预览：

```
即将合并以下分支到 main：
✓ feature/user-auth
✓ docs/api-update

影响的文件：
  src/auth/jwt.ts         (新增)
  src/auth/session.ts     (新增)
  docs/api/auth.md        (新增)
  docs/api/user.md        (修改)

预计冲突：无

确认合并？ (yes/no)
```

### 7. 执行合并

逐个合并选中的分支：

```bash
git merge --no-ff origin/feature/user-auth -m "Merge branch 'feature/user-auth'"
git merge --no-ff origin/docs/api-update -m "Merge branch 'docs/api-update'"
```

### 8. 清理

合并完成后自动清理 worktree：

```bash
git worktree remove /tmp/git-branch-review-1707581234/feature-user-auth
git worktree remove /tmp/git-branch-review-1707581234/docs-api-update
rm -rf /tmp/git-branch-review-1707581234
```

## 选项

| 选项 | 说明 | 示例 |
|------|------|------|
| `--pattern` | 只审查匹配模式的分支 | `--pattern "feature/*"` |
| `--since` | 只审查指定时间后的分支 | `--since "7 days ago"` |
| `--exclude` | 排除匹配模式的分支 | `--exclude "wip/*"` |
| `--base` | 指定对比的基准分支 | `--base develop` |

## 最佳实践

### 发布前审查

```bash
# 准备发布前，审查所有 feature 分支
git-branch-review --pattern "feature/*"
```

### 定期清理

```bash
# 每周审查一次，合并不需要保留的分支
git-branch-review --since "7 days ago"
```

### 紧急修复优先

```bash
# 优先处理 fix 分支
git-branch-review --pattern "fix/*"
```

## 冲突处理

如果合并时出现冲突：

1. **停止合并**：流程会暂停，保留已成功的合并
2. **冲突提示**：显示哪些文件有冲突
3. **解决指导**：提供解决冲突的建议
4. **手动解决**：用户手动解决冲突后继续
5. **恢复流程**：解决后可以重新运行命令继续

## 安全提示

⚠️ **合并前请确保：**
- 当前分支已 push 到远程（可回滚）
- CI/CD 测试已通过
- 代码审查已完成

💡 **建议操作：**
```bash
# 创建备份分支
git branch backup-$(git branch --show-current)

# 然后执行合并
git-branch-review
```

## 相关命令

- `git-branch-cleanup` - 清理临时 worktree
- `git-worktree` - Git worktree 底层命令
