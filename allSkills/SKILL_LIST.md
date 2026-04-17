# Claude Code Skills 列表

> 最后更新：2026-01-23
>
> 📋 **技能优先级配置**: 详见 [SKILL_PRIORITY.md](SKILL_PRIORITY.md)

当前可用的 Claude Code 技能列表。所有技能位于：`D:\ProjectAI\CC\CC_record\skills\`

---

## 📝 已安装技能

### 1. **ms-image** ⭐⭐⭐ 优先级: 1
**ModelScope 免费AI绘图**

- **用途**：AI图片生成、图生图（根据参考图生成同风格图片）
- **特点**：
  - 每天免费2000张图片额度
  - 使用通义千问Turbo模型（快速生成）
  - 支持图生图功能（上传参考图生成同风格）
  - 支持多种比例：16:9、9:16、1:1等
  - 自定义尺寸控制
  - 高质量图片输出（FHD级别）
- **依赖**：
  - Python 3.9+
  - requests, pillow
- **使用示例**：
  - "帮我生成一张图片，内容是'一只金色的猫'"
  - "用AI画一个赛博朋克风格的城市"
  - "根据这张图片生成同风格的..."（图生图）
- **命令行使用**：
  ```bash
  python scripts/ms_image_generator.py "A golden cat" -s "1920x1080"
  python scripts/ms_image_generator.py "A dog" -r reference.jpg -o result.jpg
  ```
- **API Key**：内置（ms-51dd7494-0706-45d9-a901-c395522c55f2）
- **最新更新**：v1.1 - 2025-01-15
  - ✅ 修复尺寸控制问题
  - ✅ 新增图生图功能
  - ✅ 支持自定义尺寸参数
- **文件**：[SKILL.md](ms-image/SKILL.md) | [README.md](ms-image/README.md) | [IMPROVEMENT_REPORT.md](ms-image/IMPROVEMENT_REPORT.md)

---

### 2. **writing-workflow** ⭐⭐⭐ 优先级: 2
**写作自动化工作流 Skill**

- **用途**：公众号文章、技术博客、视频脚本、产品文档、营销文案
- **特点**：
  - 两层判断机制（工作区 + 任务类型）
  - Think Aloud 透明化思考
  - 强制调研确保信息准确
  - 选题讨论避免方向错误
  - 个人素材库降 AI 味
  - **三遍审校机制**（系统化降 AI 检测率至 30% 以下）
  - 完整配图流程
- **最新更新**：2026-01-09 - 升级了降 AI 味审校清单
- **文件**：[SKILL.md](writing-workflow/SKILL.md) | [README.md](writing-workflow/README.md)

---

### 3. **dev-best-practices** ⭐⭐⭐ 优先级: 3
**全局开发最佳实践**

- **用途**：跨项目的通用开发经验、需求沟通模式、问题解决方法
- **特点**：
  - 4个常见问题模式库（浮点数、边界、缓存、选择器）
  - 测试驱动开发流程
  - 开发工作流 SOP
  - 快速参考卡片
  - 持续迭代更新
- **最新更新**：2026-01-10 - 基于字体缩放功能开发经验创建
- **文件**：[SKILL.md](dev-best-practices/SKILL.md) | [CHANGELOG.md](dev-best-practices/references/CHANGELOG.md)

---

### 3. **prompt-copilot**
**提示词领航员 (Prompt Co-Pilot)**

- **用途**：提示词梳理、技术文档编写、清晰指令构建
- **特点**：结构化提示、版本管理、示例驱动
- **文件**：[SKILL.md](prompt-copilot/SKILL.md)

---

### 4. **pptx**
**PowerPoint 演示文稿创建**

- **用途**：创建、编辑、分析 PPT 文件
- **特点**：支持布局修改、内容添加、注释和演讲者备注
- **文件**：[SKILL.md](pptx/SKILL.md)

---

### 5. **skill-creator**
**技能创建指南**

- **用途**：创建新的 Claude Code 技能
- **特点**：提供设计原则、文件结构要求、最佳实践
- **文件**：[SKILL.md](skill-creator/SKILL.md)

---

### 6. **webapp-testing**
**Web 应用测试**

- **用途**：UI 测试、API 测试、端到端测试
- **特点**：完整的测试工作流和最佳实践
- **文件**：[SKILL.md](webapp-testing/SKILL.md)

---

### 7. **n8n-skills**
**n8n 工作流自动化**

- **用途**：创建、管理、故障排除 n8n 工作流和节点
- **特点**：工作流自动化平台专用技能
- **文件**：[SKILL.md](n8n-skills/SKILL.md)

---

### 8. **mcp-builder**
**MCP 服务器构建指南**

- **用途**：构建高质量的 Model Context Protocol (MCP) 服务器
- **特点**：
  - 支持 Python (FastMCP) 和 Node/TypeScript
  - 最佳实践和评估指南
  - 工具设计原则
- **文件**：[SKILL.md](mcp-builder/SKILL.md)

---

### 9. **Skill_Seekers**
**技能发现和评估**

- **用途**：发现、评估和选择 Claude Code 技能
- **特点**：技能库导航、能力对比、使用指南
- **文件**：[SKILL.md](Skill_Seekers/SKILL.md)

---

### 10. **planning-with-files**
**基于文件的规划**

- **用途**：使用文件进行项目规划和管理
- **特点**：结构化文档、工作流优化
- **文件**：[SKILL.md](planning-with-files/planning-with-files/SKILL.md)

---

### 11. **x-article-publisher** ⭐ 新安装
**X (Twitter) 文章发布器**

- **用途**：将 Markdown 文章自动发布到 X (Twitter) Articles
- **特点**：
  - 自动转换 Markdown 到富文本格式
  - 智能图片定位 (block-index 技术)
  - 自动上传封面图和内容图
  - 仅保存草稿，绝不自动发布
  - 10倍效率提升（20-30分钟 → 2-3分钟）
- **依赖**：
  - Playwright MCP（浏览器自动化）
  - X Premium Plus 订阅
  - Python 3.9+ + Pillow
- **使用示例**：
  - "Publish /path/to/article.md to X"
  - "Help me post this article to X Articles: ~/Documents/my-post.md"
  - `/x-article-publisher /path/to/article.md`
- **最新更新**：v1.1.0 - 2025-12
- **来源**：https://github.com/wshuyi/x-article-publisher-skill
- **文件**：[SKILL.md](x-article-publisher/SKILL.md)

---

### 12. **notebooklm** ⭐⭐⭐ 新安装
**NotebookLM 研究助手 (Google NotebookLM 集成)**

- **用途**：让 Claude Code 直接与 Google NotebookLM 通信，获取基于你上传文档的准确答案
- **特点**：
  - 源自文档的答案（大幅减少幻觉）
  - 浏览器自动化（无需复制粘贴）
  - 持久身份验证（一次登录，长期使用）
  - 智能库管理（保存笔记本链接与标签）
  - 引用支持（每个答案都包含来源参考）
  - 多源关联（连接50+文档间的信息）
- **依赖**：
  - Python 3.9+
  - Patchright（浏览器自动化库）
  - Google Chrome（自动安装）
- **使用示例**：
  - "设置 NotebookLM 身份验证"
  - "添加这个 NotebookLM 到我的库：[链接]"
  - "查询我的 API 文档关于 [主题]"
  - "显示我的 NotebookLM 笔记本"
- **工作流程**：
  ```bash
  # 1. 检查身份验证状态
  python scripts/run.py auth_manager.py status

  # 2. 首次使用需要身份验证（会打开浏览器登录 Google）
  python scripts/run.py auth_manager.py setup

  # 3. 添加笔记本到库
  python scripts/run.py notebook_manager.py add --url "[URL]" --name "名称" --description "描述" --topics "主题1,主题2"

  # 4. 查询笔记本
  python scripts/run.py ask_question.py --question "你的问题" --notebook-url "[URL]"
  ```
- **注意事项**：
  - 仅适用于本地 Claude Code（不适用于 Web UI）
  - 笔记本必须公开分享
  - 无状态设计（每次查询独立）
- **最新更新**：v1.0 - 2026-01-21
- **来源**：https://github.com/PleasePrompto/notebooklm-skill
- **文件**：[SKILL.md](notebooklm/SKILL.md) | [README.md](notebooklm/README.md) | [AUTHENTICATION.md](notebooklm/AUTHENTICATION.md)

---

### 13. **ppt-generator** ⭐⭐⭐ 新安装
**NanoBanana PPT Skills - AI 驱动 PPT 生成器**

- **用途**：基于 AI 自动生成高质量 PPT 图片和视频，支持智能转场和交互式播放
- **特点**：
  - 🤖 智能文档分析 - 自动提取核心要点，规划 PPT 内容结构
  - 🎨 多风格支持 - 渐变毛玻璃、矢量插画、3D 粘土拟人、黑金奢华、东方美学、硅谷创投、极致科技等风格
  - 🖼️ 高质量图片 - 使用云雾 AI (Gemini 3 Pro) 生成 16:9 高清 PPT (2K/4K)
  - 🎬 AI 转场视频 - 使用 Veo 模型生成流畅的页面过渡动画
  - 🎮 交互式播放器 - 视频+图片混合播放，支持键盘导航
  - 🎥 完整视频导出 - FFmpeg 合成包含所有转场的完整 PPT 视频
  - 📊 智能布局 - 封面页、内容页、数据页自动识别
- **依赖**：
  - Python 3.8+
  - google-genai, pillow, python-dotenv, requests
  - FFmpeg（视频功能需要）
- **环境变量**：
  - `YUNWU_API_KEY`（必需）- 云雾 AI API 密钥，用于生成 PPT 图片和视频
- **成本**：
  - 视频生成 (veo-3.1): 约 0.09 元/次
  - 图片生成 (nano-banana): 约 0.16 元/张
- **使用示例**：
  - `/ppt-generator-pro`
  - "基于以下文档生成一个 5 页的 PPT，使用渐变毛玻璃风格"
  - "生成一个关于 AI 产品设计的 PPT，包含封面、内容、数据页"
- **最新更新**：v2.0.0 - 2026-01-11
  - ✅ 新增 Veo 模型转场视频生成
  - ✅ 交互式视频播放器（视频+图片混合）
  - ✅ FFmpeg 完整视频合成
  - ✅ 首页循环预览视频
- **来源**：https://github.com/xj-bear/NanoBanana-PPT-Skills
- **文件**：[SKILL.md](ppt-generator/SKILL.md) | [README.md](ppt-generator/README.md)

---

### 15. **all-2md** ⭐⭐⭐ 新安装
**All-2-MD - 全格式文档转换器**

- **用途**：将各种文档格式转换为 Markdown（PDF、Word、PPT、Excel、HTML、图片 OCR、音频等）
- **特点**：
  - 📄 多格式支持 - PDF、DOCX、PPTX、XLSX、HTML、图片、音频、ZIP
  - 🔍 OCR 图片识别 - 从扫描 PDF、截图中提取文字
  - 📊 表格保留 - 保留 PDF 和文档中的表格结构
  - 🎯 代码块识别 - 自动识别并保留代码块格式
  - 🚀 简单易用 - 命令行或通过 Claude Code 直接调用
  - ✅ 已测试格式 - HTML、DOCX、XLSX、PPTX 全部测试通过
- **依赖**：
  - Python 3.9+
  - markitdown (微软官方开源包)
  - python-docx (Word 支持)
  - openpyxl (Excel 支持)
  - python-pptx (PowerPoint 支持)
- **使用示例**：
  - "把这个文件转换成 Markdown: path/to/file.pdf"
  - "使用 all-2-md skill 转换这个文档: path/to/document.docx"
  - `/all-2md document.pdf`
- **命令行使用**：
  ```bash
  # 直接使用 markitdown 命令
  markitdown path/to/document.pdf
  markitdown path/to/document.pdf -o output.md

  # 使用辅助脚本
  python convert.py document.pdf output.md
  ```
- **测试结果**：
  - ✅ HTML - 转换正常，保留结构和格式
  - ✅ DOCX - 转换正常，保留表格和列表
  - ✅ XLSX - 转换正常，表格转 Markdown 表格
  - ✅ PPTX - 转换正常，按幻灯片分离
- **技术信息**：
  - **工具**: 微软开源 [MarkItDown](https://github.com/microsoft/markitdown)
  - **Python 包**: markitdown
  - **版本**: 0.0.2
- **最新更新**：v2.0 - 2026-01-22
  - ✅ 重命名为 all-2md
  - ✅ 完整测试 HTML、DOCX、XLSX、PPTX 格式
  - ✅ 更新文档和测试用例
- **来源**: 微软官方开源
- **文件**：[SKILL.md](all-2md/SKILL.md) | [README.md](all-2md/README.md) | [convert.py](all-2md/convert.py) | [tests/](all-2md/tests/)

---

### 16. **document-illustrator** ⭐⭐ 新安装
**Document Illustrator - 文档配图生成器**

- **用途**：基于 AI 智能分析的文档配图生成工具，自动理解文档内容并生成专业配图
- **特点**：
  - 🤖 AI 智能归纳 - 自动理解文档内容，智能提取核心主题
  - 📝 格式无关 - 支持任何格式的文档（Markdown、纯文本、PDF 等）
  - 🎨 三种风格 - 渐变玻璃卡片、票据风格、矢量插画
  - 📐 灵活比例 - 支持 16:9（横屏）和 3:4（竖屏）
  - 🖼️ 封面图可选 - 可生成概括全文的封面图作为系列配图的引导
  - ✅ 内容完整 - 展示归纳结果供确认，确保所有重要信息都被包含
- **依赖**：
  - Python 3.8+
  - google-genai, pillow, python-dotenv
- **环境变量**：
  - `GEMINI_API_KEY`（必需）- Gemini API 密钥，获取地址：https://makersuite.google.com/app/apikey
- **使用示例**：
  - "帮我为这个文档生成配图：/path/to/document.md"
  - "我想为这篇文章生成一些配图"
  - "为 ~/blog/my-article.md 生成配图，使用票据风格"
- **工作流程**：
  1. Claude 读取并理解文档
  2. 询问图片比例（16:9 / 3:4）
  3. 询问是否生成封面图
  4. 询问内容配图数量（3-10 张）
  5. Claude 智能归纳内容并展示确认
  6. 生成配图并保存
- **最新更新**：v1.0
- **来源**：https://github.com/op7418/Document-illustrator-skill
- **文件**：[SKILL.md](document-illustrator/SKILL.md) | [README.md](document-illustrator/README.md)

---

### 14. **ms-image** ⭐
**ModelScope 免费AI绘图**

- **用途**：使用ModelScope API免费生成AI图片
- **特点**：
  - 每天免费2000张图片额度
  - 使用通义千问Turbo模型（快速生成）
  - 异步任务处理
  - 支持自定义输出路径
  - 高质量图片输出
- **依赖**：
  - Python 3.9+
  - requests, pillow
- **使用示例**：
  - "帮我生成一张图片，内容是'一只金色的猫'"
  - "用AI画一个赛博朋克风格的城市"
  - "生成图片：美丽的日落风景"
- **命令行使用**：
  ```bash
  python scripts/ms_image_generator.py "A golden cat"
  python scripts/ms_cli.py "A beautiful sunset" sunset.jpg
  ```
- **API Key**：内置（ms-51dd7494-0706-45d9-a901-c395522c55f2）
- **最新更新**：v1.0 - 2025-01-15
- **文件**：[SKILL.md](ms-image/SKILL.md) | [README.md](ms-image/README.md)

---

### 17. **baoyu-skills** ⭐⭐⭐ 新安装
**Baoyu 内容创作技能包**

- **来源**：https://github.com/JimLiu/baoyu-skills
- **位置**：`baoyu-skills/`
- **用途**：专业的AI内容创作和发布工具集，包含13个专业技能

#### 内容创作技能 (Content Skills)

| 技能 | 用途 | 命令 |
|------|------|------|
| **baoyu-xhs-images** | 小红书信息图生成（9种风格 × 6种布局） | `/baoyu-xhs-images article.md --style notion --layout dense` |
| **baoyu-infographic** | 专业信息图生成（20种布局 × 17种风格） | `/baoyu-infographic content.md --layout pyramid --style technical` |
| **baoyu-cover-image** | 文章封面图生成（21种风格） | `/baoyu-cover-image article.md --style warm` |
| **baoyu-slide-deck** | 演示文稿图片生成（16种风格） | `/baoyu-slide-deck article.md --style corporate` |
| **baoyu-comic** | 知识漫画创作器（8种风格） | `/baoyu-comic source.md --style ohmsha` |
| **baoyu-article-illustrator** | 文章智能插图生成（20种风格） | `/baoyu-article-illustrator article.md --style watercolor` |
| **baoyu-post-to-x** | 发布到 X (Twitter) | `/baoyu-post-to-x "Hello" --image photo.png` |
| **baoyu-post-to-wechat** | 发布到微信公众号 | `/baoyu-post-to-wechat 文章 --markdown article.md` |

#### AI生成技能 (AI Generation Skills)

| 技能 | 用途 | 命令 |
|------|------|------|
| **baoyu-image-gen** | AI图片生成（OpenAI/Google官方API） | `/baoyu-image-gen --prompt "A cat" --image cat.png --ar 16:9` |
| **baoyu-danger-gemini-web** | Gemini Web交互（需谨慎使用） | `/baoyu-danger-gemini-web "Hello Gemini"` |

#### 工具技能 (Utility Skills)

| 技能 | 用途 | 命令 |
|------|------|------|
| **baoyu-url-to-markdown** | URL转Markdown（Chrome CDP） | `/baoyu-url-to-markdown https://example.com` |
| **baoyu-danger-x-to-markdown** | X(Twitter)内容转Markdown | `/baoyu-danger-x-to-markdown https://x.com/user/status/123` |
| **baoyu-compress-image** | 图片压缩 | `/baoyu-compress-image image.png --quality 80` |

#### 环境变量配置

创建 `~/.baoyu-skills/.env`：
```bash
# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_IMAGE_MODEL=gpt-image-1.5

# Google
GOOGLE_API_KEY=xxx
GOOGLE_IMAGE_MODEL=gemini-3-pro-image-preview
```

#### 风格库

- **小红书风格**：cute, fresh, warm, bold, minimal, retro, pop, notion, chalkboard
- **信息图风格**：craft-handmade, claymation, kawaii, watercolor, chalkboard, cyberpunk-neon, corporate-memphis, technical-schematic
- **封面图风格**：elegant, blueprint, bold-editorial, chalkboard, dark-atmospheric, editorial-infographic, fantasy-animation, minimal, nature, notion, pixel-art, playful, retro, sketch-notes, vector-illustration, vintage, warm, watercolor
- **漫画风格**：classic, dramatic, warm, sepia, vibrant, ohmsha, realistic, wuxia, shoujo
- **文章插图风格**：notion, elegant, warm, minimal, playful, nature, sketch, watercolor, vintage, scientific, chalkboard, editorial, flat, flat-doodle, retro, blueprint, vector-illustration, sketch-notes, pixel-art, intuition-machine, fantasy-animation

#### 注意事项

- `baoyu-danger-gemini-web` 和 `baoyu-danger-x-to-markdown` 使用非官方API，使用需自负风险
- 首次使用需配置环境变量
- 支持通过 `EXTEND.md` 自定义风格和配置

**文件**：[README.md](baoyu-skills/README.md) | [CLAUDE.md](baoyu-skills/CLAUDE.md)

---

### 18. **Khazix-Skills** ⭐⭐⭐ 新安装
**Khazix 技能管理系统**

- **来源**：https://github.com/KKKKhazix/Khazix-Skills
- **位置**：`Khazix-Skills/`
- **用途**：完整的 AI 技能生命周期管理系统 - 从创建、维护到持续进化
- **依赖**：Python 3.8+, Git, PyYAML

#### 核心技能

| 技能 | 用途 | 命令 |
|------|------|------|
| **github-to-skills** | 自动将 GitHub 仓库转换为 AI skills | `/github-to-skills <url>` 或 "Package this repo: <url>" |
| **skill-manager** | 管理技能生命周期（检查更新、列表、删除） | `/skill-manager check` / `/skill-manager list` / `/skill-manager delete <name>` |
| **skill-evolution-manager** | 基于用户反馈持续进化技能 | `/evolve` 或 "复盘一下刚才的对话" |

#### 完整工作流

**1. 创建阶段 (github-to-skills)**
- 自动获取仓库元数据（README、最新 commit hash）
- 生成标准化技能目录结构
- 创建扩展 frontmatter（用于生命周期管理）
- 生成工具调用包装脚本

**2. 维护阶段 (skill-manager)**
- 扫描本地技能文件夹中的 GitHub-based skills
- 对比本地和远程 commit hash 检测更新
- 生成状态报告（Stale/Current）
- 引导式升级工作流
- 列表和删除管理

**3. 进化阶段 (skill-evolution-manager)**
- 复盘诊断：分析对话中技能表现
- 经验提取：将反馈转化为结构化 JSON
- 智能缝合：自动写入 SKILL.md 持久化
- 跨版本对齐：更新后经验不丢失

#### 核心脚本

| 脚本 | 用途 |
|------|------|
| `fetch_github_info.py` | 获取仓库信息（README, Hash, Tags） |
| `create_github_skill.py` | 生成技能目录和初始文件 |
| `scan_and_check.py` | 扫描并检查远程版本 |
| `update_helper.py` | 更新前备份文件 |
| `list_skills.py` | 列出所有已安装技能 |
| `delete_skill.py` | 永久删除技能 |
| `merge_evolution.py` | 增量合并经验数据 |
| `smart_stitch.py` | 生成/更新 SKILL.md 最佳实践章节 |
| `align_all.py` | 批量重缝合所有技能经验 |

#### 元数据标准

每个由 github-to-skills 创建的技能必须包含：
```yaml
---
name: <kebab-case-repo-name>
description: <concise-description>
github_url: <original-repo-url>
github_hash: <latest-commit-hash>
version: <tag-or-0.1.0>
created_at: <ISO-8601-date>
entry_point: scripts/wrapper.py
dependencies: [list-of-dependencies]
---
```

#### 使用示例

```bash
# 创建新技能
/github-to-skills https://github.com/yt-dlp/yt-dlp

# 检查更新
/skill-manager check

# 列出所有技能
/skill-manager list

# 复盘并进化技能
/evolve

# 删除技能
/skill-manager delete yt-dlp
```

#### 最佳实践

- **隔离性**：生成的技能应安装自己的依赖或清晰声明
- **渐进式披露**：不要将整个仓库放入技能，只包含必要的包装代码
- **幂等性**：`github_hash` 允许 skill-manager 检测 `remote_hash != local_hash`
- **不直接修改 SKILL.md**：通过 `evolution.json` 通道进行经验修正

#### 理念

```
+------------------+     +----------------+     +------------------------+
| github-to-skills | --> | skill-manager  | --> | skill-evolution-manager|
+------------------+     +----------------+     +------------------------+
        |                       |                         |
    Create new             Maintain &                 Evolve &
    skills from            update skills              improve based
    GitHub repos                                      on feedback
```

**文件**：[README.md](Khazix-Skills/README.md) | [github-to-skills](Khazix-Skills/github-to-skills/SKILL.md) | [skill-manager](Khazix-Skills/skill-manager/SKILL.md) | [skill-evolution-manager](Khazix-Skills/skill-evolution-manager/SKILL.md)

---

## 🔧 开发中/实验性技能

### mcp-chrome
**MCP Chrome 集成**

- **用途**：Chrome 浏览器 MCP 服务器
- **状态**：开发中
- **文件**：[mcp-chrome](mcp-chrome/)

---

## 📚 技能集合目录

### anthropic-skills
**Anthropic 官方技能集合**

包含官方示例技能：
- algorithmic-art
- brand-guidelines
- canvas-design
- doc-coauthoring
- docx
- frontend-design
- internal-comms
- pdf
- slack-gif-creator
- theme-factory
- web-artifacts-builder
- xlsx

---

### awesomeAgentskills
**精选第三方技能集合**

包含：
- deploying-to-production
- doc-sync-tool
- google-official-seo-guide
- internationalizing-websites
- shipany

---

## ⚡ Superpowers 技能集合

**完整的软件开发工作流系统**

由 [obra/superpowers](https://github.com/obra/superpowers) 提供的一套完整的软件开发工作流技能。

### 核心工作流

1. **brainstorming** 💡 - 交互式设计优化
   - 苏格拉底式提问完善想法
   - 探索多种方案并权衡
   - 分段呈现设计以验证

2. **using-git-worktrees** 🌳 - Git 工作树管理
   - 创建隔离的工作空间
   - 并行开发分支管理
   - 项目设置和基线验证

3. **writing-plans** 📋 - 详细实施计划
   - 将工作分解为 2-5 分钟的小任务
   - 每个任务包含精确的文件路径和代码
   - 完整的验证步骤

4. **subagent-driven-development** 🤖 - 子代理驱动开发
   - 为每个任务派发独立子代理
   - 两阶段审查（规范符合性 + 代码质量）
   - 快速迭代

5. **test-driven-development** 🧪 - 测试驱动开发
   - 强制 RED-GREEN-REFACTOR 循环
   - 先写测试,看它失败
   - 编写最小代码,看它通过
   - 重构优化

6. **requesting-code-review** 👀 - 代码审查请求
   - 预审查清单
   - 按严重程度报告问题
   - 关键问题阻止进度

7. **finishing-a-development-branch** 🎯 - 完成开发分支
   - 验证测试
   - 合并/PR 决策工作流
   - 清理工作树

### 辅助技能

8. **executing-plans** ⚙️ - 批量执行计划
   - 带有人类检查点的批量执行
   - 适合已验证的计划

9. **dispatching-parallel-agents** 🔄 - 并发子代理
   - 并行处理独立任务
   - 提高效率

10. **receiving-code-review** 📝 - 响应代码审查
    - 处理反馈意见
    - 技术严谨性验证

11. **systematic-debugging** 🐛 - 系统化调试
    - 4 阶段根因分析过程
    - 条件等待技术
    - 防御深度

12. **verification-before-completion** ✅ - 完成前验证
    - 确保问题真正修复
    - 验证胜过声明

13. **writing-skills** ✍️ - 技能创建指南
    - 创建新技能的最佳实践
    - 测试方法学
    - 技能规范

14. **using-superpowers** 🚀 - Superpowers 使用指南
    - 技能系统介绍
    - 快速入门

### 理念

- **测试驱动开发** - 始终先写测试
- **系统化优于临时** - 流程优于猜测
- **降低复杂性** - 简单性是主要目标
- **证据优于声明** - 验证后再宣布成功

**来源**: https://github.com/obra/superpowers
**最新更新**: 2026-01-12 - 初始安装

---

## 🚀 如何使用技能

### 方式 1：直接调用
```
帮我写一篇关于 XXX 的公众号文章
```
如果匹配了写作 skill 的工作区，会自动激活

### 方式 2：明确指定
```
使用写作 skill 帮我...
```

### 方式 3：通过 slash 命令
```
/writing-workflow
```

---

## 📖 技能开发

如果你想让某个技能可用，确保：

1. **SKILL.md 文件存在** - 这是技能的主文件
2. **清晰的触发机制** - 在 SKILL.md 顶部定义何时激活
3. **README.md** - 提供快速入门指南
4. **examples.md** - 提供使用示例（可选）

---

## 🔗 相关资源

- **技能存储位置**：`D:\ProjectAI\CC\CC_record\skills\`
- **Claude 配置**：`C:\Users\RyanCh\.claude\`
- **项目文档**：[CLAUDE.md](../CLAUDE.md)

---

**提示**：写作 automation skill (writing-workflow) 刚刚升级了降 AI 味审校清单，现在包含了完整的三遍审校流程和详细的检查清单！
