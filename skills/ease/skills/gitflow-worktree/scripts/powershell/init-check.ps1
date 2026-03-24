# GitFlow Worktree 环境检查脚本（裸仓库模式）- PowerShell 版本

# 最低 Git 版本要求
$MIN_GIT_VERSION = "2.15"

Write-Host ""
Write-Host "🔍 GitFlow Worktree 环境检查" -ForegroundColor Cyan
Write-Host "============================"
Write-Host ""

$finalStatus = 0

# ============================================
# 1. 检查 Git 是否安装
# ============================================
Write-Host "[1/5] 检查 Git 安装..." -ForegroundColor Blue

$gitCommand = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCommand) {
    Write-Host "❌ Git 未安装" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装 Git："
    Write-Host "  Windows: https://git-scm.com/download/win"
    Write-Host "  或使用: choco install git"
    $finalStatus = 1
} else {
    Write-Host "✅ Git 已安装" -ForegroundColor Green
}

# ============================================
# 2. 检查 Git 版本
# ============================================
if ($finalStatus -eq 0) {
    Write-Host "[2/5] 检查 Git 版本..." -ForegroundColor Blue
    
    $gitVersionOutput = git --version
    $gitVersion = [regex]::Match($gitVersionOutput, '\d+\.\d+').Value
    $gitMajor = [int]($gitVersion.Split('.')[0])
    $gitMinor = [int]($gitVersion.Split('.')[1])
    
    $minMajor = [int]($MIN_GIT_VERSION.Split('.')[0])
    $minMinor = [int]($MIN_GIT_VERSION.Split('.')[1])
    
    Write-Host "   当前版本: $gitVersion"
    Write-Host "   最低要求: $MIN_GIT_VERSION"
    
    if ($gitMajor -lt $minMajor -or ($gitMajor -eq $minMajor -and $gitMinor -lt $minMinor)) {
        Write-Host "❌ Git 版本过低，不支持 worktree" -ForegroundColor Red
        Write-Host ""
        Write-Host "请升级 Git 到 $MIN_GIT_VERSION 或更高版本"
        $finalStatus = 1
    } else {
        Write-Host "✅ Git 版本满足要求" -ForegroundColor Green
    }
}

# ============================================
# 3. 检查是否在 Git 仓库中
# ============================================
if ($finalStatus -eq 0) {
    Write-Host "[3/5] 检查 Git 仓库..." -ForegroundColor Blue
    
    $isGitRepo = git rev-parse --is-inside-work-tree 2>$null
    if ($isGitRepo -ne "true") {
        Write-Host "❌ 当前目录不是 Git 仓库" -ForegroundColor Red
        Write-Host ""
        Write-Host "请在 Git 仓库目录中运行此命令"
        $finalStatus = 1
    } else {
        $repoRoot = git rev-parse --show-toplevel
        Write-Host "   仓库路径: $repoRoot"
        Write-Host "✅ Git 仓库存在" -ForegroundColor Green
    }
}

# ============================================
# 4. 检查远程仓库
# ============================================
if ($finalStatus -eq 0) {
    Write-Host "[4/5] 检查远程仓库..." -ForegroundColor Blue
    
    $remoteUrl = git remote get-url origin 2>$null
    if (-not $remoteUrl) {
        Write-Host "❌ 未配置远程仓库（origin）" -ForegroundColor Red
        Write-Host ""
        Write-Host "请先配置远程仓库："
        Write-Host "   git remote add origin <repository-url>"
        $finalStatus = 1
    } else {
        Write-Host "   远程仓库: $remoteUrl"
        Write-Host "✅ 远程仓库已配置" -ForegroundColor Green
    }
}

# ============================================
# 5. 检查 git-flow 工具
# ============================================
if ($finalStatus -eq 0) {
    Write-Host "[5/5] 检查 git-flow 工具..." -ForegroundColor Blue
    
    $gitFlowCommand = Get-Command git-flow -ErrorAction SilentlyContinue
    if (-not $gitFlowCommand) {
        Write-Host "❌ git-flow 未安装" -ForegroundColor Red
        Write-Host ""
        Write-Host "请安装 git-flow："
        Write-Host "  Windows: choco install gitflow-avh"
        Write-Host "  或参考 https://github.com/nvie/gitflow/wiki/Installation"
        $finalStatus = 1
    } else {
        Write-Host "✅ git-flow 已安装" -ForegroundColor Green
    }
}

# ============================================
# 显示检查结果摘要
# ============================================
Write-Host ""
Write-Host "============================"
Write-Host "📊 检查结果摘要"
Write-Host "============================"
Write-Host ""

if ($finalStatus -eq 0) {
    Write-Host "✅ 所有检查通过！环境已就绪" -ForegroundColor Green
    Write-Host ""
    Write-Host "🚀 现在可以运行初始化命令："
    Write-Host "   /ease:gitflow init"
    Write-Host ""
    Write-Host "初始化后将创建以下目录结构："
    Write-Host ""
    Write-Host "   <project>-workspace\"
    Write-Host "   ├── .bare\           # 裸仓库"
    Write-Host "   ├── .git             # 指向 .bare"
    Write-Host "   ├── master\          # master 分支"
    Write-Host "   └── develop\         # develop 分支"
} else {
    Write-Host "❌ 环境检查失败" -ForegroundColor Red
    Write-Host ""
    Write-Host "请解决上述问题后重试"
}

exit $finalStatus
