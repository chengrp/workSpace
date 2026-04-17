---
name: image-assistant
description: 配图助手 - 将文章/内容转换为统一风格、少字高可读的 16:9 信息图生图提示词。先确定"需要几张图+每张讲什么"，再压缩文案与隐喻，最后输出可直接复制的生图提示词并迭代。⚠️ 包含 1 个强制停止点：阶段3.5风格选择，必须使用 AskUserQuestion 工具等待用户选择。Use when user asks to: (1) Create image prompts from content ("这段内容做个图", "配几张图", "给我出图提示词"), (2) Make text more visual and readable ("字太多不好看", "更趣味更好读"), (3) Generate infographics for presentations/slides, (4) Batch generate images from prompts. Supports 6 generation APIs (Google AI, Yunwu, ModelScope, OpenAI, APIMart) with intelligent routing and auto-fallback.
---

# 配图助手 (image-assistant)

将内容转换为统一风格、少字高可读的 16:9 信息图提示词。

---

## ⚠️ 执行前必读：强制停止协议

本技能包含 1 个强制停止点，AI 必须停止并使用 AskUserQuestion 工具等待用户选择：

| 停止点 | 阶段 | 操作 |
|--------|------|------|
| 🛑 停止点1 | 阶段3.5 风格选择 | 展示风格选项 → 立即停止 |

**违反协议后果：用户失去风格选择权，生成结果不符合预期。**

## 触发条件

使用此技能当用户：
- 请求为内容创建配图（"这段内容做个图"、"配几张图"、"出图提示词"）
- 需要改善文字可读性（"字太多不好看"、"更趣味更好读"）
- 需要为 PPT/演示文稿生成信息图
- 需要批量生图

## 快速开始

用户最小输入：
1. 要配图的内容
2. 使用场景（PPT 投影 / 手机 / 海报）
3. 受众（小白 / 从业者 / 老板 / 学生）
4. 偏好（少字清爽 vs 信息密度）

## 工作流程

按顺序执行以下阶段，每个阶段开始时告知用户当前阶段和输出物。

| 阶段 | 目标 | 停止点 | 参考 |
|------|------|--------|------|
| 1. 需求澄清 | 挖需求：内容/场景/受众/字多字少 | - | [references/workflows/01-brief.md](references/workflows/01-brief.md) |
| 2. 配图规划 | 拆内容→定图清单 | - | [references/workflows/02-plan.md](references/workflows/02-plan.md) |
| 3. 文案定稿 (Copy Spec) | 确定画面布局与"图上写什么" | 🛑 **必须等待** | [references/workflows/03-copy.md](references/workflows/03-copy.md) |
| 3.5 风格选择 | 选择视觉风格（17种选项） | 🛑 **必须等待** | 见下方"风格选择指南" |
| 4. 提示词封装 | 封装成可复制提示词 | - | [references/workflows/04-prompts.md](references/workflows/04-prompts.md) |
| 5. 迭代润色 | 减字、换隐喻、提可读性 | - | [references/workflows/05-iterate.md](references/workflows/05-iterate.md) |

### 阶段判断规则

- 还没讲清楚需求（内容+场景+受众）→ 阶段1
- 文章长、需拆块、需确定"几张图"→ 阶段2
- 已确认图清单，未确定"图上写什么"→ **阶段3** (必须展示 ASCII 布局并等待用户确认)
- 🛑 阶段3.5：已确认 Copy Spec，需选择风格 → 停止并等待用户选择
- Copy Spec 确认，要出可复制提示词→ 阶段4
- 用户反馈"字多/不好看"→ 阶段5

## 输出规范

- 每张图一个核心信息
- 中文清晰可读：大字号、少字短句
- 每张提示词独立代码块
- 默认 16:9 横版
- 风格由用户在阶段 3.5 选择（未指定则使用 craft-handmade）
- Copy Spec 确认后不得擅自改文案

---

## 风格选择指南

Copy Spec 确认后，进入阶段 3.5，必须停止并等待用户选择风格。

### 🛑 阶段 3.5：风格选择（强制停止点）

**17 种内置风格选项：**

| 风格 | 描述 | 适用场景 |
|-------|------|----------|
| `craft-handmade` | 手工风 - 手绘插图、纸质工艺美学（默认推荐）| 通用、科普、生活方式 |
| `claymation` | 粘土动画 - 3D 粘土人偶、定格动画风格 | 趣味、儿童教育 |
| `kawaii` | 日系可爱 - 大眼睛、柔和色调、日式可爱 | 生活方式、轻松话题 |
| `storybook-watercolor` | 故事书水彩 - 柔和绘画插图、奇幻风格 | 童话、故事叙述 |
| `chalkboard` | 黑板风 - 彩色粉笔、黑色背景 | 教育、知识分享 |
| `cyberpunk-neon` | 赛博朋克霓虹 - 深色背景、霓虹光效、未来感 | 科技、未来主题 |
| `bold-graphic` | 粗体漫画风 - 半调网点、高对比度 | 漫画、视觉冲击 |
| `aged-academia` | 古老学术风 - 复古科学、棕褐色草图 | 历史、学术、复古 |
| `corporate-memphis` | 企业孟菲斯 - 扁平矢量人物、鲜艳填充 | 商业、企业、PPT |
| `technical-schematic` | 技术示意图 - 蓝图、等轴 3D、工程风格 | 技术文档、系统架构 |
| `origami` | 折纸风 - 折叠纸艺、几何形态 | 极简、几何美学 |
| `pixel-art` | 像素风 - 复古 8 位、怀旧游戏 | 复古游戏、像素艺术 |
| `ui-wireframe` | UI 线框风 - 灰度方块、界面原型 | 产品设计、线框图 |
| `subway-map` | 地铁图风 - 交通线路图、彩色线条 | 路线图、流程图 |
| `ikea-manual` | 宜家手册风 - 极简线稿、组装说明风格 | 组装指南、说明书 |
| `knolling` | 平铺摆放风 - 有序平铺、俯视图 | 整理、归纳、展示 |
| `lego-brick` | 乐高砖块风 - 玩具砖块建造、趣味 | 趣味、模块化、建造 |

**🚨 停止并等待用户选择风格**
```
【停止并等待用户选择】
使用 AskUserQuestion 工具：
questions: [{
  question: "请选择配图风格：",
  header: "风格选择",
  options: [
    { label: "craft-handmade (推荐)", description: "手工风 - 手绘插图、纸质工艺美学，适合通用科普" },
    { label: "默认风格", description: "使用 style-block.md 的默认奶油纸+彩铅风格（快速）" },
    { label: "corporate-memphis", description: "企业孟菲斯 - 扁平矢量、鲜艳填充，适合商业PPT" },
    { label: "technical-schematic", description: "技术示意图 - 蓝图等轴3D，适合技术文档" },
    { label: "storybook-watercolor", description: "故事书水彩 - 柔和绘画，适合童话故事" },
    { label: "chalkboard", description: "黑板风 - 彩色粉笔黑色背景，适合教育内容" },
    { label: "kawaii", description: "日系可爱 - 大眼睛柔和色调，适合轻松话题" },
    { label: "cyberpunk-neon", description: "赛博朋克霓虹 - 深色霓虹光效，适合科技主题" },
    { label: "ikea-manual", description: "宜家手册风 - 极简线稿组装，适合说明书" },
    { label: "pixel-art", description: "像素风 - 复古8位怀旧，适合复古主题" },
    { label: "bold-graphic", description: "粗体漫画风 - 半调网点高对比，适合视觉冲击" }
  ],
  multiSelect: false
}]
```

### 默认行为

**如果用户没有明确选择**（例如直接说"生成配图"、"继续"、或者在其他对话中已经选过风格）：
- 直接应用 `templates/style-block.md` 的默认风格（奶油纸底 + 彩铅水彩手绘 + 轻涂鸦）
- 不再重复询问，直接进入阶段 4

**设计理念**：减少重复确认，提升流畅体验。用户如需选择其他风格时，会在阶段 1 需求澄清时主动说明。

## 生图方式

阶段4提示词封装后，提供生图方式选择：

| 方式 | 特点 | 适用场景 |
|------|------|----------|
| **all-image skill** | ⭐ 推荐 - 智能路由+自动降级 | 一键生图，自动选择最优API |
| **云雾 API** | 快速响应 | 需要快速出图 |
| **Google AI** | 最高质量，4K，图生图 | 高质量需求 |
| **ModelScope** | 免费 2000张/天 | 批量免费 |
| **OpenAI** | DALL-E 3 | OpenAI 用户 |
| **APIMart** | 批量异步 | 大批量任务 |

详细信息：[references/templates/api-comparison.md](references/templates/api-comparison.md)

## 模板

默认使用风格模板：[references/templates/style-block.md](references/templates/style-block.md)

可用布局模板：
- [16x9-infographic.md](references/templates/16x9-infographic.md) - 信息图
- [16x9-3cards-insights.md](references/templates/16x9-3cards-insights.md) - 三卡片洞察
- [16x9-contrast-2cards.md](references/templates/16x9-contrast-2cards.md) - 双卡对比
- [16x9-cover-roadmap.md](references/templates/16x9-cover-roadmap.md) - 封面路线图
- [16x9-5panel-comic.md](references/templates/16x9-5panel-comic.md) - 五格漫画

## Scripts

- [scripts/banana-mcp/google_image_mcp.py](scripts/banana-mcp/google_image_mcp.py) - Google Image MCP 服务器
- [scripts/apimart_batch_generate.py](scripts/apimart_batch_generate.py) - APIMart 批量生图脚本
