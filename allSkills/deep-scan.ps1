# Deep C Drive Scan - Find large files and cleanup opportunities
param(
    [int]$TopN = 20,
    [int]$MinSizeMB = 100
)

Write-Host "Scanning C Drive for files larger than $MinSizeMB MB..." -ForegroundColor Cyan

# 1. User Downloads
Write-Host "`n=== DOWNLOADS ===" -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\Downloads") {
    Get-ChildItem "$env:USERPROFILE\Downloads" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt ($MinSizeMB * 1MB) } |
        Sort-Object Length -Descending |
        Select-Object -First $TopN |
        Format-Table Name, @{N='SizeMB';E={'{0:N2}' -f ($_.Length/1MB)}}, LastWriteTime -AutoSize
}

# 2. User Desktop
Write-Host "`n=== DESKTOP ===" -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\Desktop") {
    Get-ChildItem "$env:USERPROFILE\Desktop" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt ($MinSizeMB * 1MB) } |
        Sort-Object Length -Descending |
        Select-Object -First $TopN |
        Format-Table Name, @{N='SizeMB';E={'{0:N2}' -f ($_.Length/1MB)}}, LastWriteTime -AutoSize
}

# 3. User Videos
Write-Host "`n=== VIDEOS ===" -ForegroundColor Yellow
if (Test-Path "$env:USERPROFILE\Videos") {
    Get-ChildItem "$env:USERPROFILE\Videos" -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Length -gt ($MinSizeMB * 1MB) } |
        Sort-Object Length -Descending |
        Select-Object -First $TopN |
        Format-Table Name, @{N='SizeMB';E={'{0:N2}' -f ($_.Length/1MB)}}, LastWriteTime -AutoSize
}

# 4. Check for Docker/VM images
Write-Host "`n=== DOCKER ===" -ForegroundColor Yellow
if (Test-Path "$env:LOCALAPPDATA\Docker") {
    Get-ChildItem "$env:LOCALAPPDATA\Docker" -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -match '\.vhd|\.vhdx|\.qcow2|\.vmdk' -and $_.Length -gt 500MB } |
        Sort-Object Length -Descending |
        Select-Object -First $TopN FullName, @{N='SizeGB';E={'{0:N2}' -f ($_.Length/1GB)}} |
        Format-Table -AutoSize
}

# 5. Check for WSL/Virtual Machine files
Write-Host "`n=== WSL / VM FILES ===" -ForegroundColor Yellow
if (Test-Path "$env:LOCALAPPDATA\Packages") {
    Get-ChildItem "$env:LOCALAPPDATA\Packages" -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Extension -match '\.vhdx|\.vhd' -and $_.Length -gt 1GB } |
        Sort-Object Length -Descending |
        Select-Object -First $TopN FullName, @{N='SizeGB';E={'{0:N2}' -f ($_.Length/1GB)}} |
        Format-Table -AutoSize
}

# 6. Check for installer packages in root
Write-Host "`n=== ROOT INSTALLERS ===" -ForegroundColor Yellow
Get-ChildItem "C:\" -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Extension -match '\.exe|\.msi|\.zip' -and $_.Length -gt ($MinSizeMB * 1MB) } |
    Sort-Object Length -Descending |
    Select-Object -First $TopN Name, @{N='SizeMB';E={'{0:N2}' -f ($_.Length/1MB)}}, LastWriteTime |
    Format-Table -AutoSize

# 7. Check for old Windows versions
Write-Host "`n=== WINDOWS.OLD ===" -ForegroundColor Yellow
if (Test-Path "C:\Windows.old") {
    $size = (Get-ChildItem "C:\Windows.old" -Recurse -ErrorAction SilentlyContinue |
             Measure-Object -Property Length -Sum).Sum
    Write-Host "Windows.old found: $([math]::Round($size/1GB,2)) GB" -ForegroundColor Red
    Write-Host "Can be removed with: Get-ComputerInfo | Select-Object WindowsVersion" -ForegroundColor Yellow
}

# 8. Check for duplicate installers
Write-Host "`n=== MULTIPLE VERSION INSTALLERS ===" -ForegroundColor Yellow
Get-ChildItem "$env:USERPROFILE\Downloads" -File -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '-\d+\.\d+\.?\d*-' -and $_.Extension -match '\.exe|\.msi' } |
    Group-Object { $_.Name -replace '-\d+\.\d+\.?\d*--', '-XX.XX-' } |
    Where-Object { $_.Count -gt 1 } |
    ForEach-Object {
        Write-Host "`nFound $($_.Count) versions of:" -ForegroundColor Cyan
        $_.Group | Format-Table Name, @{N='SizeMB';E={'{0:N2}' -f ($_.Length/1MB)}} -AutoSize
    }

Write-Host "`n=== SCAN COMPLETE ===" -ForegroundColor Green
