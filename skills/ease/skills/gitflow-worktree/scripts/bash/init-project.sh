#!/bin/bash

# GitFlow Worktree 项目初始化脚本（裸仓库模式）
# 
# 初始化流程：
# 1. 获取当前项目的仓库地址
# 2. 在项目同级创建 <project>-workspace 目录
# 3. 克隆裸仓库到 .bare 目录
# 4. 创建 .git 文件指向裸仓库
# 5. 创建 master worktree
# 6. 初始化 git flow
#
# 最终目录结构：
# my-app-workspace/
#   ├── .bare/        # 裸仓库
#   ├── .git          # 指向 .bare 的文件
#   ├── master/       # master 分支 worktree
#   ├── develop/      # develop 分支 worktree
#   └── ...

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
MASTER_BRANCH="master"
DEVELOP_BRANCH="develop"

# 解析参数
FORCE=0
SKIP_GITFLOW=0

print_usage() {
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --force, -f         强制重新初始化（清除现有工作空间）"
    echo "  --skip-gitflow      跳过 git flow 初始化"
    echo "  --master <branch>   指定主分支名称 (默认: master)"
    echo "  --develop <branch>  指定开发分支名称 (默认: develop)"
    echo "  --help, -h          显示帮助信息"
    echo ""
    echo "示例:"
    echo "  $0                  # 在当前项目目录执行初始化"
    echo "  $0 --force          # 强制重新初始化"
}

while [[ $# -gt 0 ]]; do
    case $1 in
        --force|-f)
            FORCE=1
            shift
            ;;
        --skip-gitflow)
            SKIP_GITFLOW=1
            shift
            ;;
        --master)
            MASTER_BRANCH="$2"
            shift 2
            ;;
        --develop)
            DEVELOP_BRANCH="$2"
            shift 2
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            print_usage
            exit 1
            ;;
    esac
done

echo ""
echo "🔧 GitFlow Worktree 初始化（裸仓库模式）"
echo "=========================================="
echo ""

# ============================================
# 1. 检查前置条件
# ============================================
echo -e "${BLUE}[1/6] 检查前置条件...${NC}"

# 检查 Git 版本
GIT_VERSION=$(git --version | grep -oE '[0-9]+\.[0-9]+' | head -1)
GIT_MAJOR=$(echo $GIT_VERSION | cut -d. -f1)
GIT_MINOR=$(echo $GIT_VERSION | cut -d. -f2)

if [ "$GIT_MAJOR" -lt 2 ] || ([ "$GIT_MAJOR" -eq 2 ] && [ "$GIT_MINOR" -lt 15 ]); then
    echo -e "${RED}❌ Git 版本过低（当前: $GIT_VERSION，要求: >= 2.15）${NC}"
    echo "   请升级 Git 以支持 worktree 功能"
    exit 1
fi
echo "   ✅ Git 版本: $GIT_VERSION"

# 检查 git-flow 工具
if [ $SKIP_GITFLOW -eq 0 ]; then
    if ! command -v git-flow &> /dev/null; then
        echo -e "${RED}❌ 未检测到 git-flow 工具${NC}"
        echo ""
        echo "请先安装 git-flow："
        echo "  macOS:   brew install git-flow"
        echo "  Ubuntu:  sudo apt-get install git-flow"
        echo "  Windows: 参考 https://github.com/nvie/gitflow/wiki/Installation"
        echo ""
        echo "或使用 --skip-gitflow 跳过 git flow 初始化"
        exit 1
    fi
    echo "   ✅ git-flow 已安装"
fi

# 检查是否在 Git 仓库中
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}❌ 当前目录不是 Git 仓库${NC}"
    echo "   请在已有的 Git 项目目录中运行此命令"
    exit 1
fi
echo "   ✅ Git 仓库检测通过"

echo -e "${GREEN}✅ 前置条件检查通过${NC}"

# ============================================
# 2. 获取仓库信息
# ============================================
echo ""
echo -e "${BLUE}[2/6] 获取仓库信息...${NC}"

# 获取仓库根目录
REPO_ROOT=$(git rev-parse --show-toplevel)
PROJECT_NAME=$(basename "$REPO_ROOT")
PARENT_DIR=$(dirname "$REPO_ROOT")
WORKSPACE_DIR="${PARENT_DIR}/${PROJECT_NAME}-workspace"

# 获取远程仓库地址
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

if [ -z "$REMOTE_URL" ]; then
    echo -e "${RED}❌ 未找到远程仓库地址（origin）${NC}"
    echo "   请先配置远程仓库："
    echo "   git remote add origin <repository-url>"
    exit 1
fi

echo "   项目名称: $PROJECT_NAME"
echo "   项目路径: $REPO_ROOT"
echo "   远程地址: $REMOTE_URL"
echo "   工作空间: $WORKSPACE_DIR"

echo -e "${GREEN}✅ 仓库信息获取完成${NC}"

# ============================================
# 3. 创建工作空间目录
# ============================================
echo ""
echo -e "${BLUE}[3/6] 创建工作空间目录...${NC}"

if [ -d "$WORKSPACE_DIR" ]; then
    if [ $FORCE -eq 0 ]; then
        echo "   工作空间目录已存在: $WORKSPACE_DIR"
        echo -e "${YELLOW}   ⚠️ 跳过创建，如需重新初始化请使用 --force 参数${NC}"
        
        # 检查是否已经初始化完成
        if [ -d "$WORKSPACE_DIR/.bare" ] && [ -f "$WORKSPACE_DIR/.git" ]; then
            echo ""
            echo -e "${GREEN}✅ 工作空间已初始化完成！${NC}"
            echo ""
            echo "📁 工作空间: $WORKSPACE_DIR"
            echo ""
            echo "🚀 可用命令："
            echo "   cd $WORKSPACE_DIR/master    # 进入 master 分支"
            echo "   cd $WORKSPACE_DIR/develop   # 进入 develop 分支"
            exit 0
        fi
    else
        echo -e "${YELLOW}   ⚠️ 强制模式：清理现有工作空间...${NC}"
        rm -rf "$WORKSPACE_DIR"
    fi
fi

mkdir -p "$WORKSPACE_DIR"
echo "   ✅ 工作空间目录已创建: $WORKSPACE_DIR"

echo -e "${GREEN}✅ 工作空间目录就绪${NC}"

# ============================================
# 4. 克隆裸仓库
# ============================================
echo ""
echo -e "${BLUE}[4/6] 克隆裸仓库...${NC}"

cd "$WORKSPACE_DIR"

echo "   执行: git clone --bare $REMOTE_URL .bare"
if ! git clone --bare "$REMOTE_URL" .bare; then
    echo -e "${RED}❌ 克隆裸仓库失败${NC}"
    echo ""
    echo "请检查："
    echo "  1. 网络连接是否正常"
    echo "  2. 远程仓库地址是否正确"
    echo "  3. Git 认证是否配置正确"
    exit 1
fi

echo "   ✅ 裸仓库克隆完成"

echo -e "${GREEN}✅ 裸仓库就绪${NC}"

# ============================================
# 5. 创建 .git 指向文件
# ============================================
echo ""
echo -e "${BLUE}[5/6] 配置 Git 指向...${NC}"

# 创建 .git 文件指向裸仓库
echo "gitdir: ./.bare" > .git
echo "   ✅ 创建 .git 文件指向 .bare"

# 配置裸仓库以支持 worktree
cd .bare
git config core.bare false
git config core.worktree "../"
cd ..

# 配置 fetch 规则，确保可以获取所有远程分支
cd .bare
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
cd ..

echo "   ✅ Git 配置完成"

echo -e "${GREEN}✅ Git 指向配置完成${NC}"

# ============================================
# 6. 创建 worktree 并初始化 GitFlow
# ============================================
echo ""
echo -e "${BLUE}[6/6] 创建 worktree 并初始化 GitFlow...${NC}"

# 创建 master worktree
echo "   创建 master worktree..."
if git show-ref --verify --quiet refs/remotes/origin/${MASTER_BRANCH} || git show-ref --verify --quiet refs/heads/${MASTER_BRANCH}; then
    git worktree add ${MASTER_BRANCH} ${MASTER_BRANCH} 2>/dev/null || \
    git worktree add ${MASTER_BRANCH} origin/${MASTER_BRANCH} 2>/dev/null || \
    git worktree add ${MASTER_BRANCH} -b ${MASTER_BRANCH} origin/${MASTER_BRANCH}
    echo "   ✅ master worktree 已创建"
else
    # 如果 master 分支不存在，从默认分支创建
    DEFAULT_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main")
    echo "   ⚠️ ${MASTER_BRANCH} 分支不存在，从 ${DEFAULT_BRANCH} 创建..."
    git worktree add ${MASTER_BRANCH} -b ${MASTER_BRANCH} origin/${DEFAULT_BRANCH}
    echo "   ✅ master worktree 已创建（基于 ${DEFAULT_BRANCH}）"
fi

# 初始化 git flow
if [ $SKIP_GITFLOW -eq 0 ]; then
    echo "   初始化 git flow..."
    cd ${MASTER_BRANCH}
    
    # 使用非交互式方式初始化 git flow
    git flow init -d -f 2>/dev/null || {
        echo -e "${YELLOW}   ⚠️ git flow init 需要手动确认，请执行以下命令：${NC}"
        echo "   cd $WORKSPACE_DIR/${MASTER_BRANCH} && git flow init"
    }
    
    cd ..
    echo "   ✅ git flow 已初始化"
fi

# 创建 develop worktree（如果 develop 分支已存在）
echo "   创建 develop worktree..."
if git show-ref --verify --quiet refs/remotes/origin/${DEVELOP_BRANCH} || git show-ref --verify --quiet refs/heads/${DEVELOP_BRANCH}; then
    git worktree add ${DEVELOP_BRANCH} ${DEVELOP_BRANCH} 2>/dev/null || \
    git worktree add ${DEVELOP_BRANCH} origin/${DEVELOP_BRANCH} 2>/dev/null || \
    git worktree add ${DEVELOP_BRANCH} -b ${DEVELOP_BRANCH} origin/${DEVELOP_BRANCH} 2>/dev/null || \
    git worktree add ${DEVELOP_BRANCH} -b ${DEVELOP_BRANCH} ${MASTER_BRANCH}
    echo "   ✅ develop worktree 已创建"
else
    # 从 master 创建 develop
    git worktree add ${DEVELOP_BRANCH} -b ${DEVELOP_BRANCH} ${MASTER_BRANCH}
    echo "   ✅ develop worktree 已创建（基于 ${MASTER_BRANCH}）"
fi

# 推送 develop 分支到远程（如果是新创建的）
cd ${DEVELOP_BRANCH}
git push -u origin ${DEVELOP_BRANCH} 2>/dev/null || true
cd ..

echo -e "${GREEN}✅ worktree 和 GitFlow 初始化完成${NC}"

# ============================================
# 显示完成信息
# ============================================
echo ""
echo "=========================================="
echo -e "${GREEN}🎉 GitFlow Worktree 初始化完成！${NC}"
echo "=========================================="
echo ""
echo "📁 工作空间目录结构："
echo ""
echo "   ${PROJECT_NAME}-workspace/"
echo "   ├── .bare/           # 裸仓库（Git 数据）"
echo "   ├── .git             # 指向 .bare"
echo "   ├── ${MASTER_BRANCH}/             # master 分支 worktree"
echo "   └── ${DEVELOP_BRANCH}/            # develop 分支 worktree"
echo ""
echo "📋 配置信息："
echo "   主分支: ${MASTER_BRANCH}"
echo "   开发分支: ${DEVELOP_BRANCH}"
echo "   远程仓库: ${REMOTE_URL}"
echo ""
echo "🚀 下一步操作："
echo ""
echo "   # 进入工作空间"
echo "   cd $WORKSPACE_DIR"
echo ""
echo "   # 开始新功能开发"
echo "   git worktree add feature/<name> -b feature/<name> ${DEVELOP_BRANCH}"
echo "   cd feature/<name>"
echo ""
echo "   # 创建发布分支"
echo "   git worktree add release/v1.0.0 -b release/v1.0.0 ${DEVELOP_BRANCH}"
echo ""
echo "   # 创建热修复分支"
echo "   git worktree add hotfix/<name> -b hotfix/<name> ${MASTER_BRANCH}"
echo ""
echo "📖 更多帮助："
echo "   /ease:gitflow help"
echo ""
