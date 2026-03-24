#!/bin/bash

# GitFlow Worktree 环境检查脚本（裸仓库模式）

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 最低 Git 版本要求
MIN_GIT_VERSION="2.15"

echo "🔍 GitFlow Worktree 环境检查"
echo "============================"
echo ""

# ============================================
# 1. 检查 Git 是否安装
# ============================================
check_git_installed() {
    echo -e "${BLUE}[1/5] 检查 Git 安装...${NC}"
    
    if ! command -v git &> /dev/null; then
        echo -e "${RED}❌ Git 未安装${NC}"
        echo ""
        echo "请先安装 Git："
        echo "  macOS:   brew install git"
        echo "  Ubuntu:  sudo apt-get install git"
        echo "  Windows: https://git-scm.com/download/win"
        return 1
    fi
    
    echo -e "${GREEN}✅ Git 已安装${NC}"
    return 0
}

# ============================================
# 2. 检查 Git 版本
# ============================================
check_git_version() {
    echo -e "${BLUE}[2/5] 检查 Git 版本...${NC}"
    
    local git_version=$(git --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    local major=$(echo $git_version | cut -d. -f1)
    local minor=$(echo $git_version | cut -d. -f2)
    
    local min_major=$(echo $MIN_GIT_VERSION | cut -d. -f1)
    local min_minor=$(echo $MIN_GIT_VERSION | cut -d. -f2)
    
    echo "   当前版本: $git_version"
    echo "   最低要求: $MIN_GIT_VERSION"
    
    if [ "$major" -lt "$min_major" ] || ([ "$major" -eq "$min_major" ] && [ "$minor" -lt "$min_minor" ]); then
        echo -e "${RED}❌ Git 版本过低，不支持 worktree${NC}"
        echo ""
        echo "请升级 Git 到 $MIN_GIT_VERSION 或更高版本："
        echo "  macOS:   brew upgrade git"
        echo "  Ubuntu:  sudo apt-get update && sudo apt-get upgrade git"
        return 1
    fi
    
    echo -e "${GREEN}✅ Git 版本满足要求${NC}"
    return 0
}

# ============================================
# 3. 检查是否在 Git 仓库中
# ============================================
check_git_repo() {
    echo -e "${BLUE}[3/5] 检查 Git 仓库...${NC}"
    
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        echo -e "${RED}❌ 当前目录不是 Git 仓库${NC}"
        echo ""
        echo "请在 Git 仓库目录中运行此命令"
        return 1
    fi
    
    local repo_root=$(git rev-parse --show-toplevel)
    echo "   仓库路径: $repo_root"
    echo -e "${GREEN}✅ Git 仓库存在${NC}"
    return 0
}

# ============================================
# 4. 检查远程仓库
# ============================================
check_remote() {
    echo -e "${BLUE}[4/5] 检查远程仓库...${NC}"
    
    local remote_url=$(git remote get-url origin 2>/dev/null || echo "")
    
    if [ -z "$remote_url" ]; then
        echo -e "${RED}❌ 未配置远程仓库（origin）${NC}"
        echo ""
        echo "请先配置远程仓库："
        echo "   git remote add origin <repository-url>"
        return 1
    fi
    
    echo "   远程仓库: $remote_url"
    echo -e "${GREEN}✅ 远程仓库已配置${NC}"
    return 0
}

# ============================================
# 5. 检查 git-flow 工具
# ============================================
check_gitflow_tool() {
    echo -e "${BLUE}[5/5] 检查 git-flow 工具...${NC}"
    
    if command -v git-flow &> /dev/null; then
        local version=$(git flow version 2>/dev/null || echo "unknown")
        echo -e "${GREEN}✅ git-flow 已安装: $version${NC}"
        return 0
    else
        echo -e "${RED}❌ git-flow 未安装${NC}"
        echo ""
        echo "请安装 git-flow："
        echo "  macOS:   brew install git-flow"
        echo "  Ubuntu:  sudo apt-get install git-flow"
        echo "  Windows: 参考 https://github.com/nvie/gitflow/wiki/Installation"
        return 1
    fi
}

# ============================================
# 显示检查结果摘要
# ============================================
show_summary() {
    local status=$1
    
    echo ""
    echo "============================"
    echo "📊 检查结果摘要"
    echo "============================"
    echo ""
    
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✅ 所有检查通过！环境已就绪${NC}"
        echo ""
        echo "🚀 现在可以运行初始化命令："
        echo "   /ease:gitflow init"
        echo ""
        echo "初始化后将创建以下目录结构："
        echo ""
        echo "   <project>-workspace/"
        echo "   ├── .bare/           # 裸仓库"
        echo "   ├── .git             # 指向 .bare"
        echo "   ├── master/          # master 分支"
        echo "   └── develop/         # develop 分支"
    else
        echo -e "${RED}❌ 环境检查失败${NC}"
        echo ""
        echo "请解决上述问题后重试"
    fi
}

# ============================================
# 主程序
# ============================================
main() {
    local final_status=0
    
    check_git_installed || final_status=1
    [ $final_status -eq 0 ] && { check_git_version || final_status=1; }
    [ $final_status -eq 0 ] && { check_git_repo || final_status=1; }
    [ $final_status -eq 0 ] && { check_remote || final_status=1; }
    [ $final_status -eq 0 ] && { check_gitflow_tool || final_status=1; }
    
    show_summary $final_status
    
    exit $final_status
}

main "$@"
