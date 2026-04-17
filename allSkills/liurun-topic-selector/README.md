# 刘润公众号选题智能体

> 以"类刘润"风格研究中国商业事件，生成深度选题建议和写作角度

## 简介

这是一个专为中国商业内容创作者设计的选题智能体。它自动抓取主流商业媒体的最新报道，智能分析重大事件，并提供符合"刘润风格"的选题建议。

**关注领域**：互联网、新能源、AI、大消费

**数据源**：36氪、虎嗅、晚点、界面、钛媒体等9+商业媒体

## 快速开始

### 安装依赖（可选）

```bash
pip install feedparser
```

> 如果没有安装feedparser，系统会自动降级到curl方案

### 运行

```bash
cd CC_record/skills/liurun-topic-selector/scripts
python main.py [hours]
```

默认获取最近48小时内的新闻。

### 输出

- `output/daily_report.md` - 完整每日报告（事件概览 + 深度分析占位）
- `output/topics_recommendations.md` - Top3选题推荐

## 工作流程

```
抓取新闻 → 分析事件 → 选择选题 → 生成报告
   ↓          ↓          ↓          ↓
 RSS源    提取关键数据   刘润风格    Markdown
48小时内   识别事件类型   评分筛选    双文件输出
```

## 配置

所有配置文件位于 `config/` 目录：

- `sources.json` - 新闻源配置
- `keywords.json` - 关键词和公司列表
- `filters.json` - 过滤规则

## 使用示例

```bash
# 获取最近48小时的新闻（默认）
python main.py

# 获取最近24小时的新闻
python main.py 24

# 获取最近72小时的新闻
python main.py 72
```

## 设计哲学

**脚本负责机械，Claude负责智能**

- 脚本：抓取、过滤、结构化数据
- Claude：深度分析、观点识别、写作角度

## License

MIT
