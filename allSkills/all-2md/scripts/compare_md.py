#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
比较 MD 文件的标题结构
"""
import re
from pathlib import Path

def extract_headers(md_path):
    """提取 MD 文件中的所有标题"""
    headers = []
    with open(md_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if line.startswith('#'):
                # 提取标题级别和内容
                match = re.match(r'^(#+)\s+(.+)$', line)
                if match:
                    level = len(match.group(1))
                    content = match.group(2)
                    headers.append((i, level, content))
    return headers

def main():
    v5_path = r"C:\Users\RyanCh\Desktop\books\以日为鉴_v5.md"
    standard_path = r"C:\Users\RyanCh\Desktop\books\以日为鉴md版.txt"

    v5_headers = extract_headers(v5_path)
    standard_headers = extract_headers(standard_path)

    print("=" * 80)
    print("V5 文件标题结构 (前50个):")
    print("=" * 80)
    for i, (line_num, level, content) in enumerate(v5_headers[:50], 1):
        indent = "  " * (level - 1)
        print(f"{i:2d}. L{line_num:5d}: {indent}{'#' * level} {content[:60]}")

    print("\n" + "=" * 80)
    print("标准文件标题结构 (前50个):")
    print("=" * 80)
    for i, (line_num, level, content) in enumerate(standard_headers[:50], 1):
        indent = "  " * (level - 1)
        print(f"{i:2d}. L{line_num:5d}: {indent}{'#' * level} {content[:60]}")

    print("\n" + "=" * 80)
    print(f"统计: V5有{len(v5_headers)}个标题, 标准有{len(standard_headers)}个标题")
    print("=" * 80)

if __name__ == '__main__':
    main()
