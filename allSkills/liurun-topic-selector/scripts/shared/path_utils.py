#!/usr/bin/env python3
"""
路径配置管理
"""

import sys
import io
from pathlib import Path

# Windows encoding fix
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def get_skill_root() -> Path:
    """获取技能根目录"""
    return Path(__file__).parent.parent.parent


def get_config_dir() -> Path:
    """获取配置目录"""
    return get_skill_root() / "config"


def get_output_dir() -> Path:
    """获取输出目录"""
    output_dir = get_skill_root() / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def get_state_file() -> Path:
    """获取状态文件路径"""
    state_dir = get_skill_root() / "data"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir / "state.json"


def get_daily_report_path() -> Path:
    """获取每日报告文件路径"""
    return get_output_dir() / "daily_report.md"


def get_recommendations_path() -> Path:
    """获取选题推荐文件路径"""
    return get_output_dir() / "topics_recommendations.md"


def get_sources_config() -> Path:
    """获取新闻源配置文件路径"""
    return get_config_dir() / "sources.json"


def get_keywords_config() -> Path:
    """获取关键词配置文件路径"""
    return get_config_dir() / "keywords.json"


def get_filters_config() -> Path:
    """获取过滤规则配置文件路径"""
    return get_config_dir() / "filters.json"
