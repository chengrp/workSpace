---
name: all-image
description: 统一生图工具 - 智能路由 + 自动降级 + 自适应修复。支持 6 种 API（Google AI/云雾/ModelScope/OpenAI/Gemini Web/APIMart），最高 4K 质量，支持文生图和图生图。其他 skill 可随时调用。
---

# all-image - 统一生图工具

## 概述

all-image 是一个高度封装的生图工具，为其他 skill 提供简单、可靠、智能的图片生成能力。

**核心特性：**
- 🚀 **极简调用** - 一行代码生成图片
- 🧠 **智能路由** - 自动选择最优 API
- 🔄 **自动降级** - API 失败自动切换
- 🛡️ **自适应修复** - 自动修复常见错误
- 📊 **详细报错** - 友好的错误信息和恢复建议
- ⚡ **高性能** - 支持批量生成和缓存

---

## 触发方式

### 对其他 skill 的调用方式

**Python 代码调用（推荐）：**
```python
from all_image import ImageGenerator

# 极简调用
gen = ImageGenerator()
result = gen.generate("一只可爱的猫咪")

# 完整参数
result = gen.generate(
    prompt="内容描述",
    ratio="16:9",
    quality="4k",
    mode="auto"  # 自动选择最优 API
)
```

**命令行调用：**
```bash
# 基础调用
python -m all_image --prompt "内容描述" --ratio 16:9

# 图生图
python -m all-image --prompt "猫咪在玩耍" --reference image.jpg

# 批量生成
python -m all-image --batch prompts.jsonl
```

**Claude Code 调用：**
```
用户："帮我生成一张配图"
助手：[自动调用 all-image skill]
```

---

## 快速使用

### 方式 1：Python 代码（推荐）

```python
from all_image import ImageGenerator

# 初始化（单例模式，自动复用连接）
gen = ImageGenerator()

# 文生图 - 极简
result = gen.generate("一只猫咪在玩耍")

# 文生图 - 完整参数
result = gen.generate(
    prompt="奶油纸底，彩铅手绘风格，一只可爱的猫咪",
    ratio="16:9",      # 16:9, 9:16, 1:1, 4:3, 3:4
    quality="4k",      # standard, high, 4k
    mode="auto",       # auto, quality, speed, free
    style="handdrawn"  # 可选风格
)

# 图生图
result = gen.generate(
    prompt="猫咪在草地上",
    reference_image="path/to/reference.jpg",
    ratio="16:9"
)

# 批量生成
results = gen.generate_batch([
    {"prompt": "图1", "ratio": "16:9"},
    {"prompt": "图2", "ratio": "9:16"},
    {"prompt": "图3", "ratio": "1:1"},
])

# 结果处理
if result.success:
    print(f"✅ 生成成功！使用 {result.provider}")
    print(f"图片路径: {result.image_path}")
    # result.base64 也可用
else:
    print(f"❌ 生成失败: {result.error}")
    print(f"💡 恢复建议: {result.suggestions}")
```

### 方式 2：函数式调用

```python
from all_image import generate_image

# 直接调用
result = generate_image(
    prompt="内容描述",
    ratio="16:9",
    quality="4k"
)

# 返回 ImageResult 对象
```

---

## 返回格式

### 成功返回

```python
ImageResult(
    success=True,
    provider="google_ai",           # 实际使用的 provider
    image_path="/path/to/image.png",  # 保存的图片路径
    base64="iVBORw0KGgoAAAANSUhEUgAA...", # base64 编码
    metadata={
        "model": "gemini-3-pro-image-preview",
        "resolution": "4096x4096",
        "generation_time": 12.5,
        "retries": 0,
        "fallback_used": False
    }
)
```

### 失败返回

```python
ImageResult(
    success=False,
    error="所有生图 API 均不可用",
    provider=None,
    image_path=None,
    base64=None,
    suggestions=[
        "检查网络连接",
        "验证 GOOGLE_API_KEY 是否正确",
        "尝试使用 ModelScope（免费额度）"
    ],
    attempted_providers=["google_ai", "yunwu", "modelscope"],
    error_details=[
        "google_ai: AuthenticationError - API Key 无效",
        "yunwu: ConnectionError - 网络超时",
        "modelscope: QuotaExceededError - 配额已用完"
    ]
)
```

---

## 智能路由规则

all-image 会根据以下规则自动选择最优 API：

| 需求 | 首选 | 备选 | 兜底 |
|------|------|------|------|
| **4K 质量** | Google AI (Gemini 3 Pro) | Google AI (Imagen) | - |
| **图生图** | Google AI | ModelScope | - |
| **快速生成** | 云雾 API | Google AI (Flash) | - |
| **免费生成** | ModelScope | - | - |
| **DALL-E** | OpenAI | - | - |

**mode 参数详解：**
- `auto` - 自动选择（默认）
- `quality` - 质量优先（Google AI）
- `speed` - 速度优先（云雾 API）
- `free` - 成本优先（ModelScope）

---

## 支持的参数

| 参数 | 类型 | 可选值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `prompt` | str | - | **必需** | 图片描述 |
| `ratio` | str | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 3:2 | 16:9 | 宽高比 |
| `quality` | str | standard, high, 4k | high | 输出质量 |
| `mode` | str | auto, quality, speed, free | auto | API 选择策略 |
| `style` | str | 任意风格描述 | - | 可选风格 |
| `reference_image` | str | 文件路径或 base64 | - | 图生图参考图 |
| `output_path` | str | 文件路径 | 自动生成 | 输出路径 |

---

## 错误处理和自适应修复

### 🔒 Provider 切换确认机制（安全特性）

**重要**：为了防止意外使用非预期的生图 API，系统默认在切换到非首选 Provider 时需要用户确认。

#### 确认规则

| 模式 | 首选 Provider | 切换到其他 Provider |
|------|--------------|-------------------|
| **auto** | Google AI | ⚠️ **需要用户确认** |
| **quality** | Google AI | ⚠️ **需要用户确认** |
| **speed** | 云雾 API | ⚠️ **需要用户确认** |
| **free** | ModelScope | ⚠️ **需要用户确认** |

#### 确认机制示例

```python
from all_image import ImageGenerator, ProviderConfirmationRequired

gen = ImageGenerator(auto_fallback=False)  # 默认需要确认

try:
    result = gen.generate("一只可爱的猫咪")
except ProviderConfirmationRequired as e:
    print(f"⚠️ {e}")
    print(f"建议 Provider: {e.decision.provider.name}")
    print(f"原因: {e.decision.reason}")
    print(f"优先级: {e.decision.priority}")

    # 用户确认后继续
    confirm = input("是否继续？(y/n): ")
    if confirm.lower() == 'y':
        result = gen.generate("一只可爱的猫咪", auto_fallback=True)
```

#### 禁用确认（自动降级）

如果希望自动降级而不需要确认：

```python
# 方式 1: 实例级别
gen = ImageGenerator(auto_fallback=True)
result = gen.generate("一只可爱的猫咪")

# 方式 2: 调用级别
gen = ImageGenerator()
result = gen.generate("一只可爱的猫咪", auto_fallback=True)
```

**⚠️ 注意**：禁用确认后，系统会自动在 Provider 之间切换，可能产生意外费用或使用非预期质量的 API。

### 自动修复的问题

1. **提示词缺少尺寸** → 自动添加 "Aspect ratio: 16:9."
2. **敏感内容** → 自动过滤或重写
3. **API Key 无效** → 提示配置，等待用户确认后降级
4. **网络超时** → 自动重试，切换 provider（需确认）
5. **配额用尽** → 提示切换，等待用户确认

### 错误报告示例

```
❌ 生成失败

尝试的 Provider:
  1. Google AI - AuthenticationError (API Key 无效)
  2. 云雾 API - ConnectionError (网络超时)
  3. ModelScope - QuotaExceededError (配额已用完)

💡 恢复建议:
  1. 检查网络连接
  2. 验证 GOOGLE_API_KEY 是否正确
  3. 考虑使用 ModelScope（免费额度）

📊 详细错误: 见 error_details 字段
```

---

## 高级功能

### 批量生成

```python
results = gen.generate_batch([
    {"prompt": "图1", "ratio": "16:9", "quality": "4k"},
    {"prompt": "图2", "ratio": "9:16", "quality": "high"},
    {"prompt": "图3", "ratio": "1:1", "quality": "standard"},
], max_concurrent=3)  # 并发数
```

### 缓存功能

```python
gen = ImageGenerator(enable_cache=True)

# 相同请求会返回缓存结果
result1 = gen.generate("一只猫咪")
result2 = gen.generate("一只猫咪")  # 返回缓存
```

### Provider 健康检查

```python
# 检查所有 provider 状态
status = gen.check_provider_health()
# {
#     "google_ai": {"healthy": true, "latency": 12.5},
#     "yunwu": {"healthy": false, "error": "timeout"},
#     "modelscope": {"healthy": true, "quota_remaining": 1500}
# }
```

---

## 环境变量配置

```bash
# ~/.baoyu-skills/.env 或项目 .env

# === Google AI (首选) ===
ALL_IMAGE_GOOGLE_API_KEY=your_google_api_key
ALL_IMAGE_GOOGLE_MODEL=gemini-3-pro-image-preview

# === 云雾 API (兜底) ===
ALL_IMAGE_YUNWU_API_KEY=your_yunwu_api_key

# === ModelScope (免费) ===
ALL_IMAGE_MODELSCOPE_API_KEY=ms-your-key-here

# === OpenAI (可选) ===
ALL_IMAGE_OPENAI_API_KEY=sk-your-key

# === 缓存配置 ===
ALL_IMAGE_CACHE_DIR=/tmp/all-image-cache
ALL_IMAGE_CACHE_TTL=3600
```

---

## 性能优化建议

1. **复用实例** - 使用单例模式，避免重复初始化
2. **批量生成** - 使用 `generate_batch()` 提高效率
3. **启用缓存** - 对相同提示词启用缓存
4. **合理并发** - 批量时设置 `max_concurrent=3`

---

## 调试和日志

### 启用调试日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)

gen = ImageGenerator(debug=True)
result = gen.generate("一只猫咪")
# 输出详细调试信息
```

### 日志输出示例

```
[all-image] [INFO] 2024-01-29 12:00:00 - 开始生成图片
[all-image] [INFO] 2024-01-29 12:00:00 - 智能路由选择: Google AI
[all-image] [INFO] 2024-01-29 12:00:01 - Google AI 生成成功 (12.5秒)
[all-image] [INFO] 2024-01-29 12:00:01 - 图片已保存: /tmp/image.png
```

---

## 文件结构

```
all-image/
├── SKILL.md              # 本文件
├── __init__.py           # 统一对外接口
├── core/
│   ├── __init__.py
│   ├── router.py         # 智能路由器
│   ├── fallback.py       # 降级策略
│   ├── retry.py          # 自适应重试
│   └── validator.py      # 参数验证
├── providers/
│   ├── __init__.py
│   ├── base.py           # Provider 基类
│   ├── google_ai.py      # Google AI Provider
│   ├── yunwu.py          # 云雾 API Provider
│   ├── modelscope.py     # ModelScope Provider
│   └── openai.py         # OpenAI Provider
├── utils/
│   ├── __init__.py
│   ├── config.py         # 配置管理
│   ├── logger.py         # 日志系统
│   └── cache.py          # 缓存工具
├── tests/
│   ├── __init__.py
│   └── test_all_image.py # 测试套件
├── .env.example          # 配置模板
└── README.md             # 使用说明
```

---

## 示例代码

### 示例 1：在其他 skill 中调用

```python
# 在你的 skill 中
from all_image import ImageGenerator

class MySkill:
    def __init__(self):
        self.image_gen = ImageGenerator()

    def create_illustration(self, content):
        result = self.image_gen.generate(
            prompt=content,
            ratio="16:9",
            quality="4k"
        )
        if result.success:
            return result.image_path
        else:
            raise Exception(f"生图失败: {result.error}")
```

### 示例 2：批量生成文章配图

```python
from all_image import ImageGenerator

gen = ImageGenerator()

articles = [
    {"title": "如何学习 Python", "prompt": "Python 代码编辑器界面"},
    {"title": "数据结构入门", "prompt": "二叉树示意图"},
    {"title": "机器学习基础", "prompt": "神经网络结构图"}
]

for article in articles:
    result = gen.generate(
        prompt=f"扁平插画风，{article['prompt']}",
        ratio="16:9",
        quality="high"
    )
    if result.success:
        print(f"✅ {article['title']} 配图生成成功")
```

---

## 更新日志

### v1.0.0 (2024-01-29)
- ✅ 首次发布
- ✅ 支持 4 种 API（Google AI / 云雾 / ModelScope / OpenAI）
- ✅ 智能路由和自动降级
- ✅ 自适应修复和错误处理
- ✅ 图生图支持
- ✅ 批量生成
- ✅ 缓存优化

---

## 相关文档

- [README.md](README.md) - 详细使用说明
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构设计
- [API.md](docs/API.md) - API 参考文档
