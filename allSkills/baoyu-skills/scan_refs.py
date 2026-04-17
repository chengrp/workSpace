#!/usr/bin/env python3
import json
import re
from pathlib import Path

TARGET_DIR = Path('skills/baoyu-article-illustrator')

PATTERNS = [
    (r'\[[^\]]+\]\(([^)]+\.md)\)', 'standard_link'),
    (r'!\[[^\]]*\]\(([^)]+\.md)\)', 'image_link'),
    (r'<(?:a|link|img)[^>]*(?:href|src)\s*=\s*["\']([^"\']+\.md)["\']', 'html_tag'),
]

def clean_path(raw):
    if not raw:
        return None
    cleaned = raw.split('#')[0].split('?')[0]
    cleaned = cleaned.replace('\\', '/').lstrip('./').lstrip('../')
    if not cleaned.endswith('.md'):
        return None
    return cleaned

def scan_file(file_path, all_files):
    content = file_path.read_text(encoding='utf-8')
    refs = set()

    for pattern, _ in PATTERNS:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            raw = match.group(1)
            cleaned = clean_path(raw)
            if cleaned:
                # 标准化为正斜杠用于比较
                normalized = cleaned.replace('\\', '/')
                for target in all_files:
                    target_rel = str(target.relative_to(TARGET_DIR)).replace('\\', '/')
                    target_name = target.name
                    # 支持多种匹配方式
                    if (cleaned == target_name or
                        normalized == target_rel or
                        target_rel.endswith(normalized) or
                        normalized in target_rel):
                        refs.add(str(target.relative_to(TARGET_DIR)))
                        break
    return refs

all_md_files = list(TARGET_DIR.rglob('*.md'))
print(f"Scanning {len(all_md_files)} files...", file=__import__('sys').stderr)

nodes = []
edges = []

for i, f in enumerate(all_md_files):
    rel_path = str(f.relative_to(TARGET_DIR))
    nodes.append({
        'id': f'f_{i}',
        'label': f.name,
        'type': 'file',
        'path': rel_path.replace('/', '\\')
    })

for i, f in enumerate(all_md_files):
    refs = scan_file(f, all_md_files)
    for ref in refs:
        target_idx = next((j for j, tf in enumerate(all_md_files)
                          if str(tf.relative_to(TARGET_DIR)) == ref), -1)
        if target_idx >= 0 and target_idx != i:
            edges.append({
                'from': f'f_{i}',
                'to': f'f_{target_idx}',
                'label': 'references',
                'type': 'EXTRACTED'
            })

graph = {
    'nodes': nodes,
    'edges': edges,
    'stats': {'nodes': len(nodes), 'edges': len(edges)}
}

print(json.dumps(graph, indent=2, ensure_ascii=False))
