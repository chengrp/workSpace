#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
刘润公众号选题智能体 - 主入口

研究中国市场重大事件，生成深度选题建议和写作角度

使用方法:
    python main.py [hours]

    hours: 获取最近N小时内的新闻 (默认48)
"""

import sys
import os

from datetime import datetime
from pathlib import Path

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from fetcher import NewsFetcher
from analyzer import EventAnalyzer
from selector import TopicSelector
from reporter import ReportGenerator, print_terminal_summary


def main(hours: int = 48):
    """
    主流程

    1. 抓取新闻
    2. 分析事件
    3. 选择选题
    4. 生成报告
    """
    print("=" * 60)
    print("🚀 刘润公众号选题智能体")
    print("=" * 60)
    print(f"\n⏰ 时间范围: 最近 {hours} 小时")
    print(f"📅 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Step 1: 抓取新闻
    print("\n" + "=" * 60)
    print("📡 Step 1: 抓取新闻")
    print("=" * 60)

    fetcher = NewsFetcher()
    articles = fetcher.fetch_all(hours)

    if not articles:
        print("\n⚠️  没有获取到文章，请检查:")
        print("   1. 网络连接")
        print("   2. RSS源是否可用")
        print("   3. 时间范围是否过小")
        return

    # Step 2: 分析事件
    print("\n" + "=" * 60)
    print("🔍 Step 2: 分析事件")
    print("=" * 60)

    analyzer = EventAnalyzer()
    events = analyzer.analyze_events(articles)
    summary = analyzer.get_topic_summary(events)

    print(f"\n✅ 分析完成:")
    print(f"   总计事件: {len(events)}")
    print(f"   高影响力事件: {len([e for e in events if e.get('impact_score', 0) >= 50])}")

    # Step 3: 选择选题
    print("\n" + "=" * 60)
    print("✨ Step 3: 选择选题")
    print("=" * 60)

    selector = TopicSelector()
    topics = selector.select_topics(events, top_n=3)

    print(f"\n✅ 选出 {len(topics)} 个选题:")
    for i, topic in enumerate(topics, 1):
        print(f"   {i}. {topic['topic_name']} (适配度: {topic['liurun_score']:.1f})")

    # Step 4: 生成报告
    print("\n" + "=" * 60)
    print("📄 Step 4: 生成报告")
    print("=" * 60)

    generator = ReportGenerator()
    generator.save_reports(events, summary, topics)

    # 终端输出
    print_terminal_summary(events, summary, topics)

    print("\n✨ 完成!")
    print(f"\n📁 报告位置:")
    print(f"   每日报告: {generator.get_daily_report_path()}")
    print(f"   选题报告: {generator.get_recommendations_path()}")

    # 提示下一步
    print("\n" + "=" * 60)
    print("🚨 CLAUDE_ACTION_REQUIRED: 深度分析")
    print("=" * 60)
    print("\n请对 daily_report.md 中的事件进行深度分析:")
    print("1. 精炼概要")
    print("2. 关键数据/事实")
    print("3. 多方观点")
    print("4. 主要争议点")
    print("\n分析完成后，报告将自动更新。")


if __name__ == "__main__":
    hours = 48
    if len(sys.argv) > 1:
        try:
            hours = int(sys.argv[1])
        except ValueError:
            print("⚠️  参数错误，使用默认值48小时")
            print("   用法: python main.py [hours]")

    try:
        main(hours)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
