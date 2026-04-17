# API 连接问题解决方案

## 问题状态

| API | 状态 | 原因 |
|-----|------|------|
| Google AI | ❌ | 连接超时，可能被防火墙阻止 |
| 代理连接 | ❌ | 代理服务未响应 (127.0.0.1:60821) |
| ModelScope | ❌ | API Key 未配置 |

---

## 解决方案

### 方案 1：启动代理服务（推荐用于 Google AI）

1. 启动你的代理工具（Clash/V2Ray/其他）
2. 确认代理端口（如 7890, 1080 等）
3. 更新 `.env` 文件中的代理设置：

```bash
HTTPS_PROXY=http://127.0.0.1:你的端口
HTTP_PROXY=http://127.0.0.1:你的端口
```

4. 重新运行生成命令

### 方案 2：使用 ModelScope（国内服务，免费）

1. 获取 ModelScope API Key:
   - 访问：https://modelscope.cn/
   - 注册账号并创建 API Key

2. 更新 `.env` 文件：
```bash
ALL_IMAGE_MODELSCOPE_API_KEY=你的ModelScope_API_Key
```

3. 运行时使用 `mode='free'`

### 方案 3：手动网页生图（最简单）

1. 打开 Google AI Studio: https://aistudio.google.com/app/prompts/new_image
2. 复制提示词文件内容
3. 粘贴并生成图片

提示词文件位置：
- `output/智能不再稀缺/prompts/智能不再稀缺_坐标蓝图版_Prompt.txt`

---

## 备选操作流程

当 API 连接失败时：

```bash
# 1. 测试网络连通性
curl -I https://generativelanguage.googleapis.com

# 2. 如果超时，尝试使用代理
curl -x http://127.0.0.1:端口 -I https://generativelanguage.googleapis.com

# 3. 或者直接使用网页手动生成
```

---

## 配置文件位置

- `C:/Users/RyanCh/.claude/skills/all-image/.env`

当前代理配置：`http://127.0.0.1:60821`
