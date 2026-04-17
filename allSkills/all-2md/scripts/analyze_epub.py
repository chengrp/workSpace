#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析 EPUB 文件的 HTML 结构
"""
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import sys
from pathlib import Path

def analyze_epub_structure(epub_path):
    """分析 EPUB 的 HTML 结构"""
    print(f"[INFO] 分析: {epub_path}")

    book = epub.read_epub(epub_path)
    doc_items = [item for item in book.get_items() if item.get_type() == ebooklib.ITEM_DOCUMENT]

    print(f"[INFO] 共 {len(doc_items)} 个文档文件")

    # 分析每个文件的结构
    for i, item in enumerate(doc_items):
        content = item.get_content()
        soup = BeautifulSoup(content, 'html.parser')

        # 获取文件名
        filename = item.get_name()

        # 获取所有标题标签
        titles = []
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'title']):
            text = tag.get_text(strip=True)
            if text:
                titles.append(f"{tag.name}: {text}")

        # 获取前几个段落的文本
        paragraphs = []
        for p in soup.find_all('p')[:5]:
            text = p.get_text(strip=True)
            if text and len(text) > 3:
                paragraphs.append(text[:100])

        # 只输出有内容的文件
        if titles or paragraphs:
            print(f"\n{'='*60}")
            print(f"文件 {i+1}: {filename}")
            print(f"{'='*60}")

            if titles:
                print("[标题标签]")
                for t in titles:
                    print(f"  {t}")

            if paragraphs:
                print("\n[段落示例]")
                for j, p in enumerate(paragraphs[:5]):
                    print(f"  {j+1}: {p}")

if __name__ == '__main__':
    epub_path = r"C:\Users\RyanCh\Desktop\books\以日为鉴[lunarora.com].epub"
    analyze_epub_structure(epub_path)
