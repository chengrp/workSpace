# 完整生图方式清单

## 一、底层 API 层（生图服务）

### 1. 云雾 API (yunwu.ai)
- **模型**: Gemini 2.5 Flash Image Preview
- **端点**: `https://yunwu.ai/v1beta/models/gemini-2.5-flash-image-preview:generateContent`
- **认证**: URL 参数 `?key=`
- **格式**: Gemini 原生格式
- **响应**: 同步返回 base64
- **特点**: 速度快（5-10秒），质量高
- **环境变量**: `YUNWU_API_KEY`

### 2. Google AI Studio (官方) ⭐ 首选
- **模型**: Gemini 2.5 Flash / Gemini 3 Pro / Imagen 3
- **端点**: `https://generativelanguage.googleapis.com/v1beta/`
- **认证**: URL 参数 `?key=`
- **格式**: Gemini 或 OpenAI 兼容格式
- **响应**: 同步返回 base64
- **特点**:
  - ⭐ **质量最高**，官方支持
  - ✅ **支持文生图**（Text-to-Image）
  - ✅ **支持图生图**（Image-to-Image）
  - ✅ 支持多种分辨率（最高 4K）
  - ✅ Gemini 3 Pro 质量最佳
- **环境变量**: `GOOGLE_API_KEY`
- **分辨率设置**:
  - 标准：1024x1024, 1792x1024 (16:9), 1024x1792 (9:16)
  - 高质量：2048x2048, 3072x3072
  - 超高清：4096x4096 (**4K 推荐**)

### 3. ModelScope API
- **模型**: Tongyi-MAI/Z-Image-Turbo
- **端点**: `https://api-inference.modelscope.cn/v1/images/generations`
- **认证**: Bearer Token
- **格式**: OpenAI 格式
- **响应**: 异步 + 轮询，返回 URL
- **特点**: 免费额度 2000张/天，支持图生图
- **环境变量**: `MODELSCOPE_API_KEY`

### 4. OpenAI API
- **模型**: gpt-image-1.5
- **端点**: `https://api.openai.com/v1/images/generations`
- **认证**: Bearer Token
- **格式**: OpenAI 格式
- **响应**: 同步返回 URL
- **特点**: 质量高，DALL-E 系列
- **环境变量**: `OPENAI_API_KEY`

### 5. Gemini Web API (非官方)
- **模型**: Gemini (Web)
- **端点**: Gemini Web 接口
- **认证**: Cookie/Session
- **格式**: Web 请求格式
- **响应**: 同步返回
- **特点**: 免费使用，非官方，稳定性不确定
- **用途**: 作为其他技能的后端（baoyu-danger-gemini-web）

### 6. APIMart (第三方聚合)
- **模型**: Gemini 3 Pro / 多模型
- **端点**: `https://api.apimart.ai/v1/images/generations`
- **认证**: Bearer Token
- **格式**: 自定义格式
- **响应**: 异步 + 轮询
- **特点**: 第三方服务，支持批量
- **环境变量**: `APIMART_TOKEN`

---

## 二、封装/工具层（调用接口）

### 1. banana-mcp
- **位置**: `image-assistant/banana-mcp/`
- **协议**: MCP (Model Context Protocol)
- **底层 API**: Google AI Studio
- **支持**: Gemini 3 Pro, Imagen 3
- **调用方式**: Claude Code 工具调用
- **特点**: MCP 协议，Claude Code 原生支持
- **配置**: `.mcp.json`

### 2. ms-image skill
- **位置**: `CC_record/skills/ms-image/`
- **底层 API**: ModelScope API
- **支持**: 文生图、图生图
- **调用方式**: 命令行 / Python
- **特点**: 独立 skill，免费额度
- **配置**: 内置 API Key 或环境变量

### 3. baoyu-image-gen
- **位置**: `baoyu-skills/skills/baoyu-image-gen/`
- **底层 API**: OpenAI / Google AI
- **支持**: 多 provider 自动选择
- **调用方式**: Bun 命令行
- **特点**: AI SDK 封装，支持参考图
- **配置**: `~/.baoyu-skills/.env`

### 4. baoyu-danger-gemini-web
- **位置**: `baoyu-skills/skills/baoyu-danger-gemini-web/`
- **底层 API**: Gemini Web
- **支持**: 文本生成、图片生成
- **调用方式**: TypeScript
- **特点**: 非官方免费 API
- **配置**: 需要同意免责声明

---

## 三、应用层（场景技能）

### 1. baoyu-xhs-images
- **用途**: 小红书配图生成
- **底层 API**: 云雾 API (优先) → ModelScope (降级)
- **特点**: 自动降级策略，水印支持
- **位置**: `baoyu-skills/skills/baoyu-xhs-images/`

### 2. baoyu-infographic
- **用途**: 信息图生成
- **底层 API**: 通过 baoyu-danger-gemini-web
- **特点**: 20 种布局 × 17 种风格
- **位置**: `baoyu-skills/skills/baoyu-infographic/`

### 3. baoyu-cover-image
- **用途**: 文章封面图生成
- **底层 API**: 通过 baoyu-danger-gemini-web
- **特点**: 多种封面风格
- **位置**: `baoyu-skills/skills/baoyu-cover-image/`

### 4. baoyu-comic
- **用途**: 知识漫画生成
- **底层 API**: 通过 baoyu-danger-gemini-web
- **特点**: 多格漫画布局
- **位置**: `baoyu-skills/skills/baoyu-comic/`

### 5. baoyu-article-illustrator
- **用途**: 文章插图生成
- **底层 API**: 云雾 API → ModelScope
- **特点**: 基于文章内容自动生成
- **位置**: `baoyu-skills/skills/baoyu-article-illustrator/`

---

## 四、快速参考对比表

| 方式 | 速度 | 质量 | 成本 | 类型 | 推荐场景 |
|------|------|------|------|------|----------|
| **Google AI** ⭐ | ⚡⚡ | ★★★★★ | 按量 | 底层 API | **首选**，最高质量，支持4K、图生图 |
| **云雾 API** | ⚡⚡⚡ | ★★★★ | 按量 | 底层 API | 快速生成，高质量兜底 |
| **ModelScope** | ⚡⚡ | ★★★☆ | 2000免费/天 | 底层 API | 批量免费 |
| **OpenAI** | ⚡⚡ | ★★★★★ | 按量 | 底层 API | DALL-E 需求 |
| **Gemini Web** | ⚡⚡ | ★★★☆ | 免费 | 底层 API | 测试/学习 |
| **APIMart** | ⚡⚡ | ★★★★ | 按量 | 底层 API | 批量处理 |
| **banana-mcp** | ⚡⚡ | ★★★★★ | 按量 | MCP 封装 | Claude Code 调用 |
| **ms-image** | ⚡⚡ | ★★★☆ | 免费 | skill 封装 | 独立使用 |
| **baoyu-image-gen** | ⚡⚡ | ★★★★★ | 按量 | CLI 工具 | Bun 项目 |

---

## 五、选择决策树

```
开始
│
├─ ⭐ 首选：Google AI (Gemini 3 Pro / Imagen 3)
│  ├─ 最高质量，支持 4K 分辨率
│  ├─ 支持文生图 + 图生图
│  └─ banana-mcp (MCP 协议)
│
├─ 兜底：云雾 API (Gemini 2.5 Flash)
│  ├─ 速度快，高质量
│  └─ 成本优化
│
├─ 需要免费大量生成？
│  └─ 是 → ModelScope API (2000/天) 或 ms-image
│
├─ 需要 DALL-E？
│  └─ 是 → OpenAI API
│
├─ 需要图生图？
│  ├─ Google AI ✅ (首选)
│  └─ ModelScope ✅ (备选)
│
└─ 小红书/信息图/漫画等特定场景？
   └─ 是 → 对应的 baoyu-* 技能
```

---

## 六、环境变量汇总

```bash
# ~/.baoyu-skills/.env 或项目 .env

# === Google AI Studio (⭐ 首选) ===
# 获取方式：https://ai.google.dev/
GOOGLE_API_KEY=your_google_api_key
GOOGLE_IMAGE_MODEL=gemini-3-pro-image-preview  # 或 imagen-3.0-generate-001
GOOGLE_BASE_URL=https://generativelanguage.googleapis.com/v1beta

# === 云雾 API (兜底，速度快) ===
# 获取方式：云雾官网
YUNWU_API_KEY=your_yunwu_api_key

# === OpenAI (可选) ===
OPENAI_API_KEY=sk-xxx
OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_BASE_URL=https://api.openai.com/v1

# === ModelScope (有免费额度) ===
MODELSCOPE_API_KEY=ms-your-key-here

# === APIMart (可选) ===
APIMART_TOKEN=your_apimart_token
```

**推荐配置优先级：**
1. **GOOGLE_API_KEY** ⭐ (必须) - 最高质量，支持 4K、图生图
2. **YUNWU_API_KEY** (推荐) - 快速兜底
3. **MODELSCOPE_API_KEY** (可选) - 免费批量生成

---

## 七、文件位置索引

### image-assistant 技能
```
image-assistant/
├── banana-mcp/                    # MCP 封装
│   └── google_image_mcp.py
├── scripts/                       # 批量脚本
│   └── apimart_batch_generate.py
└── templates/
    ├── yunwu-api.md              # 云雾 API 文档
    └── api-comparison.md         # API 对比分析
```

### 独立 skills
```
CC_record/skills/
└── ms-image/                      # ModelScope 独立 skill
    └── scripts/ms_image_generator.py
```

### baoyu-skills 包
```
baoyu-skills/skills/
├── baoyu-image-gen/              # 通用生图 (OpenAI/Google)
├── baoyu-danger-gemini-web/       # Gemini Web 封装
├── baoyu-xhs-images/             # 小红书图片 (云雾+ModelScope)
├── baoyu-infographic/            # 信息图
├── baoyu-cover-image/            # 封面图
├── baoyu-comic/                  # 漫画
└── baoyu-article-illustrator/    # 文章插图
```
