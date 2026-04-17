# 手动技能管理工作流

## 系统架构（当前状态）

```
C:\Users\RyanCh\.claude\skills  →  Junction  →  D:\ProjectAI\CC\CC_record\skills
                                                        ↓
                                              单点真理源（所有技能存储于此）
```

**关键点：**
- `.claude/skills` 是 Junction（无需管理员权限）
- 所有技能的实际文件都在 `CC_record/skills`
- 修改任一位置会同步到另一位置（同一目录）
- **不再使用** Vercel Skills CLI (`npx skills add`)

## 添加新技能

### 方法 1：从 GitHub 克隆（推荐）

```powershell
# 进入技能目录
cd D:\ProjectAI\CC\CC_record\skills

# 克隆技能仓库
git clone https://github.com/用户名/技能仓库名.git 技能目录名

# 验证技能可访问
ls C:\Users\RyanCh\.claude\skills\技能目录名
```

**示例：**
```powershell
# 安装 paul-graham-skill
cd D:\ProjectAI\CC\CC_record\skills
git clone https://github.com/alchaincyf/paul-graham-skill.git

# 验证
ls C:\Users\RyanCh\.claude\skills\paul-graham-skill
```

### 方法 2：手动下载并解压

1. 从 GitHub 下载 ZIP 文件
2. 解压到 `D:\ProjectAI\CC\CC_record\skills\技能目录名`
3. 验证技能可访问

### 方法 3：创建自定义技能

```powershell
# 创建技能目录
mkdir D:\ProjectAI\CC\CC_record\skills\my-custom-skill

# 创建 SKILL.md 文件
cat > D:\ProjectAI\CC\CC_record\skills\my-custom-skill\SKILL.md << 'EOF'
---
name: my-custom-skill
description: 我的自定义技能
---

# 技能说明

这里写技能的使用说明...
EOF
```

## 更新技能

```powershell
# 进入技能目录
cd D:\ProjectAI\CC\CC_record\skills\技能目录名

# 拉取最新代码
git pull origin main
```

## 删除技能

```powershell
# 直接删除 CC_record 中的目录
rm -r D:\ProjectAI\CC\CC_record\skills\技能目录名

# 由于 Junction，.claude/skills 中的引用会自动消失
```

## 技能结构规范

每个技能应包含：

```
技能目录名/
├── SKILL.md              # 必需：技能定义文件（YAML frontmatter + 内容）
├── README.md             # 可选：技能说明文档
├── scripts/              # 可选：工具脚本
└── references/           # 可选：参考文档
```

**SKILL.md 最小示例：**
```markdown
---
name: my-skill
description: 技能简短描述
---

# 技能名称

技能详细说明...

## 使用方法

触发词：`/my-skill`
```

## 验证技能是否正常工作

```powershell
# 检查技能文件存在
ls C:\Users\RyanCh\.claude\skills\技能目录名\SKILL.md

# 在 Claude Code 中测试
# 输入触发词，看是否正确加载技能
```

## 故障排查

### 问题：技能在 Claude Code 中不可见

**检查：**
```powershell
# 1. 验证 Junction 完好
powershell -Command "Get-Item 'C:\Users\RyanCh\.claude\skills' | Select-Object LinkType, Target"

# 应显示：
# LinkType  Target
# --------  -----
# Junction  {D:\ProjectAI\CC\CC_record\skills}

# 2. 验证技能文件存在
ls D:\ProjectAI\CC\CC_record\skills\技能目录名\SKILL.md
```

### 问题：Junction 损坏

**修复：**
```powershell
# 删除损坏的 Junction
rm C:\Users\RyanCh\.claude\skills

# 重新创建 Junction
cmd /c "mklink /J C:\Users\RyanCh\.claude\skills D:\ProjectAI\CC\CC_record\skills"
```

## 迁移历史

- **2026-04-14**: 卸载 Vercel Skills CLI，切换到手动管理
- **迁移前**: 技能分散在 `.agents/skills` 和 `.claude/skills`
- **迁移后**: 统一到 `CC_record/skills`，`.claude/skills` 作为 Junction

## 相关命令参考

```powershell
# 查看 Junction 目标
Get-Item "路径" | Select-Object LinkType, Target

# 创建 Junction（无需管理员权限）
cmd /c "mklink /J 链接路径 目标路径"

# 删除 Junction
rm 链接路径
```
