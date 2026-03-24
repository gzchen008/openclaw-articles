#!/bin/bash

# GitFlow Worktree 管理脚本（裸仓库模式）
# 结合 GitFlow 分支模型和 Git Worktree 的自动化工具
#
# 目录结构：
# my-app-workspace/
#   ├── .bare/        # 裸仓库
#   ├── .git          # 指向 .bare 的文件
#   ├── master/       # master 分支 worktree
#   ├── develop/      # develop 分支 worktree
#   ├── feature/      # feature 分支目录
#   ├── release/      # release 分支目录
#   └── hotfix/       # hotfix 分支目录

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置变量
MASTER_BRANCH="master"
DEVELOP_BRANCH="develop"
FEATURE_PREFIX="feature/"
RELEASE_PREFIX="release/"
HOTFIX_PREFIX="hotfix/"

# 帮助信息
show_help() {
    echo "GitFlow Worktree 管理工具（裸仓库模式）"
    echo ""
    echo "用法: $0 <command> [subcommand] [arguments]"
    echo ""
    echo "Commands:"
    echo "  init                    初始化 GitFlow Worktree 工作空间"
    echo ""
    echo "  feature start <name>    创建新功能分支并设置 worktree"
    echo "  feature finish <name>   完成功能，合并到 develop"
    echo "  feature list            列出所有 feature 分支"
    echo "  feature sync <name>     同步 develop 到 feature 分支"
    echo ""
    echo "  release start <version> 创建发布分支并设置 worktree"
    echo "  release finish <version> 完成发布，合并到 master 和 develop"
    echo "  release list            列出所有 release 分支"
    echo ""
    echo "  hotfix start <name>     从 master 创建热修复分支"
    echo "  hotfix finish <name>    完成热修复，合并到 master 和 develop"
    echo "  hotfix list             列出所有 hotfix 分支"
    echo ""
    echo "  status                  显示当前状态"
    echo "  worktree list           列出所有 worktree"
    echo "  worktree clean          清理已合并分支的 worktree"
    echo ""
    echo "示例:"
    echo "  $0 feature start user-auth"
    echo "  $0 release start v1.2.0"
    echo "  $0 status"
}

# 检查是否在工作空间目录
check_workspace() {
    if [ ! -d ".bare" ] || [ ! -f ".git" ]; then
        echo -e "${RED}❌ 错误：当前目录不是 GitFlow Worktree 工作空间${NC}"
        echo ""
        echo "工作空间目录应包含："
        echo "  - .bare/ 目录（裸仓库）"
        echo "  - .git 文件（指向 .bare）"
        echo ""
        echo "请先运行 '/ease:gitflow init' 在原项目目录中初始化工作空间"
        exit 1
    fi
}

# 检查工作区是否干净
check_clean_working_tree() {
    local path=$1
    if [ -d "$path" ]; then
        cd "$path"
        if [ -n "$(git status --porcelain)" ]; then
            echo -e "${YELLOW}⚠️ 警告：${path} 有未提交的更改${NC}"
            git status --short
            read -p "是否继续？(y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                exit 1
            fi
        fi
        cd - > /dev/null
    fi
}

# Feature 命令
feature_start() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}❌ 错误：请提供 feature 名称${NC}"
        echo "用法: $0 feature start <name>"
        exit 1
    fi

    local branch="${FEATURE_PREFIX}${name}"
    local worktree_path="feature/${name}"

    echo -e "${BLUE}📥 更新 ${DEVELOP_BRANCH} 分支...${NC}"
    cd ${DEVELOP_BRANCH}
    git fetch origin
    git pull origin ${DEVELOP_BRANCH}
    cd ..

    if git show-ref --verify --quiet refs/heads/${branch}; then
        echo -e "${YELLOW}⚠️ 分支 ${branch} 已存在${NC}"
        if [ -d "${worktree_path}" ]; then
            echo -e "${GREEN}✅ Worktree 已存在：${worktree_path}${NC}"
            exit 0
        else
            echo -e "${BLUE}🔧 创建 worktree...${NC}"
            mkdir -p feature
            git worktree add ${worktree_path} ${branch}
            echo -e "${GREEN}✅ Worktree 已创建${NC}"
            exit 0
        fi
    fi

    echo -e "${BLUE}🌿 创建分支 ${branch}...${NC}"
    mkdir -p feature
    git worktree add ${worktree_path} -b ${branch} ${DEVELOP_BRANCH}

    echo ""
    echo -e "${GREEN}✅ Feature 分支创建成功！${NC}"
    echo ""
    echo "📋 信息："
    echo "   分支名称：${branch}"
    echo "   工作目录：$(pwd)/${worktree_path}"
    echo ""
    echo "🚀 下一步："
    echo "   cd ${worktree_path}"
    echo "   开始你的开发工作..."
}

feature_finish() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}❌ 错误：请提供 feature 名称${NC}"
        exit 1
    fi

    local branch="${FEATURE_PREFIX}${name}"
    local worktree_path="feature/${name}"

    if ! git show-ref --verify --quiet refs/heads/${branch}; then
        echo -e "${RED}❌ 错误：分支 ${branch} 不存在${NC}"
        exit 1
    fi

    # 检查 worktree 中是否有未提交的更改
    check_clean_working_tree "${worktree_path}"

    echo -e "${BLUE}📥 进入 ${DEVELOP_BRANCH} 目录...${NC}"
    cd ${DEVELOP_BRANCH}
    git fetch origin
    git pull origin ${DEVELOP_BRANCH}

    echo -e "${BLUE}🔀 合并 ${branch}...${NC}"
    git merge --no-ff ${branch} -m "Merge branch '${branch}' into ${DEVELOP_BRANCH}"

    echo -e "${BLUE}📤 推送到远程...${NC}"
    git push origin ${DEVELOP_BRANCH}

    cd ..

    # 删除 worktree
    if [ -d "${worktree_path}" ]; then
        echo -e "${BLUE}🧹 清理 worktree...${NC}"
        git worktree remove ${worktree_path}
    fi

    echo -e "${BLUE}🗑️ 删除分支...${NC}"
    git branch -d ${branch}
    git push origin --delete ${branch} 2>/dev/null || true

    echo ""
    echo -e "${GREEN}✅ Feature 完成！${NC}"
    echo ""
    echo "📋 已完成操作："
    echo "   ✓ 合并 ${branch} 到 ${DEVELOP_BRANCH}"
    echo "   ✓ 清理 worktree"
    echo "   ✓ 删除分支 ${branch}"
}

feature_list() {
    echo "📋 Feature 分支列表"
    echo "===================="
    echo ""

    echo "🏠 本地分支（Worktree）："
    if [ -d "feature" ]; then
        local found=0
        for dir in feature/*/; do
            if [ -d "$dir" ]; then
                found=1
                local name=$(basename "$dir")
                echo "   feature/${name} → ${dir}"
            fi
        done
        if [ $found -eq 0 ]; then
            echo "   (无)"
        fi
    else
        echo "   (无)"
    fi

    echo ""
    echo "☁️ 远程分支："
    git branch -r --list "origin/${FEATURE_PREFIX}*" 2>/dev/null | while read branch; do
        branch_name=$(echo $branch | sed 's/^[ *]*//' | sed 's/origin\///')
        echo "   ${branch_name}"
    done || echo "   (无)"
}

feature_sync() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}❌ 错误：请提供 feature 名称${NC}"
        exit 1
    fi

    local worktree_path="feature/${name}"

    if [ ! -d "${worktree_path}" ]; then
        echo -e "${RED}❌ 错误：Worktree 不存在：${worktree_path}${NC}"
        exit 1
    fi

    echo -e "${BLUE}📥 同步 ${DEVELOP_BRANCH} 到 feature/${name}...${NC}"
    cd ${worktree_path}
    git fetch origin
    git rebase origin/${DEVELOP_BRANCH}
    cd ../..

    echo -e "${GREEN}✅ 同步完成${NC}"
}

# Release 命令
release_start() {
    local version=$1
    if [ -z "$version" ]; then
        echo -e "${RED}❌ 错误：请提供版本号${NC}"
        echo "用法: $0 release start <version>"
        exit 1
    fi

    local branch="${RELEASE_PREFIX}${version}"
    local worktree_path="release/${version}"

    echo -e "${BLUE}📥 更新 ${DEVELOP_BRANCH} 分支...${NC}"
    cd ${DEVELOP_BRANCH}
    git fetch origin
    git pull origin ${DEVELOP_BRANCH}
    cd ..

    if git show-ref --verify --quiet refs/heads/${branch}; then
        echo -e "${RED}❌ 错误：分支 ${branch} 已存在${NC}"
        exit 1
    fi

    echo -e "${BLUE}🌿 创建分支 ${branch}...${NC}"
    mkdir -p release
    git worktree add ${worktree_path} -b ${branch} ${DEVELOP_BRANCH}

    # 更新版本号
    cd ${worktree_path}
    local clean_version=${version#v}
    if [ -f "package.json" ]; then
        echo -e "${BLUE}📝 更新 package.json 版本号...${NC}"
        sed -i.bak "s/\"version\": \"[^\"]*\"/\"version\": \"${clean_version}\"/" package.json
        rm -f package.json.bak
        git add package.json
        git commit -m "chore: bump version to ${version}"
    fi
    cd ../..

    echo ""
    echo -e "${GREEN}✅ Release 分支创建成功！${NC}"
    echo ""
    echo "📋 信息："
    echo "   分支名称：${branch}"
    echo "   工作目录：$(pwd)/${worktree_path}"
    echo "   版本号：${version}"
    echo ""
    echo "🚀 下一步："
    echo "   1. cd ${worktree_path}"
    echo "   2. 进行最终测试和 Bug 修复"
    echo "   3. 完成后执行：$0 release finish ${version}"
}

release_finish() {
    local version=$1
    if [ -z "$version" ]; then
        echo -e "${RED}❌ 错误：请提供版本号${NC}"
        exit 1
    fi

    local branch="${RELEASE_PREFIX}${version}"
    local worktree_path="release/${version}"
    local tag_name=${version}

    if ! git show-ref --verify --quiet refs/heads/${branch}; then
        echo -e "${RED}❌ 错误：分支 ${branch} 不存在${NC}"
        exit 1
    fi

    # 检查 worktree 中是否有未提交的更改
    check_clean_working_tree "${worktree_path}"

    # 合并到 master
    echo -e "${BLUE}📥 合并到 ${MASTER_BRANCH}...${NC}"
    cd ${MASTER_BRANCH}
    git fetch origin
    git pull origin ${MASTER_BRANCH}
    git merge --no-ff ${branch} -m "Merge branch '${branch}' into ${MASTER_BRANCH}"

    # 创建 Tag
    echo -e "${BLUE}🏷️ 创建 Tag ${tag_name}...${NC}"
    git tag -a ${tag_name} -m "Release ${tag_name}"

    git push origin ${MASTER_BRANCH}
    git push origin ${tag_name}

    cd ..

    # 合并到 develop
    echo -e "${BLUE}📥 合并到 ${DEVELOP_BRANCH}...${NC}"
    cd ${DEVELOP_BRANCH}
    git fetch origin
    git pull origin ${DEVELOP_BRANCH}
    git merge --no-ff ${branch} -m "Merge branch '${branch}' into ${DEVELOP_BRANCH}"
    git push origin ${DEVELOP_BRANCH}

    cd ..

    # 清理
    if [ -d "${worktree_path}" ]; then
        echo -e "${BLUE}🧹 清理 worktree...${NC}"
        git worktree remove ${worktree_path}
    fi

    echo -e "${BLUE}🗑️ 删除分支...${NC}"
    git branch -d ${branch}
    git push origin --delete ${branch} 2>/dev/null || true

    echo ""
    echo -e "${GREEN}🎉 Release ${version} 发布成功！${NC}"
    echo ""
    echo "📋 已完成操作："
    echo "   ✓ 合并到 ${MASTER_BRANCH}"
    echo "   ✓ 创建 Tag ${tag_name}"
    echo "   ✓ 合并到 ${DEVELOP_BRANCH}"
    echo "   ✓ 推送到远程"
    echo "   ✓ 清理分支和 worktree"
}

release_list() {
    echo "📋 Release 分支列表"
    echo "===================="
    echo ""

    echo "🏠 本地分支（Worktree）："
    if [ -d "release" ]; then
        local found=0
        for dir in release/*/; do
            if [ -d "$dir" ]; then
                found=1
                local name=$(basename "$dir")
                echo "   release/${name} → ${dir}"
            fi
        done
        if [ $found -eq 0 ]; then
            echo "   (无)"
        fi
    else
        echo "   (无)"
    fi

    echo ""
    echo "🏷️ 最近的 Tags："
    git tag --sort=-version:refname 2>/dev/null | head -5 | while read tag; do
        date=$(git log -1 --format="%ci" $tag 2>/dev/null | cut -d' ' -f1)
        echo "   ${tag} (${date})"
    done || echo "   (无)"
}

# Hotfix 命令
hotfix_start() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}❌ 错误：请提供 hotfix 名称${NC}"
        exit 1
    fi

    local branch="${HOTFIX_PREFIX}${name}"
    local worktree_path="hotfix/${name}"

    echo -e "${BLUE}📥 更新 ${MASTER_BRANCH} 分支...${NC}"
    cd ${MASTER_BRANCH}
    git fetch origin
    git pull origin ${MASTER_BRANCH}
    cd ..

    if git show-ref --verify --quiet refs/heads/${branch}; then
        echo -e "${RED}❌ 错误：分支 ${branch} 已存在${NC}"
        exit 1
    fi

    local current_version=$(cd ${MASTER_BRANCH} && git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    echo -e "${BLUE}📌 当前版本：${current_version}${NC}"

    echo -e "${BLUE}🌿 创建分支 ${branch}...${NC}"
    mkdir -p hotfix
    git worktree add ${worktree_path} -b ${branch} ${MASTER_BRANCH}

    echo ""
    echo -e "${GREEN}🚨 Hotfix 分支创建成功！${NC}"
    echo ""
    echo "📋 信息："
    echo "   分支名称：${branch}"
    echo "   工作目录：$(pwd)/${worktree_path}"
    echo "   基于版本：${current_version}"
    echo ""
    echo "⚠️ 注意：仅修复紧急问题，不添加新功能"
    echo ""
    echo "🚀 下一步："
    echo "   cd ${worktree_path}"
    echo "   修复 Bug..."
}

hotfix_finish() {
    local name=$1
    if [ -z "$name" ]; then
        echo -e "${RED}❌ 错误：请提供 hotfix 名称${NC}"
        exit 1
    fi

    local branch="${HOTFIX_PREFIX}${name}"
    local worktree_path="hotfix/${name}"

    if ! git show-ref --verify --quiet refs/heads/${branch}; then
        echo -e "${RED}❌ 错误：分支 ${branch} 不存在${NC}"
        exit 1
    fi

    # 检查 worktree 中是否有未提交的更改
    check_clean_working_tree "${worktree_path}"

    # 计算新版本号
    local current_version=$(cd ${MASTER_BRANCH} && git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    local version_parts=(${current_version//[v.]/ })
    local major=${version_parts[0]:-0}
    local minor=${version_parts[1]:-0}
    local patch=${version_parts[2]:-0}
    local new_version="v${major}.${minor}.$((patch + 1))"

    echo -e "${BLUE}📌 新版本号：${new_version}${NC}"

    # 更新版本号
    if [ -d "${worktree_path}" ]; then
        cd ${worktree_path}
        local clean_version=${new_version#v}
        if [ -f "package.json" ]; then
            sed -i.bak "s/\"version\": \"[^\"]*\"/\"version\": \"${clean_version}\"/" package.json
            rm -f package.json.bak
            git add package.json
            git commit -m "chore: bump version to ${new_version}"
        fi
        cd ../..
    fi

    # 合并到 master
    echo -e "${BLUE}📥 合并到 ${MASTER_BRANCH}...${NC}"
    cd ${MASTER_BRANCH}
    git fetch origin
    git pull origin ${MASTER_BRANCH}
    git merge --no-ff ${branch} -m "Merge hotfix '${branch}' into ${MASTER_BRANCH}"

    # 创建 Tag
    echo -e "${BLUE}🏷️ 创建 Tag ${new_version}...${NC}"
    git tag -a ${new_version} -m "Hotfix ${new_version}: ${name}"

    git push origin ${MASTER_BRANCH}
    git push origin ${new_version}

    cd ..

    # 合并到 develop
    echo -e "${BLUE}📥 合并到 ${DEVELOP_BRANCH}...${NC}"
    cd ${DEVELOP_BRANCH}
    git fetch origin
    git pull origin ${DEVELOP_BRANCH}
    git merge --no-ff ${branch} -m "Merge hotfix '${branch}' into ${DEVELOP_BRANCH}"
    git push origin ${DEVELOP_BRANCH}

    cd ..

    # 清理
    if [ -d "${worktree_path}" ]; then
        echo -e "${BLUE}🧹 清理 worktree...${NC}"
        git worktree remove ${worktree_path}
    fi

    echo -e "${BLUE}🗑️ 删除分支...${NC}"
    git branch -d ${branch}
    git push origin --delete ${branch} 2>/dev/null || true

    echo ""
    echo -e "${GREEN}🎉 Hotfix ${new_version} 完成！${NC}"
    echo ""
    echo "📋 已完成操作："
    echo "   ✓ 合并到 ${MASTER_BRANCH}"
    echo "   ✓ 创建 Tag ${new_version}"
    echo "   ✓ 合并到 ${DEVELOP_BRANCH}"
    echo "   ✓ 推送到远程"
    echo "   ✓ 清理分支和 worktree"
}

hotfix_list() {
    echo "📋 Hotfix 分支列表"
    echo "===================="
    echo ""

    echo "🏠 本地分支（Worktree）："
    if [ -d "hotfix" ]; then
        local found=0
        for dir in hotfix/*/; do
            if [ -d "$dir" ]; then
                found=1
                local name=$(basename "$dir")
                echo "   hotfix/${name} → ${dir}"
            fi
        done
        if [ $found -eq 0 ]; then
            echo "   (无)"
        fi
    else
        echo "   (无)"
    fi
}

# 状态命令
show_status() {
    echo "📊 GitFlow Worktree 状态"
    echo "========================"
    echo ""

    echo -e "${BLUE}📁 工作空间目录：${NC}"
    echo "   $(pwd)"
    echo ""

    echo -e "${BLUE}🌿 主要分支：${NC}"
    if [ -d "${MASTER_BRANCH}" ]; then
        echo "   ✅ ${MASTER_BRANCH}/ → $(cd ${MASTER_BRANCH} && git log -1 --format='%h %s' 2>/dev/null)"
    else
        echo "   ❌ ${MASTER_BRANCH}/ (不存在)"
    fi
    if [ -d "${DEVELOP_BRANCH}" ]; then
        echo "   ✅ ${DEVELOP_BRANCH}/ → $(cd ${DEVELOP_BRANCH} && git log -1 --format='%h %s' 2>/dev/null)"
    else
        echo "   ❌ ${DEVELOP_BRANCH}/ (不存在)"
    fi
    echo ""

    echo -e "${BLUE}🔀 Feature 分支：${NC}"
    if [ -d "feature" ]; then
        for dir in feature/*/; do
            if [ -d "$dir" ]; then
                local name=$(basename "$dir")
                echo "   feature/${name}/"
            fi
        done
    else
        echo "   (无)"
    fi
    echo ""

    echo -e "${BLUE}📦 Release 分支：${NC}"
    if [ -d "release" ]; then
        for dir in release/*/; do
            if [ -d "$dir" ]; then
                local name=$(basename "$dir")
                echo "   release/${name}/"
            fi
        done
    else
        echo "   (无)"
    fi
    echo ""

    echo -e "${BLUE}🔧 Hotfix 分支：${NC}"
    if [ -d "hotfix" ]; then
        for dir in hotfix/*/; do
            if [ -d "$dir" ]; then
                local name=$(basename "$dir")
                echo "   hotfix/${name}/"
            fi
        done
    else
        echo "   (无)"
    fi
    echo ""

    echo -e "${BLUE}🏷️ 最近的 Tags：${NC}"
    git tag --sort=-version:refname 2>/dev/null | head -5 || echo "   (无)"
}

# Worktree 命令
worktree_list() {
    echo "📁 Worktree 列表"
    echo "================"
    echo ""
    git worktree list
}

worktree_clean() {
    echo -e "${BLUE}🧹 清理无效的 Worktree...${NC}"
    echo ""

    # 清理孤立的 worktree
    git worktree prune

    echo -e "${GREEN}✅ 清理完成${NC}"
}

# 主程序
main() {
    if [ $# -eq 0 ]; then
        show_help
        exit 0
    fi

    local command=$1
    local subcommand=$2
    shift 2 2>/dev/null || true

    # init 命令不需要检查工作空间
    if [ "$command" != "init" ] && [ "$command" != "help" ] && [ "$command" != "--help" ] && [ "$command" != "-h" ]; then
        check_workspace
    fi

    case $command in
        feature)
            case $subcommand in
                start)  feature_start "$@" ;;
                finish) feature_finish "$@" ;;
                list)   feature_list ;;
                sync)   feature_sync "$@" ;;
                *)      echo "未知的 feature 子命令: $subcommand"; show_help; exit 1 ;;
            esac
            ;;
        release)
            case $subcommand in
                start)  release_start "$@" ;;
                finish) release_finish "$@" ;;
                list)   release_list ;;
                *)      echo "未知的 release 子命令: $subcommand"; show_help; exit 1 ;;
            esac
            ;;
        hotfix)
            case $subcommand in
                start)  hotfix_start "$@" ;;
                finish) hotfix_finish "$@" ;;
                list)   hotfix_list ;;
                *)      echo "未知的 hotfix 子命令: $subcommand"; show_help; exit 1 ;;
            esac
            ;;
        status)
            show_status
            ;;
        init)
            echo "请使用 init-project.sh 脚本初始化工作空间"
            echo "或在原项目目录中运行 /ease:gitflow init"
            ;;
        worktree)
            case $subcommand in
                list)  worktree_list ;;
                clean) worktree_clean ;;
                *)     echo "未知的 worktree 子命令: $subcommand"; show_help; exit 1 ;;
            esac
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo "未知的命令: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
