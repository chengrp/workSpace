# all-image - 统一生图工具

> 智能路由 + 自动降级 + 自适应修复

**all-image** 是一个高度封装的生图工具，为其他 skill 提供简单、可靠、智能的图片生成能力。

## 核心特性

- 🚀 **极简调用** - 一行代码生成图片
- 🧠 **智能路由** - 自动选择最优 API
- 🔄 **自动降级** - API 失败自动切换
- 🛡️ **自适应修复** - 自动修复常见错误
- 📊 **详细报错** - 友好的错误信息和恢复建议
- ⚡ **高性能** - 支持批量生成和缓存

## 快速开始

### 安装

```bash
# 确保已安装 Python 3.8+
pip install -r requirements.txt
```

### 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的 API Key
# 至少配置一个 Provider（推荐 Google AI）
```

### 基础使用

```python
from all_image import ImageGenerator

# 初始化
gen = ImageGenerator()

# 极简调用
result = gen.generate("一只可爱的猫咪")

if result.success:
    print(f"✅ {result.image_path}")
else:
    print(f"❌ {result.error}")
    print(f"💡 {result.suggestions}")
```

## 支持的 API

| API | 优先级 | 质量 | 速度 | 特点 |
|-----|--------|------|------|------|
| **Google AI** | ⭐ 首选 | ★★★★★ | 10-20s | 最高质量，支持 4K、图生图 |
| **云雾 API** | 兜底 | ★★★★☆ | 5-10s | 快速响应，高质量 |
| **ModelScope** | 免费兜底 | ★★★☆☆ | 20-40s | 免费额度 2000张/天 |
| **OpenAI** | 备选 | ★★★★★ | 15-30s | DALL-E 3，高质量 |
| **APIMart** | 批量 | ★★★★☆ | 异步 | 第三方聚合，支持批量 |

## 参数说明

| 参数 | 类型 | 可选值 | 默认值 | 说明 |
|------|------|--------|--------|------|
| `prompt` | str | - | **必需** | 图片描述 |
| `ratio` | str | 16:9, 9:16, 1:1, 4:3, 3:4, 21:9, 3:2 | 16:9 | 宽高比 |
| `quality` | str | standard, high, 4k | high | 输出质量 |
| `mode` | str | auto, quality, speed, free | auto | API 选择策略 |
| `style` | str | 任意风格描述 | - | 可选风格 |
| `reference_image` | str | 文件路径或 base64 | - | 图生图参考图 |

## 高级功能

### 批量生成

```python
results = gen.generate_batch([
    {"prompt": "图1", "ratio": "16:9", "quality": "4k"},
    {"prompt": "图2", "ratio": "9:16", "quality": "high"},
    {"prompt": "图3", "ratio": "1:1", "quality": "standard"},
], max_concurrent=3)
```

### 图生图

```python
result = gen.generate(
    prompt="猫咪在草地上",
    reference_image="path/to/reference.jpg",
    ratio="16:9"
)
```

### 健康检查

```python
status = gen.check_provider_health()
# {
#     "google_ai": {"healthy": True, "status": "available"},
#     "yunwu": {"healthy": True, "status": "available"},
#     "modelscope": {"healthy": True, "status": "available"}
# }
```

## 错误处理

### 自动修复的问题

1. **提示词缺少尺寸** → 自动添加 "Aspect ratio: 16:9."
2. **敏感内容** → 自动过滤或重写
3. **API Key 无效** → 提示配置，自动降级
4. **网络超时** → 自动重试，切换 provider
5. **配额用尽** → 自动切换到其他 provider

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
```

## 在其他 skill 中使用

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

## 文件结构

```
all-image/
├── SKILL.md              # 技能文档（触发机制）
├── README.md             # 本文件
├── .env.example          # 配置模板
├── __init__.py           # 统一对外接口
├── core/
│   ├── __init__.py
│   ├── router.py         # 智能路由器
│   └── retry.py          # 自适应重试
├── providers/
│   ├── __init__.py
│   ├── base.py           # Provider 基类
│   ├── google_ai.py      # Google AI Provider
│   ├── yunwu.py          # 云雾 API Provider
│   └── modelscope.py     # ModelScope Provider
└── tests/
    └── test_all_image.py # 测试套件
```

## 开源协议

MIT License

---

**作者**: Claude Code
**版本**: 1.0.0
