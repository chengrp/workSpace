# ms-image - ModelScope免费AI绘图技能

## 简介

`ms-image`是一个使用ModelScope API进行AI图片生成的Claude Code技能。通过通义千问的`Z-Image-Turbo`模型，每天可以免费生成2000张高质量图片。

## 特性

- ✅ **免费额度**：每天2000张图片生成额度
- ⚡ **快速生成**：使用Turbo模型，生成速度快
- 🎨 **高质量输出**：基于通义千问图像生成模型
- 🔄 **异步处理**：支持任务提交和状态轮询
- 🎯 **简单易用**：友好的命令行接口

## 安装

### 1. 环境要求

```bash
pip install requests pillow
```

### 2. 技能安装

将此技能目录放置在Claude Code的skills目录下：

```bash
# Windows
CC_record\skills\ms-image\

# 或创建符号链接到Claude skills目录
```

## 使用方法

### 在Claude Code中使用

直接告诉Claude你的图片生成需求：

```
帮我生成一张图片，内容是"一只金色的猫坐在红垫子上"
```

Claude会自动：
1. 理解你的需求
2. 调用ModelScope API
3. 生成并保存图片
4. 告诉你图片保存位置

### 命令行使用

```bash
# 基本使用
python scripts/ms_image_generator.py "A golden cat"

# 指定输出路径
python scripts/ms_image_generator.py "A flying eagle" -o eagle.jpg

# 使用快速CLI
python scripts/ms_cli.py "A beautiful sunset" sunset.jpg
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `prompt` | 图片描述（建议英文） | 必填 |
| `-o, --output` | 输出图片路径 | result_image.jpg |
| `-m, --model` | 使用的模型 | Tongyi-MAI/Z-Image-Turbo |
| `-i, --interval` | 状态检查间隔（秒） | 5 |
| `-k, --api-key` | 自定义API Key | 内置key |
| `-q, --quiet` | 静默模式 | False |

## Prompt编写建议

### 好的Prompt示例

- "A golden cat sitting on a red cushion, digital art, highly detailed"
- "Cyberpunk city at night, neon lights, rain, 4K, cinematic"
- "A peaceful mountain landscape at sunset, oil painting style"

### 编写技巧

1. **使用英文**：英文prompt效果通常更好
2. **具体描述**：包含主体、场景、风格、细节
3. **添加修饰词**：highly detailed, 4K, cinematic, digital art等
4. **指定风格**：oil painting, watercolor, digital art, photography等

## 项目结构

```
ms-image/
├── SKILL.md                    # 技能文档（Claude读取）
├── README.md                   # 使用说明
├── scripts/                    # Python脚本
│   ├── config.py              # 配置文件
│   ├── ms_image_generator.py  # 核心生成器
│   └── ms_cli.py              # 快速CLI工具
├── examples/                   # 示例和测试
│   └── test.py                # 测试脚本
└── references/                 # 参考文档
```

## API信息

- **API提供商**：ModelScope
- **模型**：Tongyi-MAI/Z-Image-Turbo
- **免费额度**：2000张/天
- **API文档**：https://inference.modelscope.cn/

## 常见问题

### Q: 额度用完了怎么办？
A: 免费额度每天重置。也可以申请自己的API Key。

### Q: 生成失败怎么办？
A: 检查prompt内容是否合规，稍后重试。

### Q: 支持中文prompt吗？
A: 支持，但英文效果通常更好。

### Q: 可以生成多张图片吗？
A: 目前每次调用生成一张，可以多次调用。

## 技术实现

### API调用流程

1. 提交异步任务 → 获取task_id
2. 轮询任务状态 → 等待完成
3. 下载图片 → 保存到本地

### 错误处理

- 401: API Key无效
- 429: 额度超限
- FAILED: 生成失败

## 许可证

MIT License

## 贡献

欢迎提交问题和改进建议！

## 更新日志

- **v1.0** (2025-01-15)
  - 初始版本发布
  - 支持基本图片生成功能
  - 集成ModelScope Turbo模型
