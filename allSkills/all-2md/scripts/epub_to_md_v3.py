#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EPUB to Markdown 转换器 V3
修复：
1. 直接使用 HTML 标题标签，不使用正则匹配
2. 修复副标题问题（以——开头的 h2 改为粗体文本）
3. 正确处理篇、章、节的层级关系
"""
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import re
from pathlib import Path
import sys

def is_subtitle(text):
    """判断是否是副标题（以——开头）"""
    return text.strip().startswith('——') or text.strip().startswith('---')

def html_to_markdown_v3(soup):
    """V3: 直接使用 HTML 标题标签，修复副标题"""
    md_lines = []
    title_stack = []  # 跟踪标题层级

    for element in soup.find_all(True):
        tag = element.name

        if tag in ('script', 'style', 'meta', 'link'):
            continue

        # 处理标题标签
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            level = int(tag[1])
            prefix = '#' * level
            text = element.get_text(strip=True)

            if not text:
                continue

            # 检查是否是副标题
            if is_subtitle(text):
                # 副标题改为粗体，不作为标题
                md_lines.append(f"\\n{text}\\n")
            else:
                # 正常标题
                md_lines.append(f"\\n{prefix} {text}\\n")
                title_stack.append((level, text))

        # 段落处理
        elif tag == 'p':
            text = element.get_text(strip=True)
            if text:
                md_lines.append(f"\\n{text}\\n")

        # 强调
        elif tag in ('b', 'strong'):
            text = element.get_text(strip=True)
            if text and md_lines:
                # 在最后一行中查找并替换
                md_lines[-1] = md_lines[-1].replace(text, f"**{text}**")

        # 列表
        elif tag == 'li':
            text = element.get_text(strip=True)
            if text:
                md_lines.append(f"- {text}")

    # 合并内容
    content = '\\n'.join(md_lines)

    # 清理多余空行
    content = re.sub(r'\\n{3,}', '\\n\\n', content)

    return content

def cleanup_final_markdown(content):
    """最终清理：移除多余粗体标记，修复格式"""
    lines = content.split('\\n')
    result = []

    for line in lines:
        line = line.strip()
        if not line:
            result.append('')
            continue

        # 移除标题中的粗体标记（如 "## 第一**章**" -> "## 第一章"）
        if re.match(r'^#+', line):
            # 移除标题中的所有 ** 对
            while '**' in line:
                line = line.replace('**', '')
            result.append(line)
        else:
            # 保留正文中的粗体，但移除单字符粗体
            # 检查是否是单字符被粗体标记
            if re.match(r'^\\*\\*([^*\\n])\\*\\*$', line):
                result.append(re.sub(r'^\\*\\*([^*\\n])\\*\\*$', r'\\1', line))
            else:
                result.append(line)

    return '\\n'.join(result)

def epub_to_markdown_v3(epub_path, md_path):
    """V3: EPUB 转 Markdown - 修复副标题和层级"""
    print(f"[INFO] Processing: {epub_path}")

    try:
        book = epub.read_epub(epub_path)

        # 获取元数据
        title = "Unknown Title"
        author = "Unknown Author"
        try:
            if book.get_metadata('DC', 'title'):
                title = book.get_metadata('DC', 'title')[0][0]
            if book.get_metadata('DC', 'creator'):
                author = book.get_metadata('DC', 'creator')[0][0]
        except:
            pass

        print(f"   Title: {title}")
        print(f"   Author: {author}")

        # 收集内容
        md_content = []

        # 添加文档头部
        md_content.append(f"# {title}")
        md_content.append(f"**Author**: {author}")
        md_content.append("---")

        # 获取所有文档
        doc_items = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                doc_items.append(item)

        print(f"   Found {len(doc_items)} document files")

        # 按顺序处理
        for i, item in enumerate(doc_items):
            soup = BeautifulSoup(item.get_content(), 'html.parser')

            # 移除不需要的元素
            for unwanted in soup(['script', 'style', 'meta', 'link']):
                unwanted.decompose()

            # 转换为 Markdown
            chapter_md = html_to_markdown_v3(soup)

            if chapter_md.strip():
                md_content.append(chapter_md)

            if (i + 1) % 10 == 0:
                print(f"   Progress: {i + 1}/{len(doc_items)}")

        # 合并
        full_md = '\\n'.join(md_content)

        # 最终清理
        full_md = cleanup_final_markdown(full_md)

        # 写入文件
        Path(md_path).write_text(full_md, encoding='utf-8')

        print(f"[OK] Conversion complete: {md_path}")
        print(f"[STAT] Character count: {len(full_md):,}")

        return True

    except Exception as e:
        print(f"[ERROR] Conversion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python epub_to_md_v3.py <epub_file> [output.md]")
        sys.exit(1)

    epub_path = sys.argv[1]

    if len(sys.argv) >= 3:
        md_path = sys.argv[2]
    else:
        epub_path_obj = Path(epub_path)
        md_path = epub_path_obj.parent / (epub_path_obj.stem + ".md")

    success = epub_to_markdown_v3(epub_path, md_path)
    sys.exit(0 if success else 1)
