---
name: tavily-search
description: "使用 Tavily API 进行智能搜索。适用于：(1) 需要结构化搜索结果，(2) 需要新闻/实时信息，(3) web_search 不可用时。自动从 OpenClaw 配置读取 API 密钥。"
author: "天依 (Tianyi)"
source: "internal"
created: "2026-02-28"
refactored-from: "workspace/skills/tavily-search"
tags: ["search", "tavily", "api", "web"]
metadata: {"openclaw": {"emoji": "🔍", "requires": {"bins": ["curl", "jq"]}, "configKey": "tools.web.search.apiKey"}}
---

# Tavily Search Skill

> **🏷️ Skill 来源：** 内部生成  
> **👤 作者：** 天依 (Tianyi)  
> **📅 创建时间：** 2026-02-28  
> **🔄 重构自：** workspace/skills/tavily-search  
> **🎯 用途：** 使用 Tavily API 进行智能搜索的完整指南

## 📖 描述

Tavily 是专为 AI 助手设计的搜索引擎，提供结构化搜索结果。

**优势：**
- ✅ 结构化搜索结果（标题、URL、摘要、评分）
- ✅ 支持新闻/通用搜索
- ✅ 适合 AI 助手的优化结果
- ✅ **自动从 OpenClaw 配置文件读取密钥**（无需手动设置）

---

## 🔑 API 配置

### 方式 1：OpenClaw 配置（推荐，自动读取）

```bash
# 1. 获取密钥：https://app.tavily.com/settings

# 2. 配置到 OpenClaw
openclaw config set tools.web.search.apiKey "tvly-your-api-key"

# 3. 验证（显示 __OPENCLAW_REDACTED__ 表示已配置）
openclaw config get tools.web.search.apiKey
```

**脚本会自动从 `~/.openclaw/openclaw.json` 读取密钥，无需额外操作！**

### 方式 2：环境变量

```bash
# 添加到 ~/.bashrc
echo 'export TAVILY_API_KEY="tvly-your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 使用方法

### 使用封装脚本（推荐）

```bash
# 基本搜索
~/.openclaw/skills/tavily-search/scripts/search.sh "搜索关键词"

# 带选项
~/.openclaw/skills/tavily-search/scripts/search.sh "AI 技术突破" --topic news --max 10

# 查看帮助
~/.openclaw/skills/tavily-search/scripts/search.sh --help
```

**可用选项：**
| 选项 | 说明 | 默认值 |
|------|------|--------|
| `--topic` | 搜索类型：`general` 或 `news` | `general` |
| `--max` | 最大结果数 | `5` |
| `--depth` | 搜索深度：`basic` 或 `advanced` | `basic` |

---

## 📊 免费额度

| 层级 | 额度 | 限制 |
|------|------|------|
| **免费** | 1000 次/月 | 10 次/分钟 |
| **付费** | 查看官网 | 更高限制 |

---

## 🔒 安全说明

### ✅ 推荐做法

1. **使用 `openclaw config` 命令** - 自动管理文件权限
2. **文件权限 600** - `chmod 600 ~/.openclaw/openclaw.json`
3. **不提交到 git** - 确保 `.gitignore` 包含配置文件

### ⚠️ 避免的做法

1. ❌ 不要硬编码在脚本中
2. ❌ 不要明文发送到聊天
3. ❌ 不要提交到版本控制

---

## 🧹 故障排除

### 提示"未设置 API 密钥"

```bash
# 检查配置
openclaw config get tools.web.search.apiKey

# 如果显示空，重新配置
openclaw config set tools.web.search.apiKey "tvly-your-key"

# 或检查配置文件
grep apiKey ~/.openclaw/openclaw.json
```

### API 调用失败

```bash
# 测试 API
curl -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d '{"api_key":"tvly-your-key","query":"test"}'
```

---

## 📁 文件结构

```
~/.openclaw/skills/tavily-search/
├── SKILL.md              # 本文档
├── KEYS.md               # 详细密钥管理指南
├── scripts/
│   └── search.sh         # 封装脚本（自动读取配置）
├── assets/
│   └── examples.md       # 使用示例
└── references/
    └── api-docs.md       # API 文档参考
```

---

## 🔧 脚本实现细节

封装脚本通过以下方式自动读取密钥：

```bash
# 优先级：1. 环境变量  2. OpenClaw 配置文件
if [ -z "$TAVILY_API_KEY" ]; then
    TAVILY_API_KEY=$(grep -o '"apiKey"[[:space:]]*:[[:space:]]*"[^"]*"' \
                     ~/.openclaw/openclaw.json | head -1 | cut -d'"' -f4)
fi
```

---

_最后更新：2026-03-01 | 安全等级：中等 | 自动读取 OpenClaw 配置 ✅_
