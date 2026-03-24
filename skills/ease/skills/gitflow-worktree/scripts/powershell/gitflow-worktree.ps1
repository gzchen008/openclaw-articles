# GitFlow Worktree 管理脚本（裸仓库模式）- PowerShell 版本
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

param(
    [Parameter(Position=0)]
    [string]$Command,
    [Parameter(Position=1)]
    [string]$SubCommand,
    [Parameter(Position=2)]
    [string]$Arg1,
    [Parameter(Position=3)]
    [string]$Arg2
)

# 配置变量
$MASTER_BRANCH = "master"
$DEVELOP_BRANCH = "develop"
$FEATURE_PREFIX = "feature/"
$RELEASE_PREFIX = "release/"
$HOTFIX_PREFIX = "hotfix/"

function Show-Help {
    Write-Host "GitFlow Worktree 管理工具（裸仓库模式）" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "用法: .\gitflow-worktree.ps1 <command> [subcommand] [arguments]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  init                    初始化 GitFlow Worktree 工作空间"
    Write-Host ""
    Write-Host "  feature start <name>    创建新功能分支并设置 worktree"
    Write-Host "  feature finish <name>   完成功能，合并到 develop"
    Write-Host "  feature list            列出所有 feature 分支"
    Write-Host "  feature sync <name>     同步 develop 到 feature 分支"
    Write-Host ""
    Write-Host "  release start <version> 创建发布分支并设置 worktree"
    Write-Host "  release finish <version> 完成发布，合并到 master 和 develop"
    Write-Host "  release list            列出所有 release 分支"
    Write-Host ""
    Write-Host "  hotfix start <name>     从 master 创建热修复分支"
    Write-Host "  hotfix finish <name>    完成热修复，合并到 master 和 develop"
    Write-Host "  hotfix list             列出所有 hotfix 分支"
    Write-Host ""
    Write-Host "  status                  显示当前状态"
    Write-Host "  worktree list           列出所有 worktree"
    Write-Host "  worktree clean          清理已合并分支的 worktree"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\gitflow-worktree.ps1 feature start user-auth"
    Write-Host "  .\gitflow-worktree.ps1 release start v1.2.0"
    Write-Host "  .\gitflow-worktree.ps1 status"
}

function Check-Workspace {
    $bareExists = Test-Path ".bare"
    $gitFileExists = Test-Path ".git" -PathType Leaf
    
    if (-not $bareExists -or -not $gitFileExists) {
        Write-Host "❌ 错误：当前目录不是 GitFlow Worktree 工作空间" -ForegroundColor Red
        Write-Host ""
        Write-Host "工作空间目录应包含："
        Write-Host "  - .bare\ 目录（裸仓库）"
        Write-Host "  - .git 文件（指向 .bare）"
        Write-Host ""
        Write-Host "请先运行 '/ease:gitflow init' 在原项目目录中初始化工作空间"
        exit 1
    }
}

function Feature-Start {
    param([string]$Name)
    
    if (-not $Name) {
        Write-Host "❌ 错误：请提供 feature 名称" -ForegroundColor Red
        Write-Host "用法: .\gitflow-worktree.ps1 feature start <name>"
        exit 1
    }
    
    $branch = "${FEATURE_PREFIX}${Name}"
    $worktreePath = "feature\${Name}"
    
    Write-Host "📥 更新 ${DEVELOP_BRANCH} 分支..." -ForegroundColor Blue
    Push-Location $DEVELOP_BRANCH
    git fetch origin
    git pull origin $DEVELOP_BRANCH
    Pop-Location
    
    $branchExists = git show-ref --verify --quiet "refs/heads/${branch}" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "⚠️ 分支 ${branch} 已存在" -ForegroundColor Yellow
        if (Test-Path $worktreePath) {
            Write-Host "✅ Worktree 已存在：${worktreePath}" -ForegroundColor Green
            exit 0
        } else {
            Write-Host "🔧 创建 worktree..." -ForegroundColor Blue
            New-Item -ItemType Directory -Force -Path "feature" | Out-Null
            git worktree add $worktreePath $branch
            Write-Host "✅ Worktree 已创建" -ForegroundColor Green
            exit 0
        }
    }
    
    Write-Host "🌿 创建分支 ${branch}..." -ForegroundColor Blue
    New-Item -ItemType Directory -Force -Path "feature" | Out-Null
    git worktree add $worktreePath -b $branch $DEVELOP_BRANCH
    
    Write-Host ""
    Write-Host "✅ Feature 分支创建成功！" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 信息："
    Write-Host "   分支名称：${branch}"
    Write-Host "   工作目录：$(Get-Location)\${worktreePath}"
    Write-Host ""
    Write-Host "🚀 下一步："
    Write-Host "   cd ${worktreePath}"
    Write-Host "   开始你的开发工作..."
}

function Feature-Finish {
    param([string]$Name)
    
    if (-not $Name) {
        Write-Host "❌ 错误：请提供 feature 名称" -ForegroundColor Red
        exit 1
    }
    
    $branch = "${FEATURE_PREFIX}${Name}"
    $worktreePath = "feature\${Name}"
    
    $branchExists = git show-ref --verify --quiet "refs/heads/${branch}" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 错误：分支 ${branch} 不存在" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "📥 进入 ${DEVELOP_BRANCH} 目录..." -ForegroundColor Blue
    Push-Location $DEVELOP_BRANCH
    git fetch origin
    git pull origin $DEVELOP_BRANCH
    
    Write-Host "🔀 合并 ${branch}..." -ForegroundColor Blue
    git merge --no-ff $branch -m "Merge branch '${branch}' into ${DEVELOP_BRANCH}"
    
    Write-Host "📤 推送到远程..." -ForegroundColor Blue
    git push origin $DEVELOP_BRANCH
    
    Pop-Location
    
    if (Test-Path $worktreePath) {
        Write-Host "🧹 清理 worktree..." -ForegroundColor Blue
        git worktree remove $worktreePath
    }
    
    Write-Host "🗑️ 删除分支..." -ForegroundColor Blue
    git branch -d $branch
    git push origin --delete $branch 2>$null
    
    Write-Host ""
    Write-Host "✅ Feature 完成！" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 已完成操作："
    Write-Host "   ✓ 合并 ${branch} 到 ${DEVELOP_BRANCH}"
    Write-Host "   ✓ 清理 worktree"
    Write-Host "   ✓ 删除分支 ${branch}"
}

function Feature-List {
    Write-Host "📋 Feature 分支列表"
    Write-Host "===================="
    Write-Host ""
    
    Write-Host "🏠 本地分支（Worktree）："
    if (Test-Path "feature") {
        $dirs = Get-ChildItem -Path "feature" -Directory
        if ($dirs) {
            foreach ($dir in $dirs) {
                Write-Host "   feature\$($dir.Name) → feature\$($dir.Name)\"
            }
        } else {
            Write-Host "   (无)"
        }
    } else {
        Write-Host "   (无)"
    }
}

function Show-Status {
    Write-Host "📊 GitFlow Worktree 状态" -ForegroundColor Cyan
    Write-Host "========================"
    Write-Host ""
    
    Write-Host "📁 工作空间目录：" -ForegroundColor Blue
    Write-Host "   $(Get-Location)"
    Write-Host ""
    
    Write-Host "🌿 主要分支：" -ForegroundColor Blue
    if (Test-Path $MASTER_BRANCH) {
        Push-Location $MASTER_BRANCH
        $lastCommit = git log -1 --format='%h %s' 2>$null
        Pop-Location
        Write-Host "   ✅ ${MASTER_BRANCH}\ → $lastCommit"
    } else {
        Write-Host "   ❌ ${MASTER_BRANCH}\ (不存在)"
    }
    
    if (Test-Path $DEVELOP_BRANCH) {
        Push-Location $DEVELOP_BRANCH
        $lastCommit = git log -1 --format='%h %s' 2>$null
        Pop-Location
        Write-Host "   ✅ ${DEVELOP_BRANCH}\ → $lastCommit"
    } else {
        Write-Host "   ❌ ${DEVELOP_BRANCH}\ (不存在)"
    }
    Write-Host ""
    
    Write-Host "🔀 Feature 分支：" -ForegroundColor Blue
    if (Test-Path "feature") {
        Get-ChildItem -Path "feature" -Directory | ForEach-Object {
            Write-Host "   feature\$($_.Name)\"
        }
    } else {
        Write-Host "   (无)"
    }
    Write-Host ""
    
    Write-Host "📦 Release 分支：" -ForegroundColor Blue
    if (Test-Path "release") {
        Get-ChildItem -Path "release" -Directory | ForEach-Object {
            Write-Host "   release\$($_.Name)\"
        }
    } else {
        Write-Host "   (无)"
    }
    Write-Host ""
    
    Write-Host "🔧 Hotfix 分支：" -ForegroundColor Blue
    if (Test-Path "hotfix") {
        Get-ChildItem -Path "hotfix" -Directory | ForEach-Object {
            Write-Host "   hotfix\$($_.Name)\"
        }
    } else {
        Write-Host "   (无)"
    }
    Write-Host ""
    
    Write-Host "🏷️ 最近的 Tags：" -ForegroundColor Blue
    $tags = git tag --sort=-version:refname 2>$null | Select-Object -First 5
    if ($tags) {
        $tags | ForEach-Object { Write-Host "   $_" }
    } else {
        Write-Host "   (无)"
    }
}

function Worktree-List {
    Write-Host "📁 Worktree 列表"
    Write-Host "================"
    Write-Host ""
    git worktree list
}

function Worktree-Clean {
    Write-Host "🧹 清理无效的 Worktree..." -ForegroundColor Blue
    Write-Host ""
    git worktree prune
    Write-Host "✅ 清理完成" -ForegroundColor Green
}

# 主程序
if (-not $Command) {
    Show-Help
    exit 0
}

# 检查工作空间（除了 init 和 help 命令）
if ($Command -ne "init" -and $Command -ne "help" -and $Command -ne "--help" -and $Command -ne "-h") {
    Check-Workspace
}

switch ($Command) {
    "feature" {
        switch ($SubCommand) {
            "start" { Feature-Start -Name $Arg1 }
            "finish" { Feature-Finish -Name $Arg1 }
            "list" { Feature-List }
            default { 
                Write-Host "未知的 feature 子命令: $SubCommand"
                Show-Help
                exit 1
            }
        }
    }
    "status" { Show-Status }
    "worktree" {
        switch ($SubCommand) {
            "list" { Worktree-List }
            "clean" { Worktree-Clean }
            default {
                Write-Host "未知的 worktree 子命令: $SubCommand"
                Show-Help
                exit 1
            }
        }
    }
    "init" {
        Write-Host "请使用 init-project.ps1 脚本初始化工作空间"
        Write-Host "或在原项目目录中运行 /ease:gitflow init"
    }
    { $_ -in "help", "--help", "-h" } { Show-Help }
    default {
        Write-Host "未知的命令: $Command"
        Show-Help
        exit 1
    }
}
