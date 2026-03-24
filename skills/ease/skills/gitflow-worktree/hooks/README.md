# GitFlow Worktree Hooks

本目录包含用于 Claude Code Worktree 钩子的脚本。

## 文件说明

| 文件 | 说明 |
|------|------|
| `gitflow-worktree-hook.sh` | WorktreeCreate 钩子，验证分支名是否符合 GitFlow 规范 |

## 安装方法

### 1. 复制钩子脚本

```bash
# 创建钩子目录
mkdir -p ~/.claude/hooks

# 复制脚本
cp gitflow-worktree-hook.sh ~/.claude/hooks/

# 添加执行权限
chmod +x ~/.claude/hooks/gitflow-worktree-hook.sh
```

### 2. 配置 Claude Code 钩子

在项目根目录创建或编辑 `.claude/settings.json`：

```json
{
  "hooks": {
    "WorktreeCreate": {
      "command": "~/.claude/hooks/gitflow-worktree-hook.sh"
    }
  }
}
```

### 3. 验证安装

```bash
# 测试钩子
claude -w feature/test-hook
```

## 钩子行为

### WorktreeCreate 钩子

当使用 `claude -w <branch>` 创建 worktree 时，钩子会：

1. **验证分支名**：检查是否符合 GitFlow 规范
2. **提示创建分支**：如果分支不存在，提示使用 `/ease:gitflow` 创建
3. **拒绝非法分支名**：不符合规范的分支名会被拒绝

### GitFlow 分支命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| Feature | `feature/<name>` | `feature/user-auth` |
| Release | `release/vX.Y.Z` | `release/v1.2.0` |
| Hotfix | `hotfix/<name>` | `hotfix/login-fix` |

### 示例输出

**成功验证：**
```
🔍 检查分支名是否符合 GitFlow 规范: feature/user-auth
✅ GitFlow 分支验证通过: feature/user-auth
```

**分支不存在：**
```
🔍 检查分支名是否符合 GitFlow 规范: feature/new-feature
✅ GitFlow 分支验证通过: feature/new-feature

⚠️ 分支 feature/new-feature 不存在

建议先使用 GitFlow 创建分支：

  /ease:gitflow feature start new-feature

然后重新运行: claude -w feature/new-feature
```

**拒绝非法分支名：**
```
🔍 检查分支名是否符合 GitFlow 规范: claude/focused-pare
❌ 分支名 'claude/focused-pare' 不符合 GitFlow 规范

GitFlow 分支命名规范：

  feature/<name>    - 功能分支
  release/vX.Y.Z    - 发布分支
  hotfix/<name>     - 热修复分支

示例：
  feature/user-auth
  release/v1.2.0
  hotfix/login-fix

请先使用 GitFlow 创建分支：
  /ease:gitflow feature start <name>
  /ease:gitflow release start vX.Y.Z
  /ease:gitflow hotfix start <name>

然后重新运行: claude -w <gitflow-branch-name>
```

## 自定义配置

### 禁用钩子

如果需要临时禁用钩子，可以：

1. **移除配置**：从 `.claude/settings.json` 中移除 hooks 配置
2. **修改脚本**：在脚本开头添加 `exit 0`

### 扩展钩子

可以在钩子脚本中添加额外的验证逻辑，例如：

- 检查分支名长度限制
- 验证版本号格式
- 添加自定义分支前缀

## 故障排除

### 钩子不生效

1. 确认脚本有执行权限：`chmod +x ~/.claude/hooks/gitflow-worktree-hook.sh`
2. 确认配置文件路径正确
3. 检查 Claude Code 版本是否支持 WorktreeCreate 钩子（>= v2.1.50）

### 钩子报错

查看错误信息，通常是：
- 分支名不符合 GitFlow 规范
- 脚本路径不正确
- 权限问题
