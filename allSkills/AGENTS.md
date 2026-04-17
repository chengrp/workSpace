# Claude Code Skills 项目指南

> 📅 最后更新：2026-02-12
> 📍 项目位置：`D:\ProjectAI\CC\CC_record\skills`

---

## 📖 项目概述

这是一个完整的 **Claude Code Skills 管理系统**，用于存储、管理和维护 AI Agent 技能（Skills）。Skills 是模块化的、自包含的功能包，通过提供专业知识、工作流程和工具集成来扩展 Claude 的能力。

### 核心功能

1. **技能存储** - 集中管理所有已安装的 Skills
2. **版本追踪** - 跟踪 Skills 来源和更新状态
3. **技能进化** - 基于使用反馈持续改进技能
4. **生态系统** - 支持从多个来源导入技能

---

## 🏗️ 项目结构

```
skills/
├── SKILL_LIST.md          # 技能清单（主要参考文档）
├── README_MASTER.md       # 系统使用指南
├── superpowers-QUICKSTART.md  # Superpowers 快速入门
│
├── 📦 核心技能集合
│   ├── anthropic-skills/      # Anthropic 官方技能
│   ├── awesomeAgentskills/    # 精选第三方技能
│   ├── baoyu-skills/          # Baoyu 内容创作技能包
│   ├── Khazix-Skills/         # 技能生命周期管理
│   └── superpowers/           # 完整开发工作流系统
│
├── 🎨 内容创作技能
│   ├── ms-image/              # ModelScope AI 绘图
│   ├── ppt-generator/         # AI 驱动 PPT 生成器
│   ├── document-illustrator/  # 文档配图生成器
│   ├── all-2md/               # 全格式文档转换器
│   ├── notebooklm/            # NotebookLM 研究助手
│   └── x-article-publisher/   # X (Twitter) 文章发布器
│
├── 🔧 开发工具技能
│   ├── skill-creator/         # 技能创建指南
│   ├── mcp-builder/           # MCP 服务器构建
│   ├── webapp-testing/        # Web 应用测试
│   └── n8n-skills/            # n8n 工作流自动化
│
├── ✍️ 写作技能
│   ├── writing-workflow/      # 写作自动化工作流
│   ├── wechat-writing/        # 微信公众号写作
│   ├── prompt-copilot/        # 提示词领航员
│   └── Humanizer-zh/          # 中文人性化改写
│
└── 🔄 Superpowers 工作流技能
    ├── brainstorming/         # 交互式设计优化
    ├── writing-plans/         # 详细实施计划
    ├── test-driven-development/  # 测试驱动开发
    ├── systematic-debugging/  # 系统化调试
    └── ... (共14个技能)
```

---

## 🚀 快速开始

### 技能使用方式

1. **自动触发** - 描述任务，匹配的技能会自动激活
2. **明确指定** - "使用写作 skill 帮我..."
3. **Slash 命令** - `/writing-workflow`

### 常用命令

```bash
# 查看 Python 版本
python --version  # Python 3.14.0

# 查看 Git 版本
git --version     # git version 2.51.0.windows.2
```

---

## 📚 技能分类详解

### 1. 内容创作技能

| 技能 | 用途 | 特点 |
|------|------|------|
| **ms-image** | AI 图片生成 | 每天 2000 张免费额度，支持图生图 |
| **ppt-generator** | PPT 生成 | 多风格支持，AI 转场视频 |
| **baoyu-skills** | 内容创作包 | 13 个专业技能，小红书/公众号发布 |
| **document-illustrator** | 文档配图 | AI 智能归纳，三种风格 |
| **all-2md** | 文档转换 | PDF/Word/PPT/Excel → Markdown |

### 2. 开发工作流 (Superpowers)

完整软件开发流程：

```
brainstorming → using-git-worktrees → writing-plans → 
subagent-driven-development → test-driven-development → 
requesting-code-review → finishing-a-development-branch
```

核心理念：
- **测试驱动开发 (TDD)** - 始终先写测试
- **系统化优于临时** - 流程优于猜测
- **证据优于声明** - 验证后再宣布成功

### 3. 技能管理 (Khazix-Skills)

生命周期管理：

| 阶段 | 工具 | 功能 |
|------|------|------|
| 创建 | github-to-skills | GitHub 仓库 → AI skill |
| 维护 | skill-manager | 检查更新、列表、删除 |
| 进化 | skill-evolution-manager | 基于反馈持续改进 |

---

## 🛠️ 技能开发规范

### 技能目录结构

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter
│   │   ├── name: (必需)
│   │   └── description: (必需，触发机制)
│   └── Markdown 指令
└── 可选资源
    ├── scripts/     # 可执行代码
    ├── references/  # 参考文档
    └── assets/      # 模板/资源文件
```

### 核心原则

1. **简洁至上** - Context window 是公共资源
2. **适度约束** - 根据任务脆弱性设定自由度
3. **渐进披露** - 三级加载：元数据 → SKILL.md → 资源文件

### SKILL.md 编写要点

```yaml
---
name: my-skill-name
description: 清晰描述功能和使用触发条件
---

# 技能名称

## 概述
[简短描述]

## 使用方式
[具体指令]

## 脚本目录
[如适用，列出 scripts/ 内容]
```

---

## 📦 依赖环境

### 系统环境
- **Python**: 3.14.0
- **Git**: 2.51.0.windows.2
- **平台**: Windows (win32)

### 常用 Python 包
```
requests, pillow, python-docx, openpyxl, python-pptx
google-genai, markitdown, PyYAML
```

### 环境变量配置

部分技能需要配置 API 密钥：

```bash
# ms-image (内置)
# ppt-generator
YUNWU_API_KEY=xxx

# document-illustrator
GEMINI_API_KEY=xxx

# baoyu-skills (~/.baoyu-skills/.env)
OPENAI_API_KEY=sk-xxx
GOOGLE_API_KEY=xxx
```

---

## 🔧 常用脚本

### 技能管理

```bash
# 创建新技能
python skill-creator/scripts/init_skill.py <skill-name> --path <output-directory>

# 打包技能
python skill-creator/scripts/package_skill.py <path/to/skill-folder>

# 检查技能更新
/skill-manager check

# 列出所有技能
/skill-manager list
```

### 内容生成

```bash
# AI 图片生成
python ms-image/scripts/ms_image_generator.py "A golden cat" -s "1920x1080"

# 文档转换
markitdown path/to/document.pdf -o output.md

# PPT 生成
/ppt-generator-pro
```

---

## 📋 重要文件说明

| 文件 | 用途 |
|------|------|
| `SKILL_LIST.md` | 所有已安装技能的详细清单 |
| `README_MASTER.md` | 系统完整使用指南 |
| `superpowers-QUICKSTART.md` | Superpowers 快速入门 |
| `collect_skills_info.ps1` | 收集技能信息的 PowerShell 脚本 |

---

## 🌐 外部资源

- **Agent Skills 规范**: https://agentskills.io/specification
- **Superpowers**: https://github.com/obra/superpowers
- **Baoyu Skills**: https://github.com/JimLiu/baoyu-skills
- **Khazix Skills**: https://github.com/KKKKhazix/Khazix-Skills
- **Anthropic Skills**: https://github.com/anthropics/skills

---

## 💡 最佳实践

### 技能使用

1. **阅读 SKILL.md** - 使用前先了解技能功能
2. **检查依赖** - 确保环境配置正确
3. **测试验证** - 新技能先用简单任务测试

### 技能开发

1. **理解场景** - 明确具体使用案例
2. **规划资源** - 确定需要的 scripts/references/assets
3. **初始化模板** - 使用 `init_skill.py` 创建结构
4. **测试脚本** - 实际运行确保无 bug
5. **迭代改进** - 基于使用反馈持续优化

### 技能维护

1. **定期检查更新** - `/skill-manager check`
2. **记录所有权** - 配置 `ownership_config.json`
3. **备份重要数据** - 定期备份配置文件

---

## ⚠️ 注意事项

1. **Windows 环境** - 使用 PowerShell/CMD 命令，避免 Linux 特定语法
2. **命令链** - PowerShell 5.1 不支持 `&&`，使用 `; if($?) {cmd2}`
3. **路径格式** - 优先使用绝对路径
4. **敏感信息** - API 密钥等敏感信息不要提交到版本控制

---

## 📝 更新日志

- **2026-02-12**: 创建 AGENTS.md
- **2026-01-23**: 更新 SKILL_LIST.md
- **2026-01-22**: 创建 README_MASTER.md
- **2026-01-12**: 安装 Superpowers 技能集

---

**提示**: 详细技能列表请参考 [SKILL_LIST.md](SKILL_LIST.md)
