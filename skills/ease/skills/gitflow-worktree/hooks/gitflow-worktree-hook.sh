#!/bin/bash
# gitflow-worktree-hook.sh
# 用于 Claude Code WorktreeCreate hook，验证分支名是否符合 GitFlow 规范
#
# 安装方法：
# 1. 复制此脚本到 ~/.claude/hooks/gitflow-worktree-hook.sh
# 2. 添加执行权限：chmod +x ~/.claude/hooks/gitflow-worktree-hook.sh
# 3. 在项目 .claude/settings.json 中配置：
#    {
#      "hooks": {
#        "WorktreeCreate": {
#          "command": "~/.claude/hooks/gitflow-worktree-hook.sh"
#        }
#      }
#    }
#
# 环境变量（由 Claude Code 提供）：
# - WORKTREE_PATH: worktree 的路径
# - WORKTREE_BRANCH: 分支名

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 如果没有分支名，跳过检查
if [ -z "$WORKTREE_BRANCH" ]; then
    echo -e "${YELLOW}⚠️ 未检测到分支名，跳过 GitFlow 验证${NC}"
    exit 0
fi

echo "🔍 检查分支名是否符合 GitFlow 规范: $WORKTREE_BRANCH"

# 检查分支名是否符合 GitFlow 规范
is_valid_gitflow_branch() {
    local branch="$1"

    # 允许的主分支名
    if [[ "$branch" == "master" || "$branch" == "main" || "$branch" == "develop" ]]; then
        return 0
    fi

    # 允许 feature 分支
    if [[ "$branch" == feature/* ]]; then
        return 0
    fi

    # 允许 release 分支（验证版本号格式）
    if [[ "$branch" == release/* ]]; then
        local version="${branch#release/}"
        if [[ "$version" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            return 0
        else
            echo -e "${YELLOW}⚠️ 版本号格式建议: vX.Y.Z (当前: $version)${NC}"
            return 0  # 仍然允许，只是警告
        fi
    fi

    # 允许 hotfix 分支
    if [[ "$branch" == hotfix/* ]]; then
        return 0
    fi

    return 1
}

# 检查分支是否存在
branch_exists() {
    git show-ref --verify --quiet "refs/heads/$1" 2>/dev/null
}

# 主逻辑
if is_valid_gitflow_branch "$WORKTREE_BRANCH"; then
    echo -e "${GREEN}✅ GitFlow 分支验证通过: $WORKTREE_BRANCH${NC}"

    # 如果分支不存在，提示用户先用 GitFlow 创建
    if ! branch_exists "$WORKTREE_BRANCH"; then
        echo ""
        echo -e "${YELLOW}⚠️ 分支 $WORKTREE_BRANCH 不存在${NC}"
        echo ""
        echo "建议先使用 GitFlow 创建分支："
        echo ""

        case "$WORKTREE_BRANCH" in
            feature/*)
                echo "  /ease:gitflow feature start ${WORKTREE_BRANCH#feature/}"
                ;;
            release/*)
                echo "  /ease:gitflow release start ${WORKTREE_BRANCH#release/}"
                ;;
            hotfix/*)
                echo "  /ease:gitflow hotfix start ${WORKTREE_BRANCH#hotfix/}"
                ;;
        esac

        echo ""
        echo "然后重新运行: claude -w $WORKTREE_BRANCH"
    fi

    exit 0
else
    echo -e "${RED}❌ 分支名 '$WORKTREE_BRANCH' 不符合 GitFlow 规范${NC}"
    echo ""
    echo "GitFlow 分支命名规范："
    echo ""
    echo "  feature/<name>    - 功能分支"
    echo "  release/vX.Y.Z    - 发布分支"
    echo "  hotfix/<name>     - 热修复分支"
    echo ""
    echo "示例："
    echo "  feature/user-auth"
    echo "  release/v1.2.0"
    echo "  hotfix/login-fix"
    echo ""
    echo "请先使用 GitFlow 创建分支："
    echo "  /ease:gitflow feature start <name>"
    echo "  /ease:gitflow release start vX.Y.Z"
    echo "  /ease:gitflow hotfix start <name>"
    echo ""
    echo "然后重新运行: claude -w <gitflow-branch-name>"

    exit 1
fi
