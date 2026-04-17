#Requires -RunAsAdministrator

Write-Host "=== 强制删除 PCManager 旧版本 ===" -ForegroundColor Cyan

# 1. 停止所有相关进程
Write-Host "`n[1/3] 停止PCManager相关进程..." -ForegroundColor Yellow

$processNames = @(
    "LenovoPcManagerService",
    "MSPCManagerService",
    "MSPCManagerCore",
    "MSPCManager"
)

foreach ($name in $processNames) {
    $processes = Get-Process -Name $name -ErrorAction SilentlyContinue
    if ($processes) {
        $processes | Stop-Process -Force -ErrorAction SilentlyContinue
        Write-Host "  已停止: $name" -ForegroundColor Green
    }
}

Start-Sleep -Seconds 3

# 验证进程是否停止
$remaining = Get-Process -Name "*PCManager*" -ErrorAction SilentlyContinue
if ($remaining) {
    Write-Host "  警告: 仍有进程运行，尝试强制终止..." -ForegroundColor Yellow
    $remaining | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# 2. 删除目标目录
Write-Host "`n[2/3] 删除目标目录..." -ForegroundColor Yellow

$targetPath = "C:\Program Files (x86)\Lenovo\PCManager\5.1.150.11202"

if (Test-Path $targetPath) {
    try {
        # 获取大小
        $sizeBefore = (Get-ChildItem $targetPath -Recurse -File -ErrorAction SilentlyContinue |
                       Measure-Object -Property Length -Sum).Sum
        $sizeMB = [math]::Round($sizeBefore / 1MB, 2)

        Remove-Item -Path $targetPath -Recurse -Force -ErrorAction Stop
        Write-Host "  已删除: $targetPath ($sizeMB MB)" -ForegroundColor Green
    }
    catch {
        Write-Host "  删除失败: $($_.Exception.Message)" -ForegroundColor Red

        # 尝试用 takeown 获取所有权
        Write-Host "`n  尝试获取文件所有权..." -ForegroundColor Yellow
        & takeown /F $targetPath /R /D Y 2>$null
        & icacls $targetPath /grant Administrators:F /T 2>$null
        Start-Sleep -Seconds 1

        # 再次尝试删除
        try {
            Remove-Item -Path $targetPath -Recurse -Force -ErrorAction Stop
            Write-Host "  已删除: $targetPath" -ForegroundColor Green
        }
        catch {
            Write-Host "  最终失败: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}
else {
    Write-Host "  路径不存在: $targetPath" -ForegroundColor Gray
}

# 3. 验证并报告
Write-Host "`n[3/3] 验证删除结果..." -ForegroundColor Yellow

if (Test-Path $targetPath) {
    Write-Host "  ❌ 目录仍然存在" -ForegroundColor Red
}
else {
    Write-Host "  ✅ 目录已成功删除" -ForegroundColor Green
}

# 检查C盘空间
$cDrive = Get-PSDrive C
$freeGB = [math]::Round($cDrive.Free / 1GB, 2)
Write-Host "`n当前C盘可用: $freeGB GB" -ForegroundColor Cyan
