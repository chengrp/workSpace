# C盘隐藏空间分析脚本

Write-Host "=== 系统隐藏文件分析 ===" -ForegroundColor Cyan

# 1. 页面文件
Write-Host "`n=== 页面文件 ===" -ForegroundColor Yellow
$pageFile = "C:\pagefile.sys"
if (Test-Path $pageFile) {
    $size = (Get-Item $pageFile -Force).Length / 1GB
    Write-Host "$pageFile : $([math]::Round($size, 2)) GB"
} else {
    Write-Host "未找到页面文件"
}

# 2. 休眠文件
Write-Host "`n=== 休眠文件 ===" -ForegroundColor Yellow
$hiberFile = "C:\hiberfil.sys"
if (Test-Path $hiberFile) {
    $size = (Get-Item $hiberFile -Force).Length / 1GB
    Write-Host "$hiberFile : $([math]::Round($size, 2)) GB"
    Write-Host "提示: 如果不使用休眠功能，可以禁用以释放空间"
    Write-Host "禁用命令: powercfg -h off"
} else {
    Write-Host "未找到休眠文件（可能已禁用）"
}

# 3. 交换文件
Write-Host "`n=== 交换文件 ===" -ForegroundColor Yellow
$swapFile = "C:\swapfile.sys"
if (Test-Path $swapFile) {
    $size = (Get-Item $swapFile -Force).Length / 1GB
    Write-Host "$swapFile : $([math]::Round($size, 2)) GB"
} else {
    Write-Host "未找到交换文件"
}

# 4. 系统还原点
Write-Host "`n=== 系统还原点 ===" -ForegroundColor Yellow
try {
    $restorePoints = Get-ComputerRestorePoint
    if ($restorePoints) {
        Write-Host "发现 $($restorePoints.Count) 个系统还原点"
        $restorePoints | Select-Object -First 10 | Format-Table CreationTime, Description, SequenceNumber -AutoSize

        # 估算还原点占用的空间（需要管理员权限）
        try {
            $shadowStorage = Get-WmiObject Win32_ShadowStorage -ErrorAction SilentlyContinue
            if ($shadowStorage) {
                $usedGB = [math]::Round($shadowStorage.UsedSpace / 1GB, 2)
                $maxGB = [math]::Round($shadowStorage.MaxSpace / 1GB, 2)
                Write-Host "还原点占用空间: $usedGB GB / $maxGB GB"
            }
        } catch {
            Write-Host "无法获取还原点空间占用信息（需要管理员权限）"
        }
    } else {
        Write-Host "未发现系统还原点"
    }
} catch {
    Write-Host "无法获取系统还原点信息"
}

# 5. WindowsApps 中的大型游戏/应用
Write-Host "`n=== WindowsApps 大型应用 ===" -ForegroundColor Yellow
$windowsAppsPath = "C:\Program Files\WindowsApps"
if (Test-Path $windowsAppsPath) {
    try {
        $apps = Get-ChildItem $windowsAppsPath -Directory -ErrorAction SilentlyContinue
        $largeApps = @()
        foreach ($app in $apps) {
            try {
                $size = (Get-ChildItem $app.FullName -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
                if ($size -gt 500MB) {
                    $sizeGB = [math]::Round($size/1GB, 2)
                    $largeApps += [PSCustomObject]@{
                        Name = $app.Name
                        SizeGB = $sizeGB
                    }
                }
            } catch { }
        }
        $largeApps | Sort-Object SizeGB -Descending | Select-Object -First 10 | Format-Table -AutoSize
    } catch {
        Write-Host "无法分析 WindowsApps（需要管理员权限）"
    }
}

# 6. 回收站
Write-Host "`n=== 回收站 ===" -ForegroundColor Yellow
$recycleBin = "C:\`$Recycle.Bin"
if (Test-Path $recycleBin) {
    $recycleSize = (Get-ChildItem $recycleBin -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $recycleGB = [math]::Round($recycleSize/1GB, 2)
    Write-Host "回收站占用: $recycleGB GB"
    Write-Host "提示: 右键回收站 → 清空回收站"
}

# 7. Windows.old（升级后遗留）
Write-Host "`n=== Windows 升级遗留文件 ===" -ForegroundColor Yellow
$windowsOld = "C:\Windows.old"
if (Test-Path $windowsOld) {
    $oldSize = (Get-ChildItem $windowsOld -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
    $oldGB = [math]::Round($oldSize/1GB, 2)
    Write-Host "发现 Windows.old 文件夹: $oldGB GB"
    Write-Host "提示: 可以通过磁盘清理工具安全删除"
}

# 8. Users 文件夹详细分析
Write-Host "`n=== Users 文件夹详细分析 ===" -ForegroundColor Yellow
$userPaths = @(
    "$env:USERPROFILE\AppData\Roaming",
    "$env:USERPROFILE\AppData\Local\Google\Chrome\User Data",
    "$env:USERPROFILE\AppData\Local\Google\Chrome\User Data\Default\Cache",
    "$env:USERPROFILE\Videos",
    "$env:USERPROFILE\Pictures",
    "$env:USERPROFILE\Music",
    "$env:USERPROFILE\Documents"
)

foreach ($path in $userPaths) {
    if (Test-Path $path) {
        try {
            $size = (Get-ChildItem $path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $sizeGB = [math]::Round($size/1GB, 2)
            Write-Host "$path : $sizeGB GB"
        } catch {
            Write-Host "$path : 无法计算"
        }
    }
}

# 9. 空间占用汇总
Write-Host "`n=== 空间占用汇总 ===" -ForegroundColor Cyan
$totalAccounted = 0
$items = @()

# 根目录文件夹
$rootSizes = @{
    "Windows" = 25.47
    "Users" = 24.63
    "Program Files" = 13.93
    "Program Files (x86)" = 13.57
    "ProgramData" = 7.62
}

foreach ($item in $rootSizes.GetEnumerator()) {
    $items += [PSCustomObject]@{
        Item = $item.Key
        SizeGB = $item.Value
    }
    $totalAccounted += $item.Value
}

# 隐藏文件
$pageFileSize = 0
$hiberFileSize = 0
if (Test-Path "C:\pagefile.sys") { $pageFileSize = (Get-Item "C:\pagefile.sys" -Force).Length / 1GB }
if (Test-Path "C:\hiberfil.sys") { $hiberFileSize = (Get-Item "C:\hiberfil.sys" -Force).Length / 1GB }

if ($pageFileSize -gt 0) {
    $items += [PSCustomObject]@{ Item = "pagefile.sys"; SizeGB = [math]::Round($pageFileSize, 2) }
    $totalAccounted += $pageFileSize
}
if ($hiberFileSize -gt 0) {
    $items += [PSCustomObject]@{ Item = "hiberfil.sys"; SizeGB = [math]::Round($hiberFileSize, 2) }
    $totalAccounted += $hiberFileSize
}

$items | Sort-Object SizeGB -Descending | Format-Table -AutoSize

Write-Host "`n已统计总计: $([math]::Round($totalAccounted, 2)) GB"
Write-Host "实际已用: 185.8 GB"
Write-Host "差异: $([math]::Round(185.8 - $totalAccounted, 2)) GB"

Write-Host "`n=== 推荐清理操作 ===" -ForegroundColor Green
Write-Host "1. 禁用休眠功能 (如果不用): powercfg -h off"
Write-Host "2. 清理系统还原点: 控制面板 → 系统 → 系统保护"
Write-Host "3. 运行磁盘清理: cleanmgr /sagerun:1"
Write-Host "4. 清理 Chrome 缓存: Chrome 设置 → 清除浏览数据"
Write-Host "5. 清理临时文件夹: %temp%"
Write-Host "6. 检查虚拟内存设置: 此电脑 → 属性 → 高级系统设置"
