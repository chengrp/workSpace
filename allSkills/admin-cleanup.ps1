# ============================================================
# C盘管理员权限清理脚本 v1.0
# 作者: Claude Code
# 日期: 2026-03-31
# ============================================================

#Requires -RunAsAdministrator

param(
    [switch]$WhatIf    # 模拟运行
    [switch]$Backup    # 创建备份
)

# ============================================================
# 全局变量
# ============================================================
$Global:TotalFreed = 0
$Global:BackupRoot = "C:\AdminCleanup_Backup"
$Global:LogFile = "$PSScriptRoot\admin-cleanup.log"

# ============================================================
# 日志函数
# ============================================================
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | $Message" | Out-File -FilePath $Global:LogFile -Append
    Write-Host "[$timestamp] $Message"
}

function Write-Success {
    param([string]$Message)
    Write-Log "✓ $Message"
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Log "⚠ $Message"
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Log "✗ $Message"
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Section {
    param([string]$Title)
    Write-Log ""
    Write-Log "=== $Title ==="
    Write-Host "`n=== $Title ===" -ForegroundColor Cyan
}

# ============================================================
# 备份函数
# ============================================================
function Backup-Item {
    param(
        [string]$Path,
        [string]$Description
    )

    if (-not $Backup) {
        return
    }

    $backupPath = Join-Path $Global:BackupRoot (Split-Path $Path -Leaf)

    try {
        if (Test-Path $Path) {
            $null = New-Item -ItemType Directory -Force $Global:BackupRoot -ErrorAction Stop
            Copy-Item -Path $Path -Destination $backupPath -Recurse -Force -ErrorAction Stop
            Write-Warning "备份: $Description -> $backupPath"
        }
    }
    catch {
        Write-Error "备份失败: $Description - $($_.Exception.Message)"
    }
}

# ============================================================
# 安全删除函数
# ============================================================
function Remove-AdminItem {
    param(
        [string]$Path,
        [string]$Description,
        [switch]$StopProcess
    )

    if (-not (Test-Path $Path)) {
        Write-Warning "跳过: $Description - 路径不存在"
        return 0
    }

    # 计算大小
    $sizeBefore = (Get-ChildItem $Path -Recurse -File -ErrorAction SilentlyContinue |
                    Measure-Object -Property Length -Sum).Sum
    $sizeMB = [math]::Round($sizeBefore / 1MB, 2)

    # 停止进程
    if ($StopProcess) {
        $processName = Split-Path $Path -Leaf
        Get-Process | Where-Object { $_.ProcessName -like "*$processName*" } |
            Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }

    # 备份
    Backup-Item -Path $Path -Description $Description

    # 执行删除
    try {
        if ($WhatIf) {
            Write-Warning "[模拟] $Description - 将删除 $sizeMB MB"
            return $sizeMB
        }

        Remove-Item -Path $Path -Recurse -Force -ErrorAction Stop
        Write-Success "$Description - 已删除 $sizeMB MB"
        return $sizeMB
    }
    catch {
        Write-Error "$Description - 删除失败: $($_.Exception.Message)"
        return 0
    }
}

# ============================================================
# 开始清理
# ============================================================
Write-Section "C盘管理员权限清理开始"

$Global:TotalFreed = 0

# ============================================================
# 1. Lenovo PCManager 旧版本 (1.22 GB)
# ============================================================
Write-Section "1. 清理Lenovo PCManager旧版本"

Write-Host "停止PCManager进程..." -ForegroundColor Yellow
Get-Process -Name "LenovoPcManager" -ErrorAction SilentlyContinue |
    Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

$freed = Remove-AdminItem -Path "C:\Program Files (x86)\Lenovo\PCManager\5.1.150.11202" `
    -Description "PCManager 5.1.150.11202" -StopProcess
$Global:TotalFreed += $freed

# ============================================================
# 2. SLBrowser旧版本
# ============================================================
Write-Section "2. 清理Lenovo SLBrowser旧版本"

Write-Host "停止SLBrowser进程..." -ForegroundColor Yellow
Get-Process -Name "SLBrowser*" -ErrorAction SilentlyContinue |
    Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 1

$freed = Remove-AdminItem -Path "C:\Program Files (x86)\Lenovo\SLBrowser\9.0.6.7021" `
    -Description "SLBrowser 9.0.6.7021" -StopProcess
$Global:TotalFreed += $freed

# ============================================================
# 3. Windows Kits 8.1
# ============================================================
Write-Section "3. 清理Windows Kits 8.1"

$freed = Remove-AdminItem -Path "C:\Program Files (x86)\Windows Kits\8.1" `
    -Description "Windows Kits 8.1"
$Global:TotalFreed += $freed

# ============================================================
# 4. Windows临时文件
# ============================================================
Write-Section "4. 清理Windows临时文件"

$tempPaths = @(
    "C:\Windows\Temp\*",
    "C:\Windows\Logs\CBS\*"
)

foreach ($pattern in $tempPaths) {
    $freed = Remove-AdminItem -Path $pattern -Description "Windows临时文件"
    $Global:TotalFreed += $freed
}

# ============================================================
# 5. 回收站
# ============================================================
Write-Section "5. 清空回收站"

Write-Host "清空回收站..." -ForegroundColor Yellow
try {
    Clear-RecycleBin -Force -ErrorAction Stop
    $recycleSize = (Get-ChildItem "C:\`$Recycle.Bin" -Recurse -Force -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum).Sum
    $recycleMB = [math]::Round($recycleSize / 1MB, 2)
    Write-Success "回收站 - 已清理 $recycleMB MB"
    $Global:TotalFreed += $recycleMB
}
catch {
    Write-Error "回收站清理失败"
}

# ============================================================
# 最终报告
# ============================================================
Write-Section "清理完成"

$cDrive = Get-PSDrive C
$freeGB = [math]::Round($cDrive.Free / 1GB, 2)
$usedPercent = [math]::Round((1 - $cDrive.Free / $cDrive.Total) * 100, 1)

Write-Success "总计释放: $([math]::Round($Global:TotalFreed/1GB, 2)) GB"
Write-Host "当前C盘可用: $freeGB GB" -ForegroundColor Cyan
Write-Host "使用率: $usedPercent%" -ForegroundColor $(if ($usedPercent -lt 85) { "Green" } else { "Red" })

if ($WhatIf) {
    Write-Host "`n[模拟模式] 要实际执行，请运行: .\admin-cleanup.ps1" -ForegroundColor Yellow
}

Write-Host "`n备份位置: $Global:BackupRoot" -ForegroundColor Gray
Write-Host "日志文件: $Global:LogFile" -ForegroundColor Gray
