#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻抓取引擎
负责从多个源抓取新闻并进行初步过滤
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

# 添加路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / "shared"))
sys.path.insert(0, str(SCRIPT_DIR.parent / "parsers"))

from path_utils import get_sources_config, get_keywords_config, get_filters_config
from utils import url_hash, is_within_hours, calculate_relevance_score, print_progress
from rss_parser import parse_rss_source


class NewsFetcher:
    """新闻抓取引擎"""

    def __init__(self):
        self.sources = self._load_sources()
        self.keywords = self._load_keywords()
        self.filters = self._load_filters()
        self.seen_urls = set()

    def _load_sources(self) -> List[Dict[str, Any]]:
        """加载新闻源配置"""
        config_file = get_sources_config()
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return config.get('sources', [])
        except Exception as e:
            print(f"⚠️  加载sources.json失败: {e}")
            return []

    def _load_keywords(self) -> Dict[str, Any]:
        """加载关键词配置"""
        config_file = get_keywords_config()
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载keywords.json失败: {e}")
            return {"sectors": [], "companies": {}, "topics": []}

    def _load_filters(self) -> Dict[str, Any]:
        """加载过滤规则配置"""
        config_file = get_filters_config()
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  加载filters.json失败: {e}")
            return {"output_limits": {}, "time_filters": {}}

    def fetch_all(self, hours: int = 48) -> List[Dict[str, Any]]:
        """
        从所有启用的源抓取新闻

        Args:
            hours: 获取最近N小时内的新闻

        Returns:
            过滤后的文章列表
        """
        all_articles = []
        enabled_sources = [s for s in self.sources if s.get('enabled', True)]

        print(f"🔍 开始抓取 {len(enabled_sources)} 个新闻源 (最近{hours}小时)...")

        for i, source in enumerate(enabled_sources, 1):
            print(f"\n[{i}/{len(enabled_sources)}] {source['name']}...", end='', flush=True)

            try:
                articles = parse_rss_source(source, self.keywords)

                # 过滤
                filtered = self._filter_articles(articles, hours)

                # 去重
                new_articles = [a for a in filtered if a['url_hash'] not in self.seen_urls]
                for article in new_articles:
                    self.seen_urls.add(article['url_hash'])

                # 添加相关性评分
                for article in new_articles:
                    article['relevance_score'] = calculate_relevance_score(article, self.keywords)

                all_articles.extend(new_articles)
                print(f" ✅ {len(new_articles)}篇 (原始{len(articles)}篇)")

            except Exception as e:
                print(f" ❌ 失败: {e}")

        # 按相关性评分和时间排序
        all_articles.sort(key=lambda x: (x.get('relevance_score', 0), x.get('published') or datetime.min), reverse=True)

        print(f"\n✨ 总计获取 {len(all_articles)} 篇文章")
        return all_articles

    def _filter_articles(self, articles: List[Dict[str, Any]], hours: int) -> List[Dict[str, Any]]:
        """
        过滤文章

        过滤条件:
        1. 时效性: 在指定小时内
        2. 排除关键词: 不包含排除关键词
        3. 标题长度: 在合理范围内
        """
        time_filter = self.filters.get('time_filters', {})
        max_hours = time_filter.get('max_hours', hours)
        quality_filter = self.filters.get('quality_filters', {})

        min_title_len = quality_filter.get('min_title_length', 10)
        max_title_len = quality_filter.get('max_title_length', 200)

        # 构建排除关键词列表
        excluded = self.keywords.get('excluded_keywords', [])

        filtered = []
        for article in articles:
            # URL hash
            article['url_hash'] = url_hash(article['url'])

            # 时效性过滤
            pub_date = article.get('published')
            if pub_date and not is_within_hours(pub_date, max_hours):
                continue

            # 标题长度过滤
            title = article.get('title', '')
            if len(title) < min_title_len or len(title) > max_title_len:
                continue

            # 排除关键词过滤
            text_to_check = (title + ' ' + article.get('summary', '')).lower()
            if any(exc.lower() in text_to_check for exc in excluded):
                continue

            filtered.append(article)

        return filtered

    def get_top_events(self, articles: List[Dict[str, Any]], top_n: int = 20) -> List[Dict[str, Any]]:
        """
        获取最重要的N个事件

        排序依据: 相关性评分 + 发布时间
        """
        max_events = self.filters.get('output_limits', {}).get('max_total_events', top_n)
        return articles[:max_events]


def fetch_news(hours: int = 48) -> List[Dict[str, Any]]:
    """
    便捷函数: 抓取新闻

    Args:
        hours: 获取最近N小时内的新闻

    Returns:
        文章列表
    """
    fetcher = NewsFetcher()
    articles = fetcher.fetch_all(hours)
    return fetcher.get_top_events(articles)


if __name__ == "__main__":
    # 测试
    articles = fetch_news(hours=48)

    print(f"\n=== 获取到 {len(articles)} 篇文章 ===")
    for i, article in enumerate(articles[:10], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源: {article['source']} | 评分: {article.get('relevance_score', 0):.1f}")
        print(f"   链接: {article['url']}")
        if article.get('summary'):
            print(f"   摘要: {article['summary'][:100]}...")
