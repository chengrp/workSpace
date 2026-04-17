#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
共享工具函数
"""

import sys
import hashlib
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path


def url_hash(url: str) -> str:
    """生成URL的短hash用于去重"""
    return hashlib.md5(url.encode()).hexdigest()[:12]


def parse_time_str(time_str: str) -> Optional[datetime]:
    """
    解析各种时间格式字符串
    支持RSS常见的时间格式
    """
    if not time_str:
        return None

    # 常见时间格式列表
    formats = [
        '%a, %d %b %Y %H:%M:%S %Z',      # RFC 822 (with timezone)
        '%a, %d %b %Y %H:%M:%S %z',      # RFC 822 (with numeric timezone)
        '%a, %d %b %Y %H:%M:%S',         # RFC 822 (no timezone)
        '%Y-%m-%dT%H:%M:%S%z',           # ISO 8601
        '%Y-%m-%dT%H:%M:%SZ',            # ISO 8601 (UTC)
        '%Y-%m-%dT%H:%M:%S',             # ISO 8601 (no timezone)
        '%Y-%m-%d %H:%M:%S',             # Standard datetime
        '%Y-%m-%d',                      # Date only
    ]

    for fmt in formats:
        try:
            return datetime.strptime(time_str.strip(), fmt)
        except ValueError:
            continue

    return None


def is_within_hours(pub_date: Optional[datetime], hours: int = 48) -> bool:
    """判断发布时间是否在指定小时内"""
    if not pub_date:
        return True  # 无法解析时间时默认保留

    now = datetime.now(pub_date.tzinfo) if pub_date.tzinfo else datetime.now()
    delta = now - pub_date.replace(tzinfo=None) if pub_date.tzinfo else now - pub_date
    return delta.total_seconds() <= hours * 3600


def extract_numbers(text: str) -> List[str]:
    """提取文本中的数字和单位（如：10亿、50%、3.2万）"""
    patterns = [
        r'\d+\.?\d*[万亿千百]+',  # 中文数字单位
        r'\d+\.?\d*%',            # 百分比
        r'\d+\.?\d*[美元美金元]',  # 金额
        r'\d{4}年\d{1,2}月',      # 日期
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, text))
    return results


def clean_html(text: str) -> str:
    """清理HTML标签"""
    if not text:
        return ""
    # 简单的HTML标签清理
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def truncate_text(text: str, max_length: int = 200) -> str:
    """截断文本到指定长度"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def calculate_relevance_score(article: Dict[str, Any], keywords: Dict[str, List[str]]) -> float:
    """
    计算文章相关性评分

    Args:
        article: 文章数据（包含title, summary等）
        keywords: 关键词配置

    Returns:
        相关性评分 (0-100)
    """
    score = 0.0
    text = (article.get('title', '') + ' ' + article.get('summary', '')).lower()

    # 领域匹配
    for sector in keywords.get('sectors', []):
        if sector.lower() in text:
            score += 15

    # 公司匹配（高权重）
    all_companies = []
    for category in keywords.get('companies', {}).values():
        all_companies.extend(category)
    for company in all_companies:
        if company.lower() in text:
            score += 20

    # 话题匹配
    for topic in keywords.get('topics', []):
        if topic.lower() in text:
            score += 10

    return min(score, 100)


def format_datetime(dt: Optional[datetime]) -> str:
    """格式化日期时间显示"""
    if not dt:
        return "未知时间"
    return dt.strftime('%Y-%m-%d %H:%M')


def group_articles_by_topic(articles: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    按话题对文章进行聚类

    基于标题相似度和关键词重叠度
    """
    groups = {"其他": []}

    for article in articles:
        title = article.get('title', '').lower()
        assigned = False

        # 简单的关键词分组
        if any(kw in title for kw in ['ai', '人工智能', '大模型', 'gpt', 'chatgpt']):
            groups.setdefault('AI', []).append(article)
            assigned = True
        elif any(kw in title for kw in ['汽车', '新能源', '电动', '自动驾驶', 'tesla', '特斯拉', '比亚迪']):
            groups.setdefault('新能源车', []).append(article)
            assigned = True
        elif any(kw in title for kw in ['手机', '芯片', '华为', '苹果', '小米', '发布']):
            groups.setdefault('科技硬件', []).append(article)
            assigned = True
        elif any(kw in title for kw in ['融资', 'ipo', '上市', '投资', '收购']):
            groups.setdefault('投融资', []).append(article)
            assigned = True
        elif any(kw in title for kw in ['财报', '业绩', '营收', '利润']):
            groups.setdefault('财报业绩', []).append(article)
            assigned = True

        if not assigned:
            groups["其他"].append(article)

    # 移除空分组
    return {k: v for k, v in groups.items() if v}


def print_progress(current: int, total: int, prefix: str = ""):
    """打印进度条"""
    if total > 0:
        percent = int(100 * current / total)
        bar = '█' * (percent // 5) + '░' * (20 - percent // 5)
        print(f"\r{prefix}[{bar}] {percent}%", end='', flush=True)
        if current == total:
            print()  # 完成后换行
