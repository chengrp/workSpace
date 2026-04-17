# 云雾 API (Yunwu) 生图方式

## 概述

云雾 API 是一个高性能的图像生成服务，使用 Google Gemini 2.5 Flash 模型。

**特点：**
- 响应速度快（Flash 模型）
- 质量高（Gemini 系列）
- 支持 base64 返回
- 可作为首选方案，失败自动降级到 ModelScope

## 配置

### 环境变量

```bash
# 在 ~/.baoyu-skills/.env 或 .env 中配置
YUNWU_API_KEY=<your_api_key>
```

### 获取 API Key

访问云雾官网注册并获取 API Key。

## API 端点

```
https://yunwu.ai/v1beta/models/gemini-2.5-flash-image-preview:generateContent
```

## 使用方式

### JavaScript/TypeScript (Bun)

```typescript
async function generateWithYunwu(prompt, outputPath) {
  const YUNWU_API_KEY = process.env.YUNWU_API_KEY;
  const YUNWU_MODEL = 'gemini-2.5-flash-image-preview';

  const requestBody = {
    contents: [{
      role: "user",
      parts: [{ text: prompt }]
    }],
    generationConfig: {
      responseModalities: ["IMAGE", "TEXT"]
    }
  };

  const url = `https://yunwu.ai/v1beta/models/${YUNWU_MODEL}:generateContent?key=${YUNWU_API_KEY}`;

  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(requestBody)
  });

  const result = await response.json();
  const base64Data = result.candidates?.[0]?.content?.parts?.[0]?.inlineData?.data;

  if (base64Data) {
    const buffer = Buffer.from(base64Data, 'base64');
    await Bun.write(outputPath, buffer);
    return { success: true, provider: 'yunwu' };
  }
  return { success: false };
}
```

### Python

```python
import os
import base64
import urllib.request
import json

def generate_with_yunwu(prompt: str, output_path: str) -> bool:
    """使用云雾 API 生成图片"""
    api_key = os.environ.get("YUNWU_API_KEY")
    if not api_key:
        raise ValueError("YUNWU_API_KEY 环境变量未设置")

    model = "gemini-2.5-flash-image-preview"
    url = f"https://yunwu.ai/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"]
        }
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    base64_data = (result.get("candidates", [{}])[0]
                           .get("content", {})
                           .get("parts", [{}])[0]
                           .get("inlineData", {})
                           .get("data"))

    if base64_data:
        image_data = base64.b64decode(base64_data)
        Path(output_path).write_bytes(image_data)
        return True
    return False
```

## 自动降级策略

优先使用云雾 API，失败时自动降级到 ModelScope：

```typescript
// 优先云雾
const yunwuResult = await generateWithYunwu(prompt, outputPath);
if (yunwuResult.success) {
  console.log('✓ 使用云雾 API 生成');
} else {
  console.log('⚠️ 云雾 API 不可用，降级到 ModelScope...');
  await generateWithModelScope(prompt, outputPath);
}
```

## 与其他 API 对比

| 特性 | 云雾 API | Google AI | ModelScope |
|------|----------|-----------|------------|
| 模型 | Gemini 2.5 Flash | Gemini 3 Pro | 多模型 |
| 速度 | 快 | 中等 | 中等 |
| 质量 | 高 | 高 | 中高 |
| 成本 | 按使用量 | 按使用量 | 免费额度 |
| 稳定性 | 高 | 高 | 高 |
| 推荐用途 | 首选 | 备选 | 备选 |

## 提示词建议

云雾 API 使用 Gemini 模型，提示词建议：

- **明确风格**：`扁平插画风`、`手绘风`、`科技风`
- **指定尺寸**：在提示词中添加 `16:9`、`9:16`、`1:1`
- **强调中文可读性**：`中文必须清晰可读，大字号`
- **避免密集文字**：`留白充足，避免密集小字`

## 故障排除

### 错误：401 Unauthorized

- 检查 `YUNWU_API_KEY` 是否正确
- 确认 API Key 是否有效

### 错误：429 Rate Limit

- 降低请求频率
- 添加延迟重试机制

### 错误：未返回图片

- 检查提示词是否符合内容政策
- 尝试简化提示词
- 启用降级到 ModelScope
