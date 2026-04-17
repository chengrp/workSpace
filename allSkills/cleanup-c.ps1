# C Drive Cleanup Script v1.0
# Target: Free 47-57 GB space
# Author: Claude Code

param(
    [switch]$WhatIf,    # Dry run
    [switch]$Admin      # Enable admin-only operations
)

# Color output functions
function Write-Section {
    param([string]$Title)
    Write-Host "`n$('=' * 60)" -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host "$('=' * 60)" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor White
}

# Safe delete with size tracking
function Remove-SafeItem {
    param(
        [string]$Path,
        [string]$Description,
        [switch]$Recurse
    )

    if (-not (Test-Path $Path)) {
        Write-Warning "$Description - Path not found"
        return 0
    }

    # Calculate size
    $sizeBefore = 0
    if ($Recurse) {
        $sizeBefore = (Get-ChildItem -Path $Path -Recurse -ErrorAction SilentlyContinue |
                      Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    } else {
        $sizeBefore = (Get-Item $Path -ErrorAction SilentlyContinue).Length
    }
    $sizeMB = [math]::Round($sizeBefore / 1MB, 2)

    # Delete
    try {
        if ($WhatIf) {
            Write-Info "[DRY RUN] $Description - Will free $sizeMB MB"
            return $sizeMB
        }

        Remove-Item -Path $Path -Recurse:$Recurse -Force -ErrorAction Stop
        Write-Success "$Description - Freed $sizeMB MB"
        return $sizeMB
    }
    catch {
        Write-Warning "$Description - Failed: $($_.Exception.Message)"
        return 0
    }
}

$TotalFreed = 0

# === 1. Lark/Feishu Cache (15-20 GB) ===
Write-Section "1. Lark/Feishu Cache (Expected: 15-20 GB)"

$larkCache = @(
    "$env:LOCALAPPDATA\LarkShell\cache",
    "$env:LOCALAPPDATA\LarkShell\Code Cache",
    "$env:LOCALAPPDATA\LarkShell\GPUCache",
    "$env:APPDATA\Lark\cache"
)

foreach ($path in $larkCache) {
    $freed = Remove-SafeItem -Path $path -Description "Lark: $path" -Recurse
    $TotalFreed += $freed
}

# === 2. Chrome Cache (10-15 GB) ===
Write-Section "2. Chrome Cache (Expected: 10-15 GB)"

$chromeCache = @(
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Code Cache",
    "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\GPUCache"
)

foreach ($path in $chromeCache) {
    $freed = Remove-SafeItem -Path $path -Description "Chrome: $path" -Recurse
    $TotalFreed += $freed
}

# === 3. Large Apps (12 GB) ===
Write-Section "3. Large Applications"

# Perplexity (~6GB)
$perplexityPath = "$env:LOCALAPPDATA\Perplexity"
if (Test-Path $perplexityPath) {
    $freed = Remove-SafeItem -Path $perplexityPath -Description "Perplexity app" -Recurse
    $TotalFreed += $freed
}

# Ubuntu ISO (~6.2GB)
$isoPaths = @(
    "$env:USERPROFILE\Downloads\ubuntu-*-desktop-amd64.iso",
    "D:\ProjectAI\CC\ubuntu-*-desktop-amd64.iso"
)

foreach ($pattern in $isoPaths) {
    $dir = Split-Path $pattern
    $filePattern = Split-Path $pattern -Leaf
    if (Test-Path $dir) {
        $isos = Get-ChildItem -Path $dir -Filter $filePattern -ErrorAction SilentlyContinue
        foreach ($iso in $isos) {
            $freed = Remove-SafeItem -Path $iso.FullName -Description "Ubuntu ISO: $($iso.Name)" -Recurse
            $TotalFreed += $freed
        }
    }
}

# === 4. Windows Temp ===
Write-Section "4. Windows Temporary Files"

$tempPaths = @(
    "$env:TEMP\*",
    "$env:LOCALAPPDATA\Temp\*"
)

if ($Admin) {
    $tempPaths += "$env:WINDIR\Temp\*"
}

foreach ($pattern in $tempPaths) {
    $freed = Remove-SafeItem -Path $pattern -Description "Temp files" -Recurse
    $TotalFreed += $freed
}

# === 5. Dev Tools Cache (2-5 GB) ===
Write-Section "5. Development Tools Cache"

$devCache = @(
    "$env:USERPROFILE\.npm\_cacache",
    "$env:USERPROFILE\.yarn\cache",
    "$env:LOCALAPPDATA\pip\cache"
)

foreach ($path in $devCache) {
    $freed = Remove-SafeItem -Path $path -Description "Dev cache: $path" -Recurse
    $TotalFreed += $freed
}

# === Final Report ===
Write-Section "Cleanup Complete!"

$TotalFreedGB = [math]::Round($TotalFreed / 1GB, 2)
Write-Success "Total freed: $TotalFreedGB GB"

$cDrive = Get-PSDrive C
$freeGB = [math]::Round($cDrive.Free / 1GB, 2)
$usedPercent = [math]::Round((1 - $cDrive.Free / $cDrive.Total) * 100, 1)

Write-Host "`nCurrent C Drive Status:" -ForegroundColor Cyan
Write-Host "  Free Space: $freeGB GB" -ForegroundColor Green
Write-Host "  Usage:      $usedPercent%" -ForegroundColor $(if ($usedPercent -lt 90) { "Green" } else { "Red" })

if ($WhatIf) {
    Write-Host "`n[DRY RUN] To execute, run without -WhatIf" -ForegroundColor Yellow
}
