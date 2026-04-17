#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
报告生成模块
生成结构化的Markdown报告
"""

import sys
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "shared"))

from path_utils import get_daily_report_path, get_recommendations_path


class ReportGenerator:
    """报告生成器"""

    def __init__(self):
        self.report_date = datetime.now().strftime('%Y-%m-%d')
        self.report_time = datetime.now().strftime('%H:%M')

    def generate_daily_report(self, events: List[Dict[str, Any]], summary: Dict[str, Any]) -> str:
        """
        生成每日报告

        包含三部分:
        1. 今日最重要的20个商业事件概览
        2. 其中最重要的5-10个关键事件深度分析
        3. Top3选题建议与写作角度
        """
        lines = []

        # 报告头部
        lines.append("# 📊 刘润公众号选题日报")
        lines.append("")
        lines.append(f"> 📅 日期: {self.report_date}")
        lines.append(f"> 🕐 时间: {self.report_time}")
        lines.append(f"> 📈 总计事件: {summary.get('total_events', 0)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Part 1: 事件概览
        lines.extend(self._generate_events_overview(events))
        lines.append("")

        # Part 2: 深度分析 (取高影响力事件)
        lines.extend(self._generate_deep_analysis(events[:10]))
        lines.append("")

        # Part 3: 选题推荐
        lines.extend(self._generate_recommendations_placeholder())

        report = '\n'.join(lines)
        return report

    def _generate_events_overview(self, events: List[Dict[str, Any]]) -> List[str]:
        """生成事件概览部分"""
        lines = []
        lines.append("## 📰 Part 1: 今日最重要的商业事件概览")
        lines.append("")
        lines.append(f"**总计 {len(events)} 个事件** (按影响力排序)")
        lines.append("")

        for i, event in enumerate(events, 1):
            lines.append(f"### {i}. {event['title']}")
            lines.append("")
            lines.append(f"- **来源**: {event['source']}")
            lines.append(f"- **时间**: {event['published_formatted']}")
            lines.append(f"- **类型**: {event['event_type']}")
            lines.append(f"- **影响力**: {event['impact_score']:.1f}")

            if event.get('key_numbers'):
                lines.append(f"- **关键数据**: {', '.join(event['key_numbers'][:5])}")

            if event.get('entities'):
                lines.append(f"- **相关实体**: {', '.join(event['entities'][:5])}")

            if event.get('summary'):
                lines.append(f"- **摘要**: {event['summary']}")

            lines.append(f"- **链接**: [{event['url']}]({event['url']})")
            lines.append("")

        return lines

    def _generate_deep_analysis(self, events: List[Dict[str, Any]]) -> List[str]:
        """生成深度分析部分"""
        lines = []
        lines.append("## 🔍 Part 2: 关键事件深度分析")
        lines.append("")
        lines.append("*以下事件由Claude进行深度分析*")
        lines.append("")
        lines.append("```")
        lines.append("CLAUDE_ACTION_REQUIRED: DEEP_ANALYSIS")
        lines.append("")
        lines.append("请对以下事件进行深度分析，为每个事件添加:")
        lines.append("1. 精炼概要 - 用2-3句话概括事件核心")
        lines.append("2. 关键数据/事实 - 提取具体数字和事实")
        lines.append("3. 多方观点 - 识别不同媒体/专家的观点")
        lines.append("4. 主要争议点 - 找出事件中的争议或不同看法")
        lines.append("")
        lines.append("等待分析的事件:")
        lines.append("```")
        lines.append("")

        for i, event in enumerate(events, 1):
            lines.append(f"### 事件 {i}: {event['title']}")
            lines.append("")
            lines.append(f"**基本信息**:")
            lines.append(f"- 来源: {event['source']}")
            lines.append(f"- 时间: {event['published_formatted']}")
            lines.append(f"- 类型: {event['event_type']}")
            lines.append(f"- 链接: {event['url']}")
            lines.append("")
            lines.append(f"**原始摘要**: {event['summary']}")
            lines.append("")

            if event.get('key_numbers'):
                lines.append(f"**关键数据**: {', '.join(event['key_numbers'])}")
                lines.append("")

            if event.get('entities'):
                lines.append(f"**相关实体**: {', '.join(event['entities'])}")
                lines.append("")

            lines.append("**📝 待补充深度分析**:")
            lines.append("- [ ] 精炼概要")
            lines.append("- [ ] 关键数据/事实")
            lines.append("- [ ] 多方观点")
            lines.append("- [ ] 主要争议点")
            lines.append("")

        return lines

    def _generate_recommendations_placeholder(self) -> List[str]:
        """生成选题推荐占位符"""
        lines = []
        lines.append("## ✨ Part 3: Top3选题建议与写作角度")
        lines.append("")
        lines.append("*选题推荐将在选题模块生成后自动填充*")
        lines.append("")
        lines.append("```")
        lines.append("CLAUDE_ACTION_REQUIRED: GENERATE_RECOMMENDATIONS")
        lines.append("")
        lines.append("运行以下命令生成选题推荐:")
        lines.append("```bash")
        lines.append("cd CC_record/skills/liurun-topic-selector/scripts")
        lines.append("python selector.py")
        lines.append("```")
        lines.append("```")
        lines.append("")

        return lines

    def generate_recommendations_report(self, topics: List[Dict[str, Any]]) -> str:
        """生成选题推荐报告"""
        lines = []

        lines.append("# ✨ 刘润风格选题推荐")
        lines.append("")
        lines.append(f"> 📅 生成时间: {self.report_date} {self.report_time}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for i, topic in enumerate(topics, 1):
            lines.append(f"## 选题 {i}: {topic['topic_name']}")
            lines.append("")

            lines.append(f"**核心事件**: {topic['core_event']}")
            lines.append("")
            lines.append(f"**事件类型**: {topic['event_type']}")
            lines.append("")
            lines.append(f"**来源**: {topic['source']} | **时间**: {topic['published']}")
            lines.append("")
            lines.append(f"**推荐理由**: {topic['recommendation_reason']}")
            lines.append("")
            lines.append(f"**刘润适配度**: {topic['liurun_score']:.1f}/100")
            lines.append("")

            lines.append("### 📝 写作角度")
            lines.append("")

            angles = topic.get('writing_angles', {})
            lines.append(f"- **切入点**: {angles.get('切入点', '')}")
            lines.append(f"- **核心探讨问题**: {angles.get('核心探讨问题', '')}")
            lines.append(f"- **类比案例**: {angles.get('类比案例', '')}")
            lines.append(f"- **潜在启发**: {angles.get('潜在启发', '')}")
            lines.append("")

            if topic.get('key_data'):
                lines.append(f"**关键数据**: {', '.join(topic['key_data'])}")
                lines.append("")

            lines.append(f"**参考链接**: [{topic['url']}]({topic['url']})")
            lines.append("")
            lines.append("---")
            lines.append("")

        return '\n'.join(lines)

    def save_reports(self, events: List[Dict[str, Any]], summary: Dict[str, Any], topics: List[Dict[str, Any]] = None):
        """保存报告到文件"""
        # 生成每日报告
        daily_report = self.generate_daily_report(events, summary)
        report_path = get_daily_report_path()

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(daily_report)

        print(f"\n📄 每日报告已保存: {report_path}")

        # 如果有选题，生成选题报告
        if topics:
            rec_report = self.generate_recommendations_report(topics)
            rec_path = get_recommendations_path()

            with open(rec_path, 'w', encoding='utf-8') as f:
                f.write(rec_report)

            print(f"📄 选题报告已保存: {rec_path}")


def print_terminal_summary(events: List[Dict[str, Any]], summary: Dict[str, Any], topics: List[Dict[str, Any]] = None):
    """在终端打印摘要"""
    print("\n" + "=" * 60)
    print("📊 刘润公众号选题智能体 - 报告摘要")
    print("=" * 60)

    print(f"\n📈 事件统计:")
    print(f"   总计事件: {summary.get('total_events', 0)}")

    if summary.get('by_type'):
        print(f"\n   事件类型分布:")
        for event_type, count in sorted(summary['by_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"   • {event_type}: {count}")

    if summary.get('top_entities'):
        print(f"\n   高频实体:")
        for entity, count in summary['top_entities'][:5]:
            print(f"   • {entity}: {count}次")

    print(f"\n🔥 Top 5 事件:")
    for i, event in enumerate(events[:5], 1):
        print(f"   {i}. [{event['event_type']}] {event['title'][:50]}...")
        print(f"      来源: {event['source']} | 影响力: {event['impact_score']:.1f}")

    if topics:
        print(f"\n✨ Top {len(topics)} 选题推荐:")
        for i, topic in enumerate(topics, 1):
            print(f"   {i}. {topic['topic_name']}")
            print(f"      理由: {topic['recommendation_reason'][:60]}...")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 测试
    from fetcher import fetch_news
    from analyzer import analyze_events, EventAnalyzer
    from selector import select_topics

    articles = fetch_news(hours=48)
    events = analyze_events(articles)

    analyzer = EventAnalyzer()
    summary = analyzer.get_topic_summary(events)

    topics = select_topics(events, top_n=3)

    # 生成报告
    generator = ReportGenerator()
    generator.save_reports(events, summary, topics)

    # 终端输出
    print_terminal_summary(events, summary, topics)
