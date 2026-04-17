# PicGo 服务端静默启动脚本
# 用于开机自启动，隐藏窗口运行

# 检查是否已经在运行
$port = Get-NetTCPConnection -LocalPort 36677 -ErrorAction SilentlyContinue
if ($port) {
    exit
}

# 启动 PicGo 服务端（隐藏窗口）
$processInfo = New-Object System.Diagnostics.ProcessStartInfo
$processInfo.FileName = "C:\Users\RyanCh\AppData\Roaming\npm\picgo.cmd"
$processInfo.Arguments = "server"
$processInfo.WindowStyle = [System.Diagnostics.ProcessWindowStyle]::Hidden
$processInfo.CreateNoWindow = $true

$process = New-Object System.Diagnostics.Process
$process.StartInfo = $processInfo
$process.Start() | Out-Null
