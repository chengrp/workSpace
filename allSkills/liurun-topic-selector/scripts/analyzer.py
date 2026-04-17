#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
事件分析模块
对抓取的新闻进行深度分析，提取关键信息、识别观点、评估影响力
"""

import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from collections import defaultdict

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "shared"))

from utils import extract_numbers, truncate_text, group_articles_by_topic
from path_utils import get_filters_config


class EventAnalyzer:
    """事件分析器"""

    def __init__(self):
        self.filters = self._load_filters()

    def _load_filters(self) -> Dict[str, Any]:
        """加载过滤配置"""
        config_file = get_filters_config()
        try:
            import json
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"output_limits": {}}

    def analyze_events(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        分析事件列表

        对每篇文章进行:
        1. 提取关键数据/数字
        2. 识别核心信息
        3. 评估热度/影响力

        Args:
            articles: 文章列表

        Returns:
            分析后的事件列表
        """
        analyzed = []

        for article in articles:
            event = self._analyze_single_event(article)
            analyzed.append(event)

        # 按影响力评分排序
        analyzed.sort(key=lambda x: x.get('impact_score', 0), reverse=True)

        return analyzed

    def _analyze_single_event(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析单个事件
        """
        title = article.get('title', '')
        summary = article.get('summary', '')
        source = article.get('source', '')

        # 提取关键数据
        key_numbers = extract_numbers(title + ' ' + summary)

        # 计算影响力评分
        impact_score = self._calculate_impact(article)

        # 识别事件类型
        event_type = self._classify_event(title + ' ' + summary)

        # 提取关键实体
        entities = self._extract_entities(title + ' ' + summary)

        return {
            'title': title,
            'url': article.get('url'),
            'summary': truncate_text(summary, 300),
            'source': source,
            'published': article.get('published'),
            'published_formatted': self._format_date(article.get('published')),
            'key_numbers': key_numbers,
            'impact_score': impact_score,
            'event_type': event_type,
            'entities': entities,
            'relevance_score': article.get('relevance_score', 0),
            'url_hash': article.get('url_hash', '')
        }

    def _calculate_impact(self, article: Dict[str, Any]) -> float:
        """
        计算事件影响力评分

        考虑因素:
        1. 相关性评分 (40%)
        2. 源权威性 (20%)
        3. 信息密度 (20%)
        4. 时效性 (20%)
        """
        score = 0.0

        # 相关性评分
        score += article.get('relevance_score', 0) * 0.4

        # 源权威性 (基于优先级)
        source = article.get('source', '')
        high_priority_sources = ['36氪', '虎嗅', '晚点LatePost', '财新', '界面新闻']
        if source in high_priority_sources:
            score += 20

        # 信息密度 (关键数据数量)
        title = article.get('title', '') + ' ' + article.get('summary', '')
        numbers = extract_numbers(title)
        score += min(len(numbers) * 5, 20)

        # 时效性 (越新越好)
        pub_date = article.get('published')
        if pub_date:
            hours_old = (datetime.now() - pub_date.replace(tzinfo=None)).total_seconds() / 3600
            if hours_old < 6:
                score += 20
            elif hours_old < 24:
                score += 15
            elif hours_old < 48:
                score += 10

        return min(score, 100)

    def _classify_event(self, text: str) -> str:
        """
        事件分类
        """
        text_lower = text.lower()

        if any(kw in text_lower for kw in ['融资', 'ipo', '上市', '投资', '收购', '并购']):
            return '投融资'
        elif any(kw in text_lower for kw in ['财报', '业绩', '营收', '利润', '季度']):
            return '财报业绩'
        elif any(kw in text_lower for kw in ['发布', '推出', '新品', '发布', '亮相']):
            return '产品发布'
        elif any(kw in text_lower for kw in ['战略合作', '合作', '联盟', '联手']):
            return '战略合作'
        elif any(kw in text_lower for kw in ['裁员', '关闭', '停止', '退出', '收缩']):
            return '组织调整'
        elif any(kw in text_lower for kw in ['调查', '处罚', '违规', '危机', '风波']):
            return '风险事件'
        elif any(kw in text_lower for kw in ['高管', 'ceo', '总裁', '任命', '离职']):
            return '人事变动'
        else:
            return '行业动态'

    def _extract_entities(self, text: str) -> List[str]:
        """
        提取关键实体 (公司名、人名等)
        """
        # 常见公司名列表
        companies = [
            'Tesla', '特斯拉', 'Nvidia', '英伟达', 'OpenAI',
            '比亚迪', '理想', '蔚来', '小鹏', '华为', '小米',
            '字节跳动', '抖音', '阿里', '腾讯', '美团', '京东',
            '拼多多', '快手', '百度', '大疆', '宁德时代',
            '苹果', '微软', '谷歌', '亚马逊', 'Meta'
        ]

        found = []
        text_lower = text.lower()
        for company in companies:
            if company.lower() in text_lower:
                found.append(company)

        return list(set(found))  # 去重

    def _format_date(self, dt: Optional[datetime]) -> str:
        """格式化日期"""
        if not dt:
            return "未知时间"
        return dt.strftime('%m-%d %H:%M')

    def get_deep_analysis_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        获取需要深度分析的事件

        选择标准:
        1. 高影响力评分
        2. 丰富的关键数据
        3. 重要的事件类型
        """
        max_deep = self.filters.get('output_limits', {}).get('max_deep_analysis', 10)

        # 优先选择高影响力事件
        high_impact = [e for e in events if e.get('impact_score', 0) >= 50]

        # 如果不够，补充中等影响力事件
        if len(high_impact) < max_deep:
            medium_impact = [e for e in events if 30 <= e.get('impact_score', 0) < 50]
            high_impact.extend(medium_impact[:max_deep - len(high_impact)])

        return high_impact[:max_deep]

    def group_by_source(self, events: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """按来源分组事件"""
        groups = defaultdict(list)
        for event in events:
            groups[event['source']].append(event)
        return dict(groups)

    def get_topic_summary(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成话题摘要统计
        """
        # 按事件类型统计
        type_counts = defaultdict(int)
        for event in events:
            type_counts[event['event_type']] += 1

        # 按来源统计
        source_counts = defaultdict(int)
        for event in events:
            source_counts[event['source']] += 1

        # 提取最常出现的实体
        all_entities = []
        for event in events:
            all_entities.extend(event['entities'])

        from collections import Counter
        top_entities = Counter(all_entities).most_common(10)

        return {
            'total_events': len(events),
            'by_type': dict(type_counts),
            'by_source': dict(source_counts),
            'top_entities': top_entities
        }


def analyze_events(articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    便捷函数: 分析事件
    """
    analyzer = EventAnalyzer()
    return analyzer.analyze_events(articles)


if __name__ == "__main__":
    # 测试
    from fetcher import fetch_news

    articles = fetch_news(hours=48)
    events = analyze_events(articles)

    print(f"\n=== 分析完成 ===")
    print(f"总计 {len(events)} 个事件\n")

    analyzer = EventAnalyzer()
    summary = analyzer.get_topic_summary(events)

    print("事件类型分布:")
    for event_type, count in summary['by_type'].items():
        print(f"  {event_type}: {count}")

    print("\n来源分布:")
    for source, count in summary['by_source'].items():
        print(f"  {source}: {count}")

    print("\n高频实体:")
    for entity, count in summary['top_entities']:
        print(f"  {entity}: {count}")
