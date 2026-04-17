---
name: wx-group-analysis
description: |
  微信群数据分析工具 - 基于 wechat-cli 自动生成群分析报告
  
  支持生成的报告类型：
  - 群日报（daily-report）
  - 成员贡献榜（member-ranking）
  - 内容质量报告（content-quality）
  - 成员成长报告（member-growth）
  - 综合月报（monthly-report）
  
  使用方法：
  - "生成本周【群名】的群日报"
  - "生成【群名】的成员贡献榜"
  - "生成【群名】本周的内容质量报告"
  - "生成【群名】的成员成长报告"
  - "生成【群名】的月度综合报告"
  
  前置要求：
  - 已安装 wechat-cli
  - 已执行 wechat-cli init 初始化
  - 微信正在运行

argument-hint: "群日报 | 贡献榜 | 质量报告 | 成长报告 | 月报"

allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - AskUserQuestion
  - Grep
  - Glob
  - mcp__serena__find_file
  - mcp__serena__list_dir
---

# 微信群数据分析 Skill

基于 wechat-cli 的微信群数据分析工具，自动生成多维度群分析报告。

## 前置条件检查

在使用任何功能前，先检查 wechat-cli 是否可用：

```bash
# 检查 wechat-cli 是否安装
wechat-cli --version

# 检查是否已初始化
ls ~/.wechat-cli/config.json
```

如果未安装，提示用户：
```
wechat-cli 未安装或未初始化。

安装方法：
npm install -g @canghe_ai/wechat-cli

初始化方法：
wechat-cli init
```

## 报告类型说明

### 1. 群日报 (daily-report)
**用途**: 每日群运营监控

**包含内容**:
- 今日数据概览（成员数、发言人数、消息总数）
- 消息类型分布
- 24小时活跃分布图
- 热门话题 Top 3
- 活跃成员 Top 5
- 今日分享链接
- 金句摘录

### 2. 成员贡献榜 (member-ranking)
**用途**: 成员激励与价值识别

**包含内容**:
- 评分维度说明（活跃度40%、知识分享25%、互动20%、守时15%）
- 成员贡献总榜 Top 20
- 发言活跃榜 Top 10
- 知识分享榜 Top 10
- 互动达人榜 Top 10
- 守时先锋榜 Top 10
- 特色称号

### 3. 内容质量报告 (content-quality)
**用途**: 内容运营优化

**包含内容**:
- 内容质量概览（5维度评分）
- 内容分布分析
- 高质量内容榜单
- 优质话题识别
- 内容质量标签分析
- 优质内容时间线
- 内容之星
- 质量改进建议

### 4. 成员成长报告 (member-growth)
**用途**: 成员运营与增长分析

**包含内容**:
- 成员成长概览（活跃成员、新增成员、人均发言、沉默成员）
- 本周明星成员（飙升榜、稳定榜、下降榜）
- 成员分层分析（核心层、潜力层、待激活层）
- 成长轨迹图
- 成员标签画像
- 本周里程碑
- 成员运营建议

### 5. 综合月报 (monthly-report)
**用途**: 决策层汇报材料

**包含内容**:
- 核心指标概览
- 本月亮点
- 趋势洞察
- 问题与建议

## 工作流程

### 步骤 1: 解析用户意图

从用户输入中提取：
- **报告类型**: daily-report | member-ranking | content-quality | member-growth | monthly-report
- **群名称**: 群聊名称或关键词
- **时间范围**: 
  - 默认：本周（周一至今日）
  - 支持指定：今天、昨天、本周、上周、本月、上月
  - 支持日期：2026-04-07、最近3天、最近7天等

### 步骤 2: 验证前置条件

```bash
# 检查 wechat-cli
wechat-cli --version

# 检查配置文件
test -f ~/.wechat-cli/config.json || echo "未初始化"
```

### 步骤 3: 获取群数据

```bash
# 获取群列表（如果需要）
wechat-cli sessions --limit 50 --format text

# 获取聊天记录
wechat-cli history "群名" --start-time "开始日期" --end-time "结束日期" --limit 1000 --format text

# 获取统计数据
wechat-cli stats "群名" --start-time "开始日期" --end-time "结束日期" --format text
```

### 步骤 4: 分析数据生成报告

使用 Bash 工具进行数据处理：
- 统计发言排行
- 提取链接分享
- 分析回复互动
- 计算各维度得分

### 步骤 5: 生成报告文件

报告保存路径：`~/wx-group-analysis/reports/`

文件命名格式：`YYYY-MM-DD-{报告类型}-{群名}.md`

## 模板文件位置

- 群日报模板: `templates/daily-report-template.md`
- 成员贡献榜模板: `templates/member-ranking-template.md`
- 内容质量报告模板: `templates/content-quality-template.md`
- 成员成长报告模板: `templates/member-growth-template.md`

## 命令示例

```bash
# 获取指定日期范围的聊天记录
wechat-cli history "【AI 登山社】" --start-time "2026-04-07" --end-time "2026-04-09" --limit 1000 --format text

# 获取统计数据
wechat-cli stats "【AI 登山社】" --start-time "2026-04-07" --end-time "2026-04-09" --format text

# 获取群成员列表
wechat-cli members "【AI 登山社】" --format text
```

## 注意事项

1. **时间范围解析**: 
   - "今天" = 当天 00:00 - 现在
   - "昨天" = 昨天 00:00 - 23:59
   - "本周" = 本周一 00:00 - 今天
   - "上周" = 上周一 00:00 - 上周日 23:59

2. **群名称匹配**: 
   - 支持完整群名
   - 支持关键词匹配
   - 如果多个群匹配，让用户选择

3. **数据量限制**: 
   - 单次查询 limit=1000
   - 如超过则分批获取

4. **错误处理**: 
   - wechat-cli 未安装：提示安装
   - 群不存在：提示检查群名
   - 数据为空：提示时间范围可能无消息
