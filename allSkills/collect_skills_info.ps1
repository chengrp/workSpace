# 收集所有Skill信息的脚本
$skillsBasePath = "~/.claude/skills"
$allSkills = @()

# 递归查找所有SKILL.md文件
$skillFiles = Get-ChildItem -Path $skillsBasePath -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue

# 为了去重，使用哈希表
$uniqueSkills = @{}

foreach ($skillFile in $skillFiles) {
    # 提取skill名称（从路径中）
    $pathParts = $skillFile.FullName.Split('\')
    $skillName = ""

    # 查找skill名称（通常是包含SKILL.md的目录的父目录名）
    for ($i = 0; $i -lt $pathParts.Length; $i++) {
        if ($pathParts[$i] -eq "skills" -and $i -lt $pathParts.Length - 1) {
            $skillName = $pathParts[$i + 1]
            break
        }
    }

    # 如果找不到skill名称，使用目录名
    if ([string]::IsNullOrEmpty($skillName)) {
        $skillName = $skillFile.Directory.Name
    }

    # 跳过重复的skill
    if ($uniqueSkills.ContainsKey($skillName)) {
        continue
    }
    $uniqueSkills[$skillName] = $true

    # 读取SKILL.md内容
    $content = Get-Content $skillFile.FullName -Raw -ErrorAction SilentlyContinue

    # 提取触发词
    $triggerWords = ""
    if ($content -match 'Trigger:\s*(.+?)[\r\n]+') {
        $triggerWords = $matches[1].Trim()
    }

    # 提取描述
    $description = ""
    if ($content -match 'Description:\s*(.+?)[\r\n]+[\r\n]+|#') {
        $description = $matches[1].Trim()
    } else {
        # 获取前200个字符作为描述
        $lines = $content -split "`n"
        $descLines = @()
        foreach ($line in $lines) {
            if ($line -notmatch '^#' -and $line.Trim() -ne '') {
                $descLines += $line
                if ($descLines.Count -ge 3) { break }
            }
        }
        $description = $descLines -join ' '
        if ($description.Length -gt 200) {
            $description = $description.Substring(0, 200) + "..."
        }
    }

    # 获取目录大小
    $skillDir = $skillFile.Directory
    $sizeBytes = 0
    try {
        $sizeBytes = (Get-ChildItem -Path $skillDir.FullName -Recurse -File -ErrorAction SilentlyContinue |
                     Measure-Object -Property Length -Sum).Sum
    } catch {
        $sizeBytes = 0
    }
    $sizeMB = [math]::Round($sizeBytes / 1MB, 2)

    # 获取安装时间（目录创建时间）
    $installDate = $skillDir.CreationTime

    # 获取最后修改时间
    $lastModified = $skillDir.LastWriteTime

    # 尝试从README或其他文件中获取GitHub地址
    $githubUrl = ""
    $readmeFiles = Get-ChildItem -Path $skillDir.Parent.FullName -Filter "README.md" -ErrorAction SilentlyContinue
    if ($readmeFiles) {
        $readmeContent = Get-Content $readmeFiles[0].FullName -Raw -ErrorAction SilentlyContinue
        if ($readmeContent -match 'github\.com/([^/\s]+)/([^/\s]+)') {
            $githubUrl = "https://github.com/$($matches[1])/$($matches[2])"
        }
    }

    # 如果README中没有找到，尝试从skill目录中查找
    if ([string]::IsNullOrEmpty($githubUrl)) {
        $readmeInSkill = Get-ChildItem -Path $skillDir.FullName -Filter "README.md" -ErrorAction SilentlyContinue
        if ($readmeInSkill) {
            $readmeContent = Get-Content $readmeInSkill[0].FullName -Raw -ErrorAction SilentlyContinue
            if ($readmeContent -match 'github\.com/([^/\s]+)/([^/\s]+)') {
                $githubUrl = "https://github.com/$($matches[1])/$($matches[2])"
            }
        }
    }

    $allSkills += [PSCustomObject]@{
        Name = $skillName
        Path = $skillDir.FullName
        TriggerWords = $triggerWords
        Description = $description
        SizeMB = $sizeMB
        InstallDate = $installDate
        LastModified = $lastModified
        GitHubUrl = $githubUrl
        HasTriggerWords = -not [string]::IsNullOrEmpty($triggerWords)
    }
}

# 按名称排序
$allSkills = $allSkills | Sort-Object Name

# 导出为JSON供后续使用
$allSkills | ConvertTo-Json -Depth 3 | Out-File -FilePath "skills_data.json" -Encoding UTF8

Write-Host "找到 $($allSkills.Count) 个独立的Skill"
Write-Host "数据已保存到 skills_data.json"
