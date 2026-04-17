# -*- coding: utf-8 -*-
"""
ms-image技能完整功能演示
展示文生图、图生图、自定义尺寸等功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("=" * 70)
print("ms-image 技能完整功能演示")
print("=" * 70)
print()

# 演示1: 基本文生图
print("【演示1】基本文生图")
print("-" * 70)
result = generator.generate_image(
    prompt="A serene mountain landscape at sunrise, digital art, highly detailed",
    size="1920x1080",
    output_path="demo_text2img.jpg",
    verbose=False
)
if result['success']:
    img = Image.open(result['output_path'])
    print(f"✅ 成功生成: {result['output_path']}")
    print(f"   尺寸: {img.size[0]} x {img.size[1]}")
print()

# 演示2: 图生图
print("【演示2】图生图 - 生成同风格图片")
print("-" * 70)
ref_img = "tom_jerry_cartoon_9_16.jpg"
ref_path = os.path.join(os.path.dirname(__file__), ref_img)

if os.path.exists(ref_path):
    result = generator.generate_image(
        prompt="A mouse riding a dog, same cartoon style",
        reference_image=ref_path,
        size="1080x1920",
        output_path="demo_img2img.jpg",
        verbose=False
    )
    if result['success']:
        img = Image.open(result['output_path'])
        print(f"✅ 成功生成: {result['output_path']}")
        print(f"   参考图: {ref_img}")
        print(f"   尺寸: {img.size[0]} x {img.size[1]}")
else:
    print(f"⚠️ 参考图不存在: {ref_img}")
print()

# 演示3: 不同比例
print("【演示3】多种比例生成")
print("-" * 70)

ratios = [
    ("16:9 横屏", "1792x1024", "demo_16_9.jpg"),
    ("9:16 竖屏", "1024x1792", "demo_9_16.jpg"),
    ("1:1 正方形", "1536x1536", "demo_1_1.jpg"),
]

for name, size, output in ratios:
    result = generator.generate_image(
        prompt=f"Beautiful abstract art {name}",
        size=size,
        output_path=output,
        verbose=False
    )
    if result['success']:
        img = Image.open(output)
        actual = f"{img.size[0]}x{img.size[1]}"
        match = "✓" if actual == size else "✗"
        print(f"   {name:<12} 期望:{size:<12} 实际:{actual:<12} {match}")

print()
print("=" * 70)
print("演示完成！生成的图片保存在examples目录")
print("=" * 70)
print()
print("功能总结:")
print("  ✅ 文生图 - 根据文字描述生成图片")
print("  ✅ 图生图 - 根据参考图生成同风格图片")
print("  ✅ 自定义尺寸 - 支持16:9、9:16、1:1等多种比例")
print("  ✅ 高质量输出 - FHD级别（约2MP）")
print("  ✅ 免费额度 - 每天2000张")
