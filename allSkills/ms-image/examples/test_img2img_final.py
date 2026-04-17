# -*- coding: utf-8 -*-
"""
测试图生图功能 - 使用代码更新后的版本
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("=" * 60)
print("测试图生图功能 - 生成同风格图片")
print("=" * 60)

# 使用猫和老鼠的图片作为参考
reference_image = "tom_jerry_cartoon_9_16.jpg"
ref_path = os.path.join(os.path.dirname(__file__), reference_image)

if not os.path.exists(ref_path):
    print(f"❌ 参考图不存在: {reference_image}")
    sys.exit(1)

# 获取参考图信息
with Image.open(ref_path) as img:
    w, h = img.size

print(f"参考图: {reference_image}")
print(f"参考图尺寸: {w} x {h}")
print(f"参考图风格: Hanna-Barbera卡通风格")
print()

# 生成同风格的新图片
result = generator.generate_image(
    prompt="A dog chasing a cat, same cartoon style as reference",
    reference_image=ref_path,
    size="1080x1920",  # 保持相同比例
    output_path="img2img_dog_chasing_cat.jpg",
    verbose=True
)

print("\n" + "=" * 60)
if result["success"]:
    # 验证生成结果
    output = result["output_path"]
    with Image.open(output) as img:
        w, h = img.size
        print("✅ 图生图成功！")
        print(f"📁 保存位置: {output}")
        print(f"📐 尺寸: {w} x {h}")
        print(f"🎨 说明: 新图片应该保持了参考图的卡通风格")
else:
    print(f"❌ 生成失败: {result.get('error', '未知错误')}")

print("=" * 60)
