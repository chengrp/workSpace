---
name: ms-image
description: ModelScope免费AI绘图工具，每天可生成2000张高质量图片。支持文生图（根据文字描述生成）和图生图（根据参考图生成同风格图片）功能，支持自定义尺寸如16:9、9:16、1:1等多种比例。当用户说"生成图片"、"AI画"、"绘图"、"创建图片"或"根据这张图片生成"时触发。
---

# ms-image Skill - ModelScope免费AI绘图工具

## 技能描述

这是一个使用ModelScope API进行AI图片生成的技能。通过ModelScope的`Tongyi-MAI/Z-Image-Turbo`模型，每天可以免费生成2000张高质量图片。

## 触发条件

当用户提出以下需求时，触发此技能：
- "帮我生成一张图片"
- "用AI画一个..."
- "创建图片..."
- "生成图像..."
- "使用ModelScope绘图..."
- "免费AI绘图..."
- "根据这张图片生成..."（图生图）
- "生成同风格的图片..."（图生图）
- 或其他类似的图片生成请求

## 功能特性

### 核心功能
- **免费额度**：每天2000张免费图片生成额度
- **快速生成**：使用Turbo模型，生成速度快
- **异步处理**：支持异步任务提交和轮询
- **高质量输出**：基于通义千问的图像生成模型
- **图生图功能**：支持根据参考图生成同风格图片
- **自定义尺寸**：支持多种比例和尺寸（16:9、9:16、1:1等）

### 增强功能（v2.0+）
- **🎨 预设风格模板**：8种预定义风格（赛博朋克、水彩画、写实摄影等）
- **✨ Prompt智能优化**：自动增强prompt描述，提升生成质量
- **📊 额度管理**：本地记录使用次数，查询剩余额度
- **🔄 批量生成**：一次生成多张图片，自动并发控制

### 支持的参数
- `prompt`（必填）：图片描述提示词
- `size`（可选）：图片尺寸，格式"宽x高"，如"1920x1080"、"1080x1920"、"1536x1536"
- `reference_image`（可选）：参考图片路径（图生图模式）
- `style`（可选）：预设风格（cyberpunk、watercolor、realistic、anime、oilpainting、3drender、pixelart、minimalist）
- `batch`（可选）：批量生成数量
- `enhance_prompt`（可选）：是否优化prompt（默认True）
- `model`：默认使用"Tongyi-MAI/Z-Image-Turbo"
- `loras`（可选）：LoRA模型配置
- `output_path`（可选）：输出图片路径，默认为"result_image.jpg"

## 使用流程

当技能被触发时，按照以下步骤操作：

### 1. 参数确认
```python
# 从用户输入中提取prompt和参数
# 例如：用户说"生成一只金色的猫"，则prompt="A golden cat"
# 例如：用户说"根据这张图生成同风格的狗"，则reference_image="xxx.jpg"
```

### 2. API调用流程

#### 文生图模式
```python
# 步骤1：提交异步任务
POST https://api-inference.modelscope.cn/v1/images/generations
Headers:
  - Authorization: Bearer {api_key}
  - Content-Type: application/json
  - X-ModelScope-Async-Mode: true
Body:
  {
    "model": "Tongyi-MAI/Z-Image-Turbo",
    "prompt": "{用户提供的prompt}",
    "size": "1920x1080"  # 可选
  }

# 步骤2：获取task_id
响应: {"task_id": "xxx"}

# 步骤3：轮询任务状态
GET https://api-inference.modelscope.cn/v1/tasks/{task_id}
Headers:
  - Authorization: Bearer {api_key}
  - X-ModelScope-Task-Type: image_generation

# 步骤4：下载图片
```

#### 图生图模式
```python
# 步骤1：读取参考图并转为base64
import base64
with open(reference_image, 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# 步骤2：提交异步任务
POST https://api-inference.modelscope.cn/v1/images/generations
Headers:
  - Authorization: Bearer {api_key}
  - Content-Type: application/json
  - X-ModelScope-Async-Mode: true
Body:
  {
    "model": "Tongyi-MAI/Z-Image-Turbo",
    "prompt": "{用户提供的prompt}",
    "image": "{base64编码的参考图}",
    "size": "1920x1080"  # 可选
  }

# 步骤3和4：同文生图模式
当task_status为"SUCCEED"时，从output_images[0]下载图片
```

### 3. 输出结果
- 保存图片到指定路径
- 向用户展示生成的图片
- 提供图片文件路径

## 错误处理

### 常见错误及解决方案
1. **API Key无效**
   - 错误：401 Unauthorized
   - 解决：检查API Key配置

2. **额度超限**
   - 错误：429 Too Many Requests
   - 解决：等待额度重置（每日重置）

3. **生成失败**
   - task_status: "FAILED"
   - 解决：检查prompt内容，重新尝试

4. **网络超时**
   - 解决：增加轮询间隔时间

## 最佳实践

### Prompt编写建议
- 使用英文prompt效果更好
- 描述要具体清晰
- 包含风格、构图、细节等元素
- 示例："A golden cat sitting on a red cushion, digital art, highly detailed"

### LoRA使用（高级功能）
```python
# 单个LoRA
"loras": "<lora-repo-id>"

# 多个LoRA（权重之和为1.0）
"loras": {
  "<lora-repo-id1>": 0.6,
  "<lora-repo-id2>": 0.4
}
```

## 配置要求

### 环境依赖
```bash
pip install requests pillow
```

### API Key配置
- 当前使用的API Key：`ms-51dd7494-0706-45d9-a901-c395522c55f2`
- 获取方式：访问ModelScope官网申请

## 使用示例

### 示例1：基本使用（文生图）
用户输入：
```
帮我生成一张图片，内容是"一只金色的猫"
```

AI响应：
```
好的，我来为你生成一张金色的猫的图片。
[调用API生成图片]
图片已生成并保存到：result_image.jpg
```

### 示例2：指定尺寸
用户输入：
```
生成一张16:9的图片，内容是"美丽的日落风景"
```

AI响应：
```
好的，正在生成16:9比例的日落风景图片（1920x1080）...
[调用API，使用size="1920x1080"]
图片已保存到：result_image.jpg
```

### 示例3：图生图（生成同风格图片）
用户输入：
```
根据这张卡通图片[上传tom_jerry.jpg]，生成一张同风格的狗和猫的图片
```

AI响应：
```
好的，我将使用参考图来生成同风格的图片。
[读取参考图，转换为base64]
[调用API，使用image参数]
同风格的图片已生成并保存到：img2img_result.jpg
```

### 示例4：指定保存路径
用户输入：
```
生成一只飞翔的鹰，保存到eagle.jpg
```

AI响应：
```
好的，正在生成飞翔的鹰的图片...
[调用API，保存到eagle.jpg]
图片已保存到：eagle.jpg
```

### 示例5：详细prompt
用户输入：
```
生成一张图片：赛博朋克风格的未来城市，霓虹灯，雨夜，高清细节
```

AI转换为：
```
prompt: "Cyberpunk futuristic city, neon lights, rainy night, high definition, highly detailed"
```

## 尺寸参数说明

### 支持的尺寸和比例
| 比例 | 尺寸示例 | 用途 | 分辨率 |
|------|---------|------|--------|
| 16:9 | 1920x1080, 1792x1024 | 横屏、桌面壁纸 | FHD |
| 9:16 | 1080x1920, 1024x1792 | 竖屏、手机壁纸 | FHD |
| 1:1 | 1536x1536 | 正方形、社交媒体 | HD |
| 4:3 | 1536x1152 | 传统照片 | HD |
| 3:4 | 1152x1536 | 传统照片竖版 | HD |

### 重要说明
- ✅ **size参数有效**：可以使用size="宽x高"控制输出尺寸
- ❌ **width/height参数无效**：单独的width和height参数被API忽略
- ⚠️ **分辨率限制**：最高支持FHD级别（约2MP），2K+会返回400错误

## 技术实现

### 核心脚本位置
- 主脚本：`scripts/ms_image_generator.py`
- 配置文件：`scripts/config.py`

### 轮询机制
- 检查间隔：5秒
- 超时时间：无限制（直到任务完成或失败）
- 状态检查：SUCCEED（成功）、FAILED（失败）、PENDING/RUNNING（进行中）

## 注意事项

1. **API Key安全**：不要在公开场合泄露API Key
2. **额度管理**：每天2000张免费额度，合理使用
3. **内容合规**：生成的图片内容需符合相关法律法规
4. **英文Prompt**：虽然支持中文，但英文prompt效果通常更好
5. **文件覆盖**：默认会覆盖同名文件，请注意文件名管理

## 增强功能详解（v2.0）

### 1. 预设风格模板

支持8种预定义风格，一键应用专业级效果：

| 风格ID | 中文名称 | 关键词 |
|--------|----------|--------|
| cyberpunk | 赛博朋克 | 霓虹灯、未来建筑、夜景、雨天氛围 |
| watercolor | 水彩画 | 柔和边缘、艺术感、粉彩色彩 |
| realistic | 写实摄影 | 专业摄影、自然光、高细节 |
| anime | 日系动漫 | 动漫风格、鲜艳色彩、线条清晰 |
| oilpainting | 油画 | 纹理笔触、经典艺术、丰富色彩 |
| 3drender | 3D渲染 | Octane渲染、CGI、体积光 |
| pixelart | 像素艺术 | 复古游戏风格、8位、16位 |
| minimalist | 极简主义 | 简洁设计、负空间、现代感 |

### 2. Prompt智能优化

自动增强用户的prompt描述：

**原始prompt：** `A golden cat`

**优化后：** `A golden cat, highly detailed, professional quality, sharp focus, best quality`

**配合风格：**
```python
prompt: "A golden cat"
style: "cyberpunk"
结果: "A golden cat, Cyberpunk style, neon lights, futuristic architecture, night city, rain, dark atmosphere, highly detailed, digital art, 4K, cinematic lighting, professional quality"
```

### 3. 额度管理

本地记录使用情况，实时显示剩余额度：

```bash
# 查看额度
python scripts/ms_image_enhanced.py --quota

输出:
==================================================
📊 额度使用情况
==================================================
日期: 2025-01-29
已用: 45/2000 (2.3%)
剩余: 1955
==================================================
```

### 4. 批量生成

一次生成多张图片：

```bash
# 批量生成4张
python scripts/ms_image_enhanced.py "A golden cat" --batch 4

# 配合风格模板
python scripts/ms_image_enhanced.py "A cityscape" --style cyberpunk --batch 4
```

### 增强版使用示例

#### 示例1：使用风格模板
```
用户: 生成一张赛博朋克风格的猫咪图片

AI响应:
正在生成赛博朋克风格的猫咪图片...
Prompt: A cat, Cyberpunk style, neon lights, futuristic architecture, night city, rain, dark atmosphere, highly detailed, digital art, 4K, cinematic lighting, professional quality
```

#### 示例2：批量生成不同风格
```
用户: 生成4张水彩画风格的风景图

AI响应:
开始批量生成 4 张图片...
[1/4] 生成第 1 张图片...
[2/4] 生成第 2 张图片...
...
批量生成完成: 4/4 成功
图片已保存到: image/batch/
```

#### 示例3：查询额度
```
用户: 查看剩余额度

AI响应:
==================================================
📊 额度使用情况
==================================================
日期: 2025-01-29
已用: 45/2000 (2.3%)
剩余: 1955
==================================================
```

### 增强版命令行参数

```bash
python scripts/ms_image_enhanced.py [prompt] [options]

选项:
  --style STYLE        预设风格模板
  --batch N            批量生成数量
  --no-enhance         禁用prompt自动优化
  --quota              查看额度使用情况
  --list-styles        列出所有可用风格
  -o OUTPUT            输出路径
  -s SIZE              图片尺寸（如1920x1080）
  -r REFERENCE         参考图片路径（图生图）
```

## 更新日志

- **v2.0** (2025-01-29)：增强版本
  - ✨ 新增预设风格模板功能（8种风格）
  - ✨ 新增Prompt智能优化
  - ✨ 新增额度管理系统
  - ✨ 新增批量生成功能
  - 📝 完善文档和示例

- **v1.0** (2025-01-15)：初始版本
  - 支持基本的图片生成功能
  - 集成ModelScope Turbo模型
  - 实现异步任务处理
