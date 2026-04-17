# 阶段4：提示词封装（Prompt Pack：可执行生成包）

**目标：** 把阶段3的 Copy Spec 原样封装成"可复制/可调用"的提示词包（Prompt Pack），并支持批量出图。阶段4不负责改文案，只负责：模板拼装、风格一致、参数/约束齐全、避免模型乱加字、把提示词整理成可批量请求的结构化请求包。

## 封装原则（避免和阶段3混淆）

- **Copy Spec 是唯一真值**：提示词中“必须逐字放入”的文字，直接来自阶段3，不在这里重写。
- **提示词负责“怎么画”**：画幅、版式、留白、对齐、图标隐喻、风格块、强制约束、负面提示、参数。
- **封面类默认“禁额外小字”**：明确写“除指定文字外不要生成任何额外文字”。

## 生成步骤（按顺序）

1. 选定结构模板（与 Copy Spec 的版式一致）
2. 粘贴通用风格块：`templates/style-block.md`
   - **风格基准锁定**：每张图都必须以 `templates/style-block.md` 定义的风格作为**唯一允许的基础风格**来生成（奶油纸 + 彩铅线稿 + 淡水彩 + 轻涂鸦、少字高可读）。
   - **不得换风格**：不要让模型自行切换成扁平矢量海报风/3D/摄影写实等“更像信息图默认风格”的路线。
   - 允许你用自己的话描述该风格，但不能删掉关键要素与负面约束（否则风格会被模型先验带偏）。
3. 写清楚画幅/用途（PPT远看 vs 手机近看）与排版硬约束（对齐、留白、字号）
4. 粘贴 Copy Spec 的"必须逐字放入的文字"
5. 加强制约束 + 负面提示（无乱码/不加字/不密集小字/不背景杂乱）
6. 生成**批量请求包（JSONL）**：把每张图的 Prompt 内容写入一行（参考 `templates/apimart-requests-jsonl.md`）
7. 用户选择批量API方式后：直接生成JSONL并执行批量出图（不再二次确认）

## 模板使用

- 通用风格块：`templates/style-block.md`
- 结构模板：
  - 封面路线图（目录/5步）：`templates/16x9-cover-roadmap.md`
  - 对比两卡：`templates/16x9-contrast-2cards.md`
  - 三卡洞察：`templates/16x9-3cards-insights.md`
  - 五格漫画：`templates/16x9-5panel-comic.md`
  - 通用信息图：`templates/16x9-infographic.md`

## 本阶段输出物

- **Prompt Pack**：按"图1/图2/…"编号输出；每张图一个独立代码块（便于复制/脚本调用）；代码块外最多 1–2 句说明
- **Batch Request Pack（JSONL）**：例如 `out/apimart.requests.jsonl`（一行一张图，字段见下文）
- **执行方式**：当用户在阶段4明确选择"批量API"时，先输出提示词让用户查看（选项A：手动出图 或 选项B：批量API），一旦用户选择B，直接生成JSONL并执行，不再二次确认

## 为什么“阶段4”容易风格跑偏（解释逻辑）

阶段4本质是“用文字去约束一个带强默认审美的出图模型”，风格会被多方力量拉扯：

1. **模型先验（Style Prior）**：很多模型看到 “infographic/信息图” 会自动偏向“干净的扁平矢量/海报风”，即使你写了彩铅水彩，也可能只被当作弱建议。
2. **可读性约束会压过质感**：当你同时要求“中文大字号、严格对齐、少字、清晰”，模型会优先保证字清楚与版式稳定，牺牲纸纹、彩铅笔触等“质感细节”。
3. **风格基准不够“排他”会降权**：如果不强调“这是唯一允许风格，不能换”，模型会把它当成“可选项”，然后自动回到信息图的默认风格（常见是扁平矢量/海报风）。
4. **风格词太短/太抽象**：仅写“彩铅水彩”不足以锁定细节，需要补“纸纹可见、笔触可见、轻晕染”等可观察特征，并配合负面约束（已在风格块中补强）。

实操上要提升稳定性：在每张图的 prompt 里都明确“以该风格为唯一基础，不得换风格”，并加入“不要扁平矢量/不要3D/不要摄影”等负面约束来对冲模型的默认风格。

---

## 批量出图执行方式选择

> 规则：**先封装 Prompt Pack 并展示给用户 → 提供生图方式选项 → 用户选择后执行**

### 生图方式选择（请在执行前让用户选择）

完成 Prompt Pack 封装后，向用户展示以下可用生图方式：

#### 方式对比快速参考

| 方式 | 速度 | 质量 | 成本 | 特点 |
|------|------|------|------|------|
| **云雾 API** | ⚡⚡⚡ 快 | ★★★☆ | 按量 | Gemini 2.5 Flash，推荐首选 |
| **banana-mcp** | ⚡⚡ 中 | ★★★★★ | 按量 | Claude Code MCP 调用 |
| **ModelScope** | ⚡⚡ 中 | ★★★☆ | 2000免费/天 | 免费额度，支持图生图 |
| **Google AI** | ⚡⚡ 中 | ★★★★★ | 按量 | Gemini 3 Pro 最高质量 |
| **APIMart** | ⚡⚡ 中 | ★★★★ | 按量 | 第三方聚合，批量支持 |
| **手动复制** | - | - | 免费 | 用户自行复制到其他平台 |

#### 推荐决策流程

```
开始批量出图
│
├─ 需要在 Claude Code 中直接生成？
│  └─ 是 → banana-mcp（逐张调用）
│
├─ 需要免费大量生成？
│  └─ 是 → ModelScope（2000张/天）
│
├─ 需要最高质量？
│  └─ 是 → Google AI（Gemini 3 Pro）
│
├─ 需要最快速度？
│  └─ 是 → 云雾 API（Flash 模型）
│
└─ 想要自己控制？
   └─ 手动复制提示词
```

### 用户确认后执行

根据用户选择，提供对应的执行方法：

---

## A. banana-mcp（Claude Code 直接调用）

**适用场景：** 需要在 Claude Code 中直接生成，逐张调用

**执行方式：** 使用 MCP 工具 `generate_image`
```python
# MCP 会自动调用，参数：
# - prompt: 提示词内容
# - output_filename: 输出文件名
# - model: gemini-3-pro-image-preview（默认）
# - aspect_ratio: 16:9（默认）
```

**输出位置：** `banana-mcp/image/`

---

## B. 云雾 API（推荐首选）

**适用场景：** 快速生成，质量稳定

**配置要求：**
```bash
# 设置环境变量
YUNWU_API_KEY=your_api_key
```

**执行方式：** 参考完整的云雾 API 调用示例（详见 `templates/yunwu-api.md`）

---

## C. ModelScope（免费额度）

**适用场景：** 批量生成，成本敏感

**配置要求：**
```bash
# 已内置免费 API Key，或设置
MODELSCOPE_API_KEY=ms-51dd7494-0706-45d9-a901-c395522c55f2
```

**执行方式：**
```bash
# 使用 ms-image skill
python3 /path/to/ms-image/scripts/ms_image_generator.py \
  "prompt here" \
  --size 1792x1024 \
  --output output.png
```

---

## D. Google AI Studio（最高质量）

**适用场景：** 需要最高质量输出

**配置要求：**
```bash
GOOGLE_API_KEY=your_google_api_key
```

**执行方式：** 通过 banana-mcp 或直接调用 REST API

---

## E. APIMart（第三方聚合）

**适用场景：** 批量处理，灵活配置

**配置要求：**
```bash
# scripts/apimart.env
TOKEN=your_token
MODEL=gemini-3-pro-image-preview
```

**执行方式：**

```bash
# A) 批量出图（推荐）
python3 scripts/apimart_batch_generate.py \
  --config scripts/apimart.env \
  --input out/apimart.requests.jsonl

# B) dry-run（不请求；生成 run.json）
python3 scripts/apimart_batch_generate.py \
  --config scripts/apimart.env \
  --input out/apimart.requests.jsonl \
  --dry-run
```

---

## F. 手动复制（用户自控）

**适用场景：** 用户想使用其他平台（如 Midjourney、DALL-E 等）

**执行方式：** 复制 Prompt Pack 中的提示词，自行到目标平台生成

---

### 请求包字段（每行一张图）

- `id`：建议 `01` / `02` / …
- `prompt`：阶段4输出的 Prompt 内容（可直接粘贴）
- `size`：默认 `16:9`
- `n`：默认 `1`
- `resolution`：默认 `2K`
- `model`：默认 `gemini-3-pro-image-preview`
- `pad_url`：可留空（暂不需要垫图 URL）

> 注：仅 APIMart 方式需要 JSONL 格式的请求包，其他方式直接使用 Prompt Pack
