# ============================================================
# C盘一键清理脚本 v1.0
# 目标：释放 47-57 GB 空间
# 作者：Claude Code PUA模式
# 日期：2026-03-30
# ============================================================

param(
    [switch]$WhatIf,    # 模拟运行，不实际删除
    [switch]$Admin      # 是否启用管理员权限操作
)

# ============================================================
# 颜色输出函数
# ============================================================
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Section {
    param([string]$Title)
    Write-Host "`n$('═' * 60)" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "$('═' * 60)" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# ============================================================
# 安全删除函数（带大小统计）
# ============================================================
function Remove-SafeItem {
    param(
        [string]$Path,
        [string]$Description,
        [switch]$Recurse
    )

    if (-not (Test-Path $Path)) {
        Write-Warning "$Description - 路径不存在，跳过"
        return 0
    }

    # 计算大小
    $sizeBefore = 0
    if ($Recurse) {
        $sizeBefore = (Get-ChildItem -Path $Path -Recurse -ErrorAction SilentlyContinue |
                      Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    } else {
        $sizeBefore = (Get-Item $Path -ErrorAction SilentlyContinue).Length
    }
    $sizeMB = [math]::Round($sizeBefore / 1MB, 2)

    # 执行删除
    try {
        if ($WhatIf) {
            Write-Host "[模拟] " -NoNewline
            Write-Warning "$Description - 将删除 $sizeMB MB"
            return $sizeMB
        }

        Remove-Item -Path $Path -Recurse:$Recurse -Force -ErrorAction Stop
        Write-Success "$Description - 已释放 $sizeMB MB"
        return $sizeMB
    }
    catch {
        Write-Error "$Description - 删除失败: $($_.Exception.Message)"
        return 0
    }
}

# ============================================================
# 1. 飞书缓存清理 (目标: 15-20 GB)
# ============================================================
$TotalFreed = 0

Write-Section "清理飞书缓存 (预计释放 15-20 GB)"

# LarkShell Cache
$larkCache = @(
    "$env:LOCALAPPDATA\LarkShell\cache",
    "$env:LOCALAPPDATA\LarkShell\Code Cache",
    "$env:LOCALAPPDATA\LarkShell\GPUCache",
    "$env:APPDATA\Lark\cache"
)

foreach ($path in $larkCache) {
    $freed = Remove-SafeItem -Path $path -Description "Lark缓存: $path" -Recurse
    $TotalFreed += $freed
}

# ============================================================
# 2. Chrome缓存清理 (目标: 10-15 GB)
# ============================================================
Write-Section "清理Chrome缓存 (预计释放 10-15 GB)"

$chromeCache = @(
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache"
)

foreach ($path in $chromeCache) {
    $freed = Remove-SafeItem -Path $path -Description "Chrome缓存: $path" -Recurse
    $TotalFreed += $freed
}

# ============================================================
# 3. 删除大型应用 (目标: 12 GB)
# ============================================================
Write-Section "删除大型应用"

# Perplexity (约6GB)
$perplexityPath = "$env:LOCALAPPDATA\Perplexity"
if (Test-Path $perplexityPath) {
    Write-Warning "检测到Perplexity应用 (约6GB)"
    $freed = Remove-SafeItem -Path $perplexityPath -Description "Perplexity" -Recurse
    $TotalFreed += $freed
}

# Ubuntu ISO (约6.2GB)
$ubuntuIsoPaths = @(
    "$env:USERPROFILE\Downloads\ubuntu-*-desktop-amd64.iso",
    "$HOME\Downloads\ubuntu-*-desktop-amd64.iso",
    "D:\ProjectAI\CC\ubuntu-*-desktop-amd64.iso"
)

foreach ($pattern in $ubuntuIsoPaths) {
    $isos = Get-ChildItem -Path (Split-Path $pattern) -Filter (Split-Path $pattern -Leaf) -ErrorAction SilentlyContinue
    foreach ($iso in $isos) {
        $sizeMB = [math]::Round($iso.Length / 1MB, 2)
        $freed = Remove-SafeItem -Path $iso.FullName -Description "Ubuntu ISO: $($iso.Name)" -Recurse
        $TotalFreed += $freed
    }
}

# ============================================================
# 4. Windows缓存清理
# ============================================================
Write-Section "清理Windows缓存"

# 临时文件
$tempPaths = @(
    "$env:TEMP\*",
    "$env:LOCALAPPDATA\Temp\*"
)

# 管理员权限才能清理系统临时文件夹
if ($Admin) {
    $tempPaths += "$env:WINDIR\Temp\*"
}

foreach ($pattern in $tempPaths) {
    $freed = Remove-SafeItem -Path $pattern -Description "临时文件" -Recurse
    $TotalFreed += $freed
}

# 回收站
$recycleBinSize = (Get-ChildItem -Path "C:\`$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue |
                  Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
if ($recycleBinSize -gt 1GB) {
    Write-Warning "回收站占用: $([math]::Round($recycleBinSize/1MB,2)) MB"
    Write-Host "请手动清空回收站或运行: Clear-RecycleBin -Force" -ForegroundColor Yellow
}

# ============================================================
# 5. 开发工具缓存
# ============================================================
Write-Section "清理开发工具缓存"

$devCache = @(
    "$env:USERPROFILE\.npm\_cacache",
    "$env:USERPROFILE\.yarn\cache",
    "$env:LOCALAPPDATA\pip\cache"
)

foreach ($path in $devCache) {
    $freed = Remove-SafeItem -Path $path -Description "开发缓存: $path" -Recurse
    $TotalFreed += $freed
}

# ============================================================
# 6. 最终报告
# ============================================================
Write-Section "清理完成！"

$TotalFreedGB = [math]::Round($TotalFreed / 1GB, 2)
Write-Success "总计释放空间: $TotalFreedGB GB"

# 获取当前C盘状态
$cDrive = Get-PSDrive C
$freeGB = [math]::Round($cDrive.Free / 1GB, 2)
$usedPercent = [math]::Round((1 - $cDrive.Free / $cDrive.Total) * 100, 1)

Write-Host "`n当前C盘状态:" -ForegroundColor Cyan
Write-Host "  可用空间: $freeGB GB" -ForegroundColor Green
Write-Host "  使用率:   $usedPercent%" -ForegroundColor $(if ($usedPercent -lt 90) { "Green" } else { "Red" })

Write-Host "`n提示: 建议重启电脑以完全释放被占用的文件" -ForegroundColor Yellow

if ($WhatIf) {
    Write-Host "`n[模拟模式] 要实际执行清理，请运行: .\cleanup-c-drive.ps1" -ForegroundColor Yellow
}
