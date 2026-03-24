# GitFlow Worktree 项目初始化脚本 (PowerShell) - 裸仓库模式
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

param(
    [switch]$Force,
    [switch]$SkipGitFlow,
    [string]$Master = "master",
    [string]$Develop = "develop"
)

# 配置变量
$MASTER_BRANCH = $Master
$DEVELOP_BRANCH = $Develop

Write-Host ""
Write-Host "🔧 GitFlow Worktree 初始化（裸仓库模式）" -ForegroundColor Cyan
Write-Host "=========================================="
Write-Host ""

# ============================================
# 1. 检查前置条件
# ============================================
Write-Host "[1/6] 检查前置条件..." -ForegroundColor Blue

# 检查 Git 版本
$gitVersionOutput = git --version
$gitVersion = [regex]::Match($gitVersionOutput, '\d+\.\d+').Value
$gitMajor = [int]($gitVersion.Split('.')[0])
$gitMinor = [int]($gitVersion.Split('.')[1])

if ($gitMajor -lt 2 -or ($gitMajor -eq 2 -and $gitMinor -lt 15)) {
    Write-Host "❌ Git 版本过低（当前: $gitVersion，要求: >= 2.15）" -ForegroundColor Red
    Write-Host "   请升级 Git 以支持 worktree 功能"
    exit 1
}
Write-Host "   ✅ Git 版本: $gitVersion" -ForegroundColor Green

# 检查 git-flow 工具
if (-not $SkipGitFlow) {
    $gitFlowCheck = Get-Command git-flow -ErrorAction SilentlyContinue
    if (-not $gitFlowCheck) {
        Write-Host "❌ 未检测到 git-flow 工具" -ForegroundColor Red
        Write-Host ""
        Write-Host "请先安装 git-flow："
        Write-Host "  Windows: choco install gitflow-avh"
        Write-Host "  或参考 https://github.com/nvie/gitflow/wiki/Installation"
        Write-Host ""
        Write-Host "或使用 -SkipGitFlow 跳过 git flow 初始化"
        exit 1
    }
    Write-Host "   ✅ git-flow 已安装" -ForegroundColor Green
}

# 检查是否在 Git 仓库中
$isGitRepo = git rev-parse --is-inside-work-tree 2>$null
if ($isGitRepo -ne "true") {
    Write-Host "❌ 当前目录不是 Git 仓库" -ForegroundColor Red
    Write-Host "   请在已有的 Git 项目目录中运行此命令"
    exit 1
}
Write-Host "   ✅ Git 仓库检测通过" -ForegroundColor Green

Write-Host "✅ 前置条件检查通过" -ForegroundColor Green

# ============================================
# 2. 获取仓库信息
# ============================================
Write-Host ""
Write-Host "[2/6] 获取仓库信息..." -ForegroundColor Blue

# 获取仓库根目录
$REPO_ROOT = git rev-parse --show-toplevel
$PROJECT_NAME = Split-Path $REPO_ROOT -Leaf
$PARENT_DIR = Split-Path $REPO_ROOT -Parent
$WORKSPACE_DIR = Join-Path $PARENT_DIR "$PROJECT_NAME-workspace"

# 获取远程仓库地址
$REMOTE_URL = git remote get-url origin 2>$null

if (-not $REMOTE_URL) {
    Write-Host "❌ 未找到远程仓库地址（origin）" -ForegroundColor Red
    Write-Host "   请先配置远程仓库："
    Write-Host "   git remote add origin <repository-url>"
    exit 1
}

Write-Host "   项目名称: $PROJECT_NAME"
Write-Host "   项目路径: $REPO_ROOT"
Write-Host "   远程地址: $REMOTE_URL"
Write-Host "   工作空间: $WORKSPACE_DIR"

Write-Host "✅ 仓库信息获取完成" -ForegroundColor Green

# ============================================
# 3. 创建工作空间目录
# ============================================
Write-Host ""
Write-Host "[3/6] 创建工作空间目录..." -ForegroundColor Blue

if (Test-Path $WORKSPACE_DIR) {
    if (-not $Force) {
        Write-Host "   工作空间目录已存在: $WORKSPACE_DIR"
        Write-Host "   ⚠️ 跳过创建，如需重新初始化请使用 -Force 参数" -ForegroundColor Yellow
        
        # 检查是否已经初始化完成
        $bareExists = Test-Path (Join-Path $WORKSPACE_DIR ".bare")
        $gitFileExists = Test-Path (Join-Path $WORKSPACE_DIR ".git")
        
        if ($bareExists -and $gitFileExists) {
            Write-Host ""
            Write-Host "✅ 工作空间已初始化完成！" -ForegroundColor Green
            Write-Host ""
            Write-Host "📁 工作空间: $WORKSPACE_DIR"
            Write-Host ""
            Write-Host "🚀 可用命令："
            Write-Host "   cd $WORKSPACE_DIR\master    # 进入 master 分支"
            Write-Host "   cd $WORKSPACE_DIR\develop   # 进入 develop 分支"
            exit 0
        }
    } else {
        Write-Host "   ⚠️ 强制模式：清理现有工作空间..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $WORKSPACE_DIR
    }
}

New-Item -ItemType Directory -Force -Path $WORKSPACE_DIR | Out-Null
Write-Host "   ✅ 工作空间目录已创建: $WORKSPACE_DIR"

Write-Host "✅ 工作空间目录就绪" -ForegroundColor Green

# ============================================
# 4. 克隆裸仓库
# ============================================
Write-Host ""
Write-Host "[4/6] 克隆裸仓库..." -ForegroundColor Blue

Push-Location $WORKSPACE_DIR

Write-Host "   执行: git clone --bare $REMOTE_URL .bare"
$cloneResult = git clone --bare $REMOTE_URL .bare 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ 克隆裸仓库失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "请检查："
    Write-Host "  1. 网络连接是否正常"
    Write-Host "  2. 远程仓库地址是否正确"
    Write-Host "  3. Git 认证是否配置正确"
    Pop-Location
    exit 1
}

Write-Host "   ✅ 裸仓库克隆完成"

Write-Host "✅ 裸仓库就绪" -ForegroundColor Green

# ============================================
# 5. 创建 .git 指向文件
# ============================================
Write-Host ""
Write-Host "[5/6] 配置 Git 指向..." -ForegroundColor Blue

# 创建 .git 文件指向裸仓库
"gitdir: ./.bare" | Out-File -FilePath ".git" -Encoding ASCII -NoNewline
Write-Host "   ✅ 创建 .git 文件指向 .bare"

# 配置裸仓库以支持 worktree
Push-Location .bare
git config core.bare false
git config core.worktree "../"
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
Pop-Location

Write-Host "   ✅ Git 配置完成"

Write-Host "✅ Git 指向配置完成" -ForegroundColor Green

# ============================================
# 6. 创建 worktree 并初始化 GitFlow
# ============================================
Write-Host ""
Write-Host "[6/6] 创建 worktree 并初始化 GitFlow..." -ForegroundColor Blue

# 创建 master worktree
Write-Host "   创建 master worktree..."
$masterRefRemote = git show-ref --verify refs/remotes/origin/$MASTER_BRANCH 2>$null
$masterRefLocal = git show-ref --verify refs/heads/$MASTER_BRANCH 2>$null

if ($masterRefRemote -or $masterRefLocal) {
    git worktree add $MASTER_BRANCH $MASTER_BRANCH 2>$null
    if ($LASTEXITCODE -ne 0) {
        git worktree add $MASTER_BRANCH "origin/$MASTER_BRANCH" 2>$null
        if ($LASTEXITCODE -ne 0) {
            git worktree add $MASTER_BRANCH -b $MASTER_BRANCH "origin/$MASTER_BRANCH"
        }
    }
    Write-Host "   ✅ master worktree 已创建"
} else {
    # 如果 master 分支不存在，从默认分支创建
    $defaultBranch = git symbolic-ref refs/remotes/origin/HEAD 2>$null
    if ($defaultBranch) {
        $defaultBranch = $defaultBranch -replace 'refs/remotes/origin/', ''
    } else {
        $defaultBranch = "main"
    }
    Write-Host "   ⚠️ $MASTER_BRANCH 分支不存在，从 $defaultBranch 创建..." -ForegroundColor Yellow
    git worktree add $MASTER_BRANCH -b $MASTER_BRANCH "origin/$defaultBranch"
    Write-Host "   ✅ master worktree 已创建（基于 $defaultBranch）"
}

# 初始化 git flow
if (-not $SkipGitFlow) {
    Write-Host "   初始化 git flow..."
    Push-Location $MASTER_BRANCH
    
    # 使用非交互式方式初始化 git flow
    $initResult = git flow init -d -f 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠️ git flow init 需要手动确认，请执行以下命令：" -ForegroundColor Yellow
        Write-Host "   cd $WORKSPACE_DIR\$MASTER_BRANCH"
        Write-Host "   git flow init"
    }
    
    Pop-Location
    Write-Host "   ✅ git flow 已初始化"
}

# 创建 develop worktree
Write-Host "   创建 develop worktree..."
$developRefRemote = git show-ref --verify refs/remotes/origin/$DEVELOP_BRANCH 2>$null
$developRefLocal = git show-ref --verify refs/heads/$DEVELOP_BRANCH 2>$null

if ($developRefRemote -or $developRefLocal) {
    git worktree add $DEVELOP_BRANCH $DEVELOP_BRANCH 2>$null
    if ($LASTEXITCODE -ne 0) {
        git worktree add $DEVELOP_BRANCH "origin/$DEVELOP_BRANCH" 2>$null
        if ($LASTEXITCODE -ne 0) {
            git worktree add $DEVELOP_BRANCH -b $DEVELOP_BRANCH "origin/$DEVELOP_BRANCH" 2>$null
            if ($LASTEXITCODE -ne 0) {
                git worktree add $DEVELOP_BRANCH -b $DEVELOP_BRANCH $MASTER_BRANCH
            }
        }
    }
    Write-Host "   ✅ develop worktree 已创建"
} else {
    # 从 master 创建 develop
    git worktree add $DEVELOP_BRANCH -b $DEVELOP_BRANCH $MASTER_BRANCH
    Write-Host "   ✅ develop worktree 已创建（基于 $MASTER_BRANCH）"
}

# 推送 develop 分支到远程
Push-Location $DEVELOP_BRANCH
git push -u origin $DEVELOP_BRANCH 2>$null
Pop-Location

Pop-Location  # 回到原目录

Write-Host "✅ worktree 和 GitFlow 初始化完成" -ForegroundColor Green

# ============================================
# 显示完成信息
# ============================================
Write-Host ""
Write-Host "=========================================="
Write-Host "🎉 GitFlow Worktree 初始化完成！" -ForegroundColor Green
Write-Host "=========================================="
Write-Host ""
Write-Host "📁 工作空间目录结构："
Write-Host ""
Write-Host "   $PROJECT_NAME-workspace\"
Write-Host "   ├── .bare\           # 裸仓库（Git 数据）"
Write-Host "   ├── .git             # 指向 .bare"
Write-Host "   ├── $MASTER_BRANCH\             # master 分支 worktree"
Write-Host "   └── $DEVELOP_BRANCH\            # develop 分支 worktree"
Write-Host ""
Write-Host "📋 配置信息："
Write-Host "   主分支: $MASTER_BRANCH"
Write-Host "   开发分支: $DEVELOP_BRANCH"
Write-Host "   远程仓库: $REMOTE_URL"
Write-Host ""
Write-Host "🚀 下一步操作："
Write-Host ""
Write-Host "   # 进入工作空间"
Write-Host "   cd $WORKSPACE_DIR"
Write-Host ""
Write-Host "   # 开始新功能开发"
Write-Host "   git worktree add feature\<name> -b feature/<name> $DEVELOP_BRANCH"
Write-Host "   cd feature\<name>"
Write-Host ""
Write-Host "   # 创建发布分支"
Write-Host "   git worktree add release\v1.0.0 -b release/v1.0.0 $DEVELOP_BRANCH"
Write-Host ""
Write-Host "   # 创建热修复分支"
Write-Host "   git worktree add hotfix\<name> -b hotfix/<name> $MASTER_BRANCH"
Write-Host ""
Write-Host "📖 更多帮助："
Write-Host "   /ease:gitflow help"
Write-Host ""
