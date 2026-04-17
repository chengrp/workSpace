#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题推荐模块
基于"类刘润"风格筛选和推荐选题
"""

import sys
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path
from collections import defaultdict

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "shared"))

from path_utils import get_keywords_config, get_filters_config


class TopicSelector:
    """选题推荐器 - 类刘润风格"""

    def __init__(self):
        self.keywords = self._load_keywords()
        self.filters = self._load_filters()

    def _load_keywords(self) -> Dict[str, Any]:
        """加载关键词配置"""
        import json
        config_file = get_keywords_config()
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载keywords失败: {e}")
            return {}

    def _load_filters(self) -> Dict[str, Any]:
        """加载过滤配置"""
        import json
        config_file = get_filters_config()
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"output_limits": {}}

    def select_topics(self, events: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
        """
        选择Top N选题

        类刘润风格筛选标准:
        1. 微观切入 - 从小事件看大逻辑
        2. 深度洞察 - 能提炼规律/方法论
        3. 启发思考 - 给读者新认知
        4. 素材丰富 - 有足够事实和数据

        Args:
            events: 分析后的事件列表
            top_n: 返回选题数量

        Returns:
            选题列表
        """
        # 计算每个事件的"刘润风格"适配度
        scored_events = []
        for event in events:
            score = self._calculate_liurun_score(event)
            scored_events.append({**event, 'liurun_score': score})

        # 按评分排序
        scored_events.sort(key=lambda x: x.get('liurun_score', 0), reverse=True)

        # 选择Top N
        max_rec = self.filters.get('output_limits', {}).get('max_recommendations', top_n)
        selected = scored_events[:max_rec]

        # 为每个选题生成写作角度
        recommendations = []
        for event in selected:
            recommendation = self._generate_recommendation(event)
            recommendations.append(recommendation)

        return recommendations

    def _calculate_liurun_score(self, event: Dict[str, Any]) -> float:
        """
        计算"类刘润"风格适配度评分

        评分维度:
        1. 微观性 (0-25): 是否有具体场景/切入点
        2. 深度性 (0-25): 能否提炼方法论
        3. 启发性 (0-25): 是否给读者新认知
        4. 素材性 (0-25): 事实数据是否充足
        """
        score = 0.0
        title = event.get('title', '').lower()
        summary = event.get('summary', '').lower()
        text = title + ' ' + summary

        # 1. 微观性: 有具体场景/故事
        micro_keywords = ['如何', '怎样', '从', '案例', '故事', '揭秘', '背后']
        if any(kw in text for kw in micro_keywords):
            score += 15
        elif len(event.get('key_numbers', [])) > 0:
            score += 10  # 有具体数字也算微观

        # 2. 深度性: 能提炼规律/方法论
        depth_keywords = ['本质', '逻辑', '规律', '方法论', '思维', '模式', '策略']
        score += min(sum(5 for kw in depth_keywords if kw in text), 25)

        # 3. 启发性: 给读者新认知
        insight_keywords = ['为什么', '启示', '思考', '颠覆', '重新', '新的', '首次']
        score += min(sum(5 for kw in insight_keywords if kw in text), 25)

        # 4. 素材性: 事实数据充足
        if event.get('key_numbers'):
            score += min(len(event['key_numbers']) * 5, 25)
        elif len(summary) > 100:
            score += 10

        return score

    def _generate_recommendation(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        为事件生成选题推荐

        生成:
        1. 选题名称 (类刘润风格标题)
        2. 核心事件
        3. 推荐理由
        4. 写作角度
        """
        title = event.get('title', '')
        event_type = event.get('event_type', '')
        entities = event.get('entities', [])

        # 生成选题名称 (类刘润风格)
        topic_name = self._generate_topic_name(title, event_type, entities)

        # 推荐理由
        reason = self._generate_reason(event)

        # 写作角度
        angles = self._generate_writing_angles(event, topic_name)

        return {
            'topic_name': topic_name,
            'core_event': title,
            'event_type': event_type,
            'source': event.get('source', ''),
            'url': event.get('url', ''),
            'published': event.get('published_formatted', ''),
            'recommendation_reason': reason,
            'writing_angles': angles,
            'key_data': event.get('key_numbers', []),
            'liurun_score': event.get('liurun_score', 0),
            'related_events': []  # 可关联的相关事件
        }

    def _generate_topic_name(self, title: str, event_type: str, entities: List[str]) -> str:
        """
        生成类刘润风格的选题名称

        常用模式:
        - "从[事件]看懂[逻辑]"
        - "拆解[现象]背后[因素]"
        - "[决策]带来何种启发"
        - "[公司/人物]的[战略/选择]"
        """
        # 尝试从标题提取核心
        if event_type == '投融资':
            for entity in entities:
                return f"从{entity}的融资看懂{event_type}背后的逻辑"
            return f"从这次融资看懂{event_type}背后的逻辑"

        elif event_type == '财报业绩':
            for entity in entities:
                return f"拆解{entity}财报背后的增长逻辑"
            return "拆解财报数据背后的商业逻辑"

        elif event_type == '产品发布':
            for entity in entities:
                return f"从{entity}新品发布看行业趋势"
            return "从新品发布看行业创新趋势"

        elif event_type == '战略合作':
            for entity in entities:
                return f"从{entity}的合作看战略格局变化"
            return "从战略合作看行业格局变化"

        elif event_type == '组织调整':
            for entity in entities:
                return f"从{entity}的组织调整看企业转型"
            return "从组织调整看企业生存逻辑"

        else:
            # 默认模式
            if entities:
                return f"从{entities[0]}看懂行业变化"
            return "从事件背后看懂商业逻辑"

    def _generate_reason(self, event: Dict[str, Any]) -> str:
        """生成推荐理由"""
        reasons = []

        # 时效性
        published = event.get('published')
        if published:
            hours_ago = (datetime.now() - published.replace(tzinfo=None)).total_seconds() / 3600
            if hours_ago < 6:
                reasons.append("🔥 刚刚发生，时效性极强")
            elif hours_ago < 24:
                reasons.append("⏰ 24小时内发生，正处讨论期")

        # 影响力
        impact = event.get('impact_score', 0)
        if impact >= 70:
            reasons.append(f"📊 影响力评分{impact:.0f}，关注度极高")
        elif impact >= 50:
            reasons.append(f"📈 影响力评分{impact:.0f}，行业关注")

        # 数据丰富度
        key_data = event.get('key_numbers', [])
        if key_data:
            reasons.append(f"🔢 包含{len(key_data)}个关键数据，素材丰富")

        # 实体重要性
        entities = event.get('entities', [])
        important_entities = ['Tesla', '特斯拉', 'Nvidia', '英伟达', '华为', '小米', '比亚迪']
        for entity in entities:
            if entity in important_entities:
                reasons.append(f"🏢 涉及{entity}，行业焦点")
                break

        # 事件类型
        event_type = event.get('event_type', '')
        if event_type in ['投融资', '财报业绩', '产品发布']:
            reasons.append(f"📌 {event_type}类事件，商业价值高")

        return " | ".join(reasons) if reasons else "具有观察价值的事件"

    def _generate_writing_angles(self, event: Dict[str, Any], topic_name: str) -> Dict[str, str]:
        """
        生成写作角度

        包含:
        1. 切入点: 具体场景或问题
        2. 核心探讨问题: 本质是什么
        3. 类比案例: 生活化类比
        4. 潜在启发/结论: 读者能获得什么
        """
        title = event.get('title', '')
        event_type = event.get('event_type', '')
        entities = event.get('entities', [])

        # 根据事件类型生成不同的写作角度
        if event_type == '投融资':
            return {
                '切入点': f"从{entities[0] if entities else '公司'}获得融资的具体场景入手",
                '核心探讨问题': "资本市场为什么看好这个领域？资金的流向说明了什么？",
                '类比案例': "就像当年互联网泡沫前的投资热潮，历史总是押韵的",
                '潜在启发': "理解资本背后的判断逻辑，把握行业发展趋势"
            }

        elif event_type == '财报业绩':
            return {
                '切入点': f"从财报中的关键数字变化切入",
                '核心探讨问题': "增长/下滑背后的真正原因是什么？",
                '类比案例': "就像看一个人的体检报告，数字背后是健康状况",
                '潜在启发': "学会从财报看企业健康度，理解商业模式"
            }

        elif event_type == '产品发布':
            return {
                '切入点': f"从{entities[0] if entities else '公司'}新品的功能特性切入",
                '核心探讨问题': "这个产品解决了什么问题？反映了什么趋势？",
                '类比案例': "就像手机取代相机，产品创新往往预示着时代变革",
                '潜在启发': "理解产品创新背后的用户需求变化"
            }

        elif event_type == '战略合作':
            return {
                '切入点': f"从{entities[0] if entities else '公司'}之间的合作细节切入",
                '核心探讨问题': "为什么是这两家公司合作？背后反映了什么战略意图？",
                '类比案例': "就像两家餐厅合并为一家美食广场，1+1可能大于2",
                '潜在启发': "理解商业合作背后的战略思考和博弈"
            }

        elif event_type == '组织调整':
            return {
                '切入点': f"从{entities[0] if entities else '公司'}组织变动的具体举措切入",
                '核心探讨问题': "企业为什么在这个时候做组织调整？",
                '类比案例': "就像园丁修剪树枝，短期的痛是为了长期的生长",
                '潜在启发': "理解企业生命周期中的必经阶段和应对之道"
            }

        else:
            return {
                '切入点': f"从事件中的具体场景/细节切入",
                '核心探讨问题': "这个事件反映了什么深层逻辑？",
                '类比案例': "用生活中的类似现象类比，帮助读者理解",
                '潜在启发': "给读者带来新的认知视角和思考框架"
            }


def select_topics(events: List[Dict[str, Any]], top_n: int = 3) -> List[Dict[str, Any]]:
    """
    便捷函数: 选择选题
    """
    selector = TopicSelector()
    return selector.select_topics(events, top_n)


if __name__ == "__main__":
    # 测试
    from fetcher import fetch_news
    from analyzer import analyze_events

    articles = fetch_news(hours=48)
    events = analyze_events(articles)
    topics = select_topics(events, top_n=3)

    print(f"\n=== Top {len(topics)} 选题推荐 ===\n")
    for i, topic in enumerate(topics, 1):
        print(f"{i}. {topic['topic_name']}")
        print(f"   核心事件: {topic['core_event']}")
        print(f"   推荐理由: {topic['recommendation_reason']}")
        print(f"   刘润适配度: {topic['liurun_score']:.1f}")
        print()
