#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化的 EPUB to Markdown 转换器 V2
修复中文章节标题识别问题
"""
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from pathlib import Path
import sys

def html_to_markdown_v2(soup):
    """V2: 正确识别中文章节结构"""
    md_lines = []

    # 获取所有文本内容，保留段落结构
    for element in soup.find_all(True):
        tag = element.name

        if tag in ('script', 'style', 'meta', 'link'):
            continue

        # 获取纯文本
        if element.name in ['p', 'div', 'span']:
            text = element.get_text(strip=True)
            if text:
                md_lines.append(f"\n{text}\n")

        # 处理标题标签
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            prefix = '#' * level
            text = element.get_text(strip=True)
            if text:
                md_lines.append(f"\n{prefix} {text}\n")

    # 合并所有内容
    content = '\n'.join(md_lines)

    # 后处理：修复中文章节结构
    lines = content.split('\n')
    result = []

    for line in lines:
        line = line.strip()
        if not line:
            result.append('')
            continue

        # 识别篇标题（如"第一篇"、"第二篇"）
        if re.match(r'^第[一二三四五六七八九十百千]+篇', line):
            result.append(f"# {line}")

        # 识别章标题（如"第一章"、"第二章"）
        elif re.match(r'^第[一二三四五六七八九十百千]+章', line):
            result.append(f"## {line}")

        # 识别节标题（如"一、"、"二、"）
        elif re.match(r'^[一二三四五六七八九十]+、', line):
            result.append(f"### {line}")

        # 识别副标题（以"—"开头）
        elif line.startswith('——') or line.startswith('——'):
            result.append(f"**{line}**")

        # 其他内容保持原样
        else:
            result.append(line)

    return '\n'.join(result)

def epub_to_markdown_v2(epub_path, md_path):
    """V2: EPUB 转 Markdown - 修复章节结构"""
    print(f"[INFO] 正在处理: {epub_path}")

    try:
        book = epub.read_epub(epub_path)

        # 获取元数据
        title = "未知书名"
        author = "未知作者"
        try:
            if book.get_metadata('DC', 'title'):
                title = book.get_metadata('DC', 'title')[0][0]
            if book.get_metadata('DC', 'creator'):
                author = book.get_metadata('DC', 'creator')[0][0]
        except:
            pass

        print(f"   书名: {title}")
        print(f"   作者: {author}")

        # 收集内容
        md_content = []

        # 添加文档头部
        md_content.append(f"# {title}")
        md_content.append(f"**作者**：{author}")
        md_content.append("---")

        # 获取所有章节
        spine_items = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                spine_items.append(item)

        print(f"   发现 {len(spine_items)} 个章节文件")

        # 按顺序处理
        for i, item in enumerate(spine_items):
            soup = BeautifulSoup(item.get_content(), 'html.parser')

            # 移除不需要的元素
            for unwanted in soup(['script', 'style', 'meta', 'link']):
                unwanted.decompose()

            # 转换为 Markdown
            chapter_md = html_to_markdown_v2(soup)

            if chapter_md.strip():
                md_content.append(chapter_md)

            if (i + 1) % 10 == 0:
                print(f"   进度: {i + 1}/{len(spine_items)}")

        # 合并并清理
        full_md = '\n'.join(md_content)

        # 最终清理：移除多余空行
        full_md = re.sub(r'\n{3,}', '\n\n', full_md)

        # 写入文件
        Path(md_path).write_text(full_md, encoding='utf-8')

        print(f"[OK] 转换完成: {md_path}")
        print(f"[STAT] 字符数: {len(full_md):,}")

        return True

    except Exception as e:
        print(f"[ERROR] 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python epub_to_md_v2.py <epub文件> [输出文件.md]")
        sys.exit(1)

    epub_path = sys.argv[1]

    if len(sys.argv) >= 3:
        md_path = sys.argv[2]
    else:
        epub_path_obj = Path(epub_path)
        md_path = epub_path_obj.parent / (epub_path_obj.stem + ".md")

    success = epub_to_markdown_v2(epub_path, md_path)
    sys.exit(0 if success else 1)
