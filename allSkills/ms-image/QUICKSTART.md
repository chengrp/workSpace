# ms-image 技能快速开始指南

## 概述

`ms-image` 是一个免费的AI图片生成技能，使用ModelScope的通义千问Turbo模型，每天可以生成2000张高质量图片。

## 立即开始

### 在Claude Code中使用（推荐）

直接告诉Claude你的需求：

```
帮我生成一张图片，内容是"一只金色的猫坐在红垫子上"
```

Claude会自动：
1. 理解你的描述
2. 调用ModelScope API
3. 生成图片并保存
4. 告诉你保存位置

### 命令行使用

```bash
# 基本使用
python scripts/ms_image_generator.py "A golden cat"

# 指定输出文件名
python scripts/ms_image_generator.py "A flying eagle" -o eagle.jpg

# 使用快速CLI
python scripts/ms_cli.py "A beautiful sunset" sunset.jpg

# 查看所有选项
python scripts/ms_image_generator.py --help
```

## 技术细节

### API信息
- **提供商**：ModelScope (modelscope.cn)
- **模型**：Tongyi-MAI/Z-Image-Turbo
- **免费额度**：2000张/天
- **生成速度**：约20-30秒/张

### Prompt编写建议

好的prompt示例：
- "A golden cat sitting on a red cushion, digital art, highly detailed"
- "Cyberpunk city at night, neon lights, rain, 4K, cinematic"
- "A peaceful mountain landscape at sunset, oil painting style"

技巧：
1. 使用英文（效果更好）
2. 包含主体、场景、风格
3. 添加修饰词：highly detailed, 4K, cinematic
4. 指定艺术风格：digital art, oil painting, photography

## 项目结构

```
ms-image/
├── SKILL.md                    # 技能文档（Claude读取）
├── README.md                   # 详细说明
├── QUICKSTART.md              # 本文件
├── requirements.txt           # Python依赖
├── scripts/                   # 核心代码
│   ├── config.py             # 配置
│   ├── ms_image_generator.py # 生成器
│   └── ms_cli.py             # CLI工具
└── examples/                  # 示例和测试
    ├── test.py               # 完整测试
    └── quick_test.py         # 快速测试
```

## 运行测试

验证技能是否正常工作：

```bash
# 快速测试（生成一张图片）
python examples/quick_test.py

# 完整测试（生成三张图片）
python examples/test.py
```

## 常见问题

**Q: 额度用完了怎么办？**
A: 免费额度每天重置。也可以申请自己的API Key。

**Q: 支持中文prompt吗？**
A: 支持，但英文效果通常更好。

**Q: 生成需要多长时间？**
A: 通常20-30秒，取决于服务器负载。

**Q: 可以调整图片大小吗？**
A: 当前版本使用默认大小，未来版本可能支持。

## 获取帮助

- 详细文档：[README.md](README.md)
- 技能规范：[SKILL.md](SKILL.md)
- ModelScope官网：https://modelscope.cn/

## 开始使用

现在就对Claude说：
```
帮我生成一张图片...
```

享受免费AI绘图的乐趣！
