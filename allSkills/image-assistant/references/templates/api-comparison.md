# 生图 API 对比分析

## 一、API 调用差异对比

### 1. 请求格式对比

| API | 认证方式 | 请求头 | 请求体格式 | 参数传递方式 |
|-----|----------|--------|-----------|-------------|
| **云雾 API** | URL参数 `?key=` | `Content-Type: application/json` | Gemini格式 | JSON Body |
| **Google AI** | URL参数 `?key=` | `Content-Type: application/json` | Gemini/OpenAI格式 | JSON Body |
| **ModelScope** | Bearer Token | `Authorization: Bearer {key}`<br>`X-ModelScope-Async-Mode: true` | OpenAI格式 | JSON Body |
| **APIMart** | Bearer Token | `Authorization: Bearer {token}` | 自定义格式 | JSON Body |

---

### 2. 端点 URL 对比

| API | 基础URL | 模型路径 | 示例 |
|-----|---------|----------|------|
| **云雾 API** | `https://yunwu.ai/v1beta/models/` | `{model}:generateContent` | `gemini-2.5-flash-image-preview:generateContent` |
| **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/models/` | `{model}:generateContent` | `gemini-3-pro-image-preview:generateContent` |
| **Google Imagen** | `https://generativelanguage.googleapis.com/v1beta/openai/` | `images/generations` | - |
| **ModelScope** | `https://api-inference.modelscope.cn/v1/` | `images/generations` | - |
| **APIMart** | 自定义配置 | `images/generations` | - |

---

### 3. 请求体结构对比

#### 云雾 API / Google Gemini (相同格式)

```json
{
  "contents": [{
    "parts": [{
      "text": "图片生成提示词"
    }]
  }],
  "generationConfig": {
    "responseModalities": ["IMAGE", "TEXT"]
  }
}
```

**特点：**
- 使用 Gemini 原生格式
- `contents` 数组支持多轮对话
- `responseModalities` 控制返回类型

#### Google Imagen (OpenAI 兼容格式)

```json
{
  "model": "imagen-3.0-generate-001",
  "prompt": "图片生成提示词",
  "response_format": "b64_json",
  "n": 1
}
```

**特点：**
- OpenAI 兼容格式
- 更简洁的参数结构
- `response_format` 指定返回格式

#### ModelScope

```json
{
  "model": "Tongyi-MAI/Z-Image-Turbo",
  "prompt": "图片生成提示词",
  "size": "1024x1792"
}
```

**特点：**
- 异步任务模式
- `size` 参数格式为 "宽x高"
- 需要轮询获取结果

#### APIMart

```json
{
  "model": "gemini-3-pro-image-preview",
  "prompt": "图片生成提示词",
  "size": "16:9",
  "n": 1,
  "resolution": "2K"
}
```

**特点：**
- 自定义格式
- `size` 支持比例格式
- `resolution` 控制质量

---

### 4. 响应格式对比

#### 云雾 API / Google Gemini (同步返回)

```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "data": "base64编码的图片数据"
        }
      }]
    }
  }]
}
```

**提取路径：**
```
candidates[0].content.parts[0].inlineData.data
```

#### ModelScope (异步返回)

```json
// 提交任务返回
{
  "task_id": "12345"
}

// 轮询返回
{
  "task_status": "SUCCEED",
  "output_images": ["https://cdn.../image.jpg"]
}
```

**特点：**
- 需要两步：提交 + 轮询
- 返回图片 URL 而非 base64

---

## 二、参数要求差异

### 1. 尺寸参数对比

| API | 参数名 | 格式 | 示例 | 支持比例 |
|-----|--------|------|------|----------|
| **云雾 API** | prompt内嵌 | 文本描述 | "Aspect ratio: 16:9" | 任意 |
| **Google Gemini** | prompt内嵌 | 文本描述 | "Aspect ratio: 9:16" | 任意 |
| **Google Imagen** | aspectRatio | 比例字符串 | "16:9", "9:16", "1:1" | 预定义比例 |
| **ModelScope** | size | "宽x高" | "1024x1792" | 任意像素尺寸 |
| **APIMart** | size | 比例字符串 | "16:9" | 预定义比例 |

### 2. 常用尺寸映射

| 比例 | ModelScope size | ModelScope 实际像素 |
|------|-----------------|-------------------|
| 16:9 | 1792x1024 | 1792 × 1024 |
| 9:16 | 1024x1792 | 1024 × 1792 |
| 1:1 | 1536x1536 | 1536 × 1536 |
| 4:3 | 1536x1152 | 1536 × 1152 |

---

## 三、出图质量对比

### 1. 模型质量等级

| API | 模型 | 质量等级 | 适用场景 |
|-----|------|----------|----------|
| **云雾 API** | Gemini 2.5 Flash | ★★★☆☆ | 快速生成 |
| **Google Gemini** | Gemini 3 Pro | ★★★★★ | 高质量需求 |
| **Google Imagen** | Imagen 3.0 | ★★★★☆ | 专业用途 |
| **ModelScope** | Z-Image-Turbo | ★★★☆☆ | 快速批量 |
| **APIMart** | Gemini 3 Pro | ★★★★★ | 高质量需求 |

### 2. 响应速度对比

| API | 平均响应时间 | 模式 |
|-----|-------------|------|
| **云雾 API** | ~5-10秒 | 同步 |
| **Google Gemini** | ~10-20秒 | 同步 |
| **Google Imagen** | ~15-30秒 | 同步 |
| **ModelScope** | ~20-40秒 | 异步+轮询 |
| **APIMart** | ~20-40秒 | 异步+轮询 |

---

## 四、应用注意点

### 1. 云雾 API

**优点：**
- ✅ 响应速度快（Flash 模型）
- ✅ API 简单，与 Gemini 兼容
- ✅ 适合实时生成场景

**注意点：**
- ⚠️ API Key 需要从云雾平台获取
- ⚠️ 质量略低于 Gemini 3 Pro
- ⚠️ 需要在提示词中嵌入尺寸信息

**适用场景：**
- 需要快速响应的实时生成
- 批量预览生成
- 作为首选方案，失败降级

**代码示例：**
```typescript
const url = `https://yunwu.ai/v1beta/models/gemini-2.5-flash-image-preview:generateContent?key=${YUNWU_API_KEY}`;

const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    contents: [{
      parts: [{ text: `A cat. Aspect ratio: 16:9.` }]
    }],
    generationConfig: {
      responseModalities: ["IMAGE", "TEXT"]
    }
  })
});
```

---

### 2. Google Gemini (banana-mcp)

**优点：**
- ✅ 质量最高
- ✅ 同步返回，使用简单
- ✅ MCP 协议，Claude Code 直接调用

**注意点：**
- ⚠️ 响应时间较长
- ⚠️ 需要处理 base64 数据
- ⚠️ 尺寸需嵌入提示词

**适用场景：**
- MCP 调用场景
- 高质量单图生成
- Claude Code 直接调用

---

### 3. ModelScope

**优点：**
- ✅ 免费额度高（2000张/天）
- ✅ 支持图生图
- ✅ 支持自定义像素尺寸

**注意点：**
- ⚠️ 异步模式，需要轮询
- ⚠️ 质量中等
- ⚠️ 返回 URL，需要二次下载

**适用场景：**
- 批量生成
- 图生图需求
- 成本敏感项目

**轮询代码示例：**
```python
# 提交任务
task_id = submit_task(prompt, model, size)

# 轮询状态
while True:
    result = check_task_status(task_id)
    if result["task_status"] == "SUCCEED":
        download_image(result["output_images"][0])
        break
    elif result["task_status"] == "FAILED":
        raise Exception("Generation failed")
    time.sleep(5)
```

---

### 4. APIMart

**优点：**
- ✅ 支持多种模型
- ✅ 批量处理能力
- ✅ 灵活的配置选项

**注意点：**
- ⚠️ 第三方服务，稳定性依赖平台
- ⚠️ 需要配置 TOKEN
- ⚠️ 异步模式，需要轮询

**适用场景：**
- 批量生图需求
- 需要灵活配置的场景
- JSONL 批量文件处理

---

## 五、推荐策略

### 场景推荐矩阵

| 场景 | 首选 | 备选 | 原因 |
|------|------|------|------|
| **Claude Code 调用** | banana-mcp | 云雾 API | MCP 原生支持 |
| **快速预览** | 云雾 API | ModelScope | 速度优先 |
| **高质量输出** | Google Gemini | APIMart | 质量优先 |
| **批量生成** | ModelScope | APIMart | 免费额度 |
| **图生图** | ModelScope | - | 独有功能 |
| **生产环境** | 云雾 API + 降级 | ModelScope | 稳定性 |

### 推荐降级策略

```typescript
async function generateWithFallback(prompt, outputPath) {
  // 1. 首选：云雾 API（快速）
  try {
    const result = await generateWithYunwu(prompt, outputPath);
    if (result.success) {
      console.log('✓ 云雾 API 生成成功');
      return { ...result, provider: 'yunwu' };
    }
  } catch (e) {
    console.log('⚠️ 云雾 API 失败:', e.message);
  }

  // 2. 降级：Google Gemini（高质量）
  try {
    const result = await generateWithGemini(prompt, outputPath);
    if (result.success) {
      console.log('✓ Gemini API 生成成功');
      return { ...result, provider: 'gemini' };
    }
  } catch (e) {
    console.log('⚠️ Gemini API 失败:', e.message);
  }

  // 3. 兜底：ModelScope（免费额度）
  try {
    const result = await generateWithModelScope(prompt, outputPath);
    if (result.success) {
      console.log('✓ ModelScope 生成成功');
      return { ...result, provider: 'modelscope' };
    }
  } catch (e) {
    console.log('❌ 所有 API 都失败:', e.message);
    throw new Error('所有生图 API 均不可用');
  }
}
```

---

## 六、环境变量配置汇总

```bash
# ~/.baoyu-skills/.env 或项目 .env

# 云雾 API（推荐首选）
YUNWU_API_KEY=your_yunwu_api_key

# Google AI Studio
GOOGLE_API_KEY=your_google_api_key
GOOGLE_IMAGE_MODEL=gemini-3-pro-image-preview

# ModelScope（可选，有免费额度）
MODELSCOPE_API_KEY=ms-51dd7494-0706-45d9-a901-c395522c55f2

# APIMart（可选）
APIMART_TOKEN=your_apimart_token
```

---

## 七、常见问题

### Q1: 如何选择合适的 API？

**A: 根据场景选择：**
- **速度优先** → 云雾 API
- **质量优先** → Google Gemini / Imagen
- **成本优先** → ModelScope
- **MCP 调用** → banana-mcp

### Q2: 尺寸参数如何正确设置？

**A: 不同 API 格式不同：**
```javascript
// 云雾 / Gemini - 嵌入提示词
prompt = "A cat. Aspect ratio: 16:9."

// Imagen - 独立参数
{ aspectRatio: "16:9" }

// ModelScope - 像素尺寸
{ size: "1792x1024" }  // 16:9

// APIMart - 比例字符串
{ size: "16:9" }
```

### Q3: 如何处理异步 API？

**A: ModelScope 和 APIMart 需要轮询：**
```python
# 通用轮询模板
def poll_task(task_id, max_wait=300):
    start = time.time()
    while time.time() - start < max_wait:
        result = check_status(task_id)
        if result["status"] in ["SUCCEED", "FAILED"]:
            return result
        time.sleep(5)
    raise TimeoutError("任务超时")
```

### Q4: base64 数据如何处理？

**A: 解码并保存：**
```python
import base64
from pathlib import Path

# 从响应提取
b64_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]

# 解码
image_bytes = base64.b64decode(b64_data)

# 保存
Path("output.png").write_bytes(image_bytes)
```
