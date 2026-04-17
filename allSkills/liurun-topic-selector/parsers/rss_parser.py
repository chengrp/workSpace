#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用RSS解析器
"""

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin

# 尝试导入feedparser，如果不存在则提供降级方案
try:
    import feedparser
except ImportError:
    feedparser = None
    import subprocess
    import json

# 添加shared目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "shared"))

from utils import parse_time_str, clean_html


def parse_rss_source(source_config: Dict[str, Any], keywords: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    解析RSS/Atom新闻源

    Args:
        source_config: 源配置字典
            - url: RSS feed URL
            - name: 源名称
            - limit: 最大获取条数

    Returns:
        文章列表，每篇文章包含:
        {
            'title': 标题,
            'url': 链接,
            'published': 发布时间(datetime),
            'summary': 摘要,
            'source': 源名称,
            'raw_data': 原始数据
        }
    """
    if feedparser is None:
        print(f"  ⚠️  feedparser未安装，尝试使用备用方法...")
        return parse_rss_fallback(source_config)

    url = source_config.get('url')
    name = source_config.get('name', 'Unknown')
    limit = source_config.get('limit', 20)

    if not url:
        return []

    try:
        feed = feedparser.parse(url)

        if feed.bozo:
            # feed有错误，但可能仍有有效内容
            print(f"  ⚠️  {name}: Feed解析警告: {feed.bozo_exception}")

        articles = []
        for entry in feed.entries[:limit]:
            # 解析发布时间
            published = None
            if hasattr(entry, 'published'):
                published = parse_time_str(entry.published)
            elif hasattr(entry, 'updated'):
                published = parse_time_str(entry.updated)

            # 获取链接
            article_url = entry.get('link')
            if not article_url and hasattr(entry, 'links') and entry.links:
                article_url = entry.links[0].get('href')

            # 清理摘要
            summary = entry.get('summary', '')
            if summary:
                summary = clean_html(summary)
            elif hasattr(entry, 'description'):
                summary = clean_html(entry.description)
            elif hasattr(entry, 'content') and entry.content:
                summary = clean_html(entry.content[0].get('value', ''))

            articles.append({
                'title': entry.get('title', '无标题'),
                'url': article_url,
                'published': published,
                'summary': summary[:500] if summary else '',  # 限制摘要长度
                'source': name,
                'author': entry.get('author', ''),
                'tags': [tag.term for tag in entry.get('tags', [])] if hasattr(entry, 'tags') else [],
                'raw_data': {
                    'feed_title': feed.feed.get('title', ''),
                }
            })

        return articles

    except Exception as e:
        print(f"  ❌ {name} 解析失败: {e}")
        return []


def parse_rss_fallback(source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    备用RSS解析方法（使用curl + xml解析）
    当feedparser不可用时使用
    """
    import subprocess
    import xml.etree.ElementTree as ET

    url = source_config.get('url')
    name = source_config.get('name', 'Unknown')
    limit = source_config.get('limit', 20)

    try:
        # 使用curl获取RSS内容
        result = subprocess.run(
            ['curl', '-s', '-L', '--max-time', '30', url],
            capture_output=True,
            text=True,
            timeout=35
        )

        if result.returncode != 0:
            print(f"  ❌ {name}: curl请求失败")
            return []

        xml_content = result.stdout

        # 解析XML
        root = ET.fromstring(xml_content)

        # RSS或Atom格式
        items = []
        if root.tag == 'rss':
            channel = root.find('channel')
            if channel is not None:
                items = channel.findall('item')
        else:
            # Atom格式
            items = root.findall('{http://www.w3.org/2005/Atom}entry')

        articles = []
        for item in items[:limit]:
            # 解析各字段（处理RSS和Atom的差异）
            title_elem = item.find('title') or item.find('{http://www.w3.org/2005/Atom}title')
            link_elem = item.find('link') or item.find('{http://www.w3.org/2005/Atom}link')
            desc_elem = item.find('description') or item.find('{http://www.w3.org/2005/Atom}summary')
            date_elem = item.find('pubDate') or item.find('{http://www.w3.org/2005/Atom}published')

            title = title_elem.text if title_elem is not None else '无标题'
            url = link_elem.text if link_elem is not None and link_elem.text else \
                  (link_elem.get('href') if link_elem is not None else '')

            summary = clean_html(desc_elem.text) if desc_elem is not None and desc_elem.text else ''
            published = parse_time_str(date_elem.text) if date_elem is not None and date_elem.text else None

            articles.append({
                'title': title,
                'url': url,
                'published': published,
                'summary': summary[:500] if summary else '',
                'source': name,
                'author': '',
                'tags': [],
                'raw_data': {}
            })

        return articles

    except Exception as e:
        print(f"  ❌ {name} 备用解析失败: {e}")
        return []


def detect_and_parse(url: str, name: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    自动检测并解析RSS源

    尝试多种解析方法，返回第一个成功的结果
    """
    source_config = {
        'url': url,
        'name': name,
        'limit': limit
    }

    # 首选feedparser
    if feedparser is not None:
        result = parse_rss_source(source_config)
        if result:
            return result

    # 备用方法
    return parse_rss_fallback(source_config)


if __name__ == "__main__":
    # 测试代码
    import json
    from pathlib import Path

    # 读取配置
    config_path = Path(__file__).parent.parent / "config" / "sources.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    print("测试RSS解析器...")
    for source in config['sources'][:3]:  # 测试前3个
        if source.get('enabled', True):
            print(f"\n测试 {source['name']}...")
            articles = parse_rss_source(source)
            print(f"  解析到 {len(articles)} 篇文章")
            if articles:
                print(f"  示例: {articles[0]['title']}")
