# C盘磁盘空间分析脚本

Write-Host "=== C盘总体情况 ===" -ForegroundColor Cyan
$drive = Get-PSDrive C
$usedGB = [math]::Round($drive.Used/1GB, 2)
$freeGB = [math]::Round($drive.Free/1GB, 2)
$totalGB = $usedGB + $freeGB
Write-Host "已用: $usedGB GB" -ForegroundColor Yellow
Write-Host "剩余: $freeGB GB" -ForegroundColor Red
Write-Host "总计: $totalGB GB"
Write-Host ""

# 分析关键目录
$keyPaths = @(
    "C:\Users",
    "C:\Program Files",
    "C:\Program Files (x86)",
    "C:\ProgramData",
    "C:\Windows",
    "C:\inetpub",
    "C:\Projects",
    "C:\CC_Projects"
)

Write-Host "=== 关键目录大小分析 ===" -ForegroundColor Cyan
$results = @()

foreach ($path in $keyPaths) {
    if (Test-Path $path) {
        try {
            $size = (Get-ChildItem $path -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
            $sizeGB = [math]::Round($size/1GB, 2)
            $results += [PSCustomObject]@{
                Path = $path
                SizeGB = $sizeGB
            }
        } catch {
            $results += [PSCustomObject]@{
                Path = $path
                SizeGB = "N/A"
            }
        }
    }
}

$results | Sort-Object {[double]$_.SizeGB} -Descending | Format-Table -AutoSize

Write-Host ""
Write-Host "=== 用户文件夹详细分析 ===" -ForegroundColor Cyan
$userPaths = @(
    "$env:USERPROFILE\.claude",
    "$env:USERPROFILE\AppData\Local",
    "$env:USERPROFILE\AppData\Roaming",
    "$env:USERPROFILE\Downloads",
    "$env:USERPROFILE\Videos",
    "$env:USERPROFILE\Pictures",
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

Write-Host ""
Write-Host "=== 查找大文件（>1GB） ===" -ForegroundColor Cyan
Get-ChildItem C:\ -Recurse -ErrorAction SilentlyContinue | Where-Object { $_.Length -gt 1GB -and !$_.PSIsContainer } | Select-Object FullName, @{Name='SizeGB';Expression={[math]::Round($_.Length/1GB,2)}} | Sort-Object SizeGB -Descending | Format-Table -AutoSize
