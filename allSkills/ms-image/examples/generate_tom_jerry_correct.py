# -*- coding: utf-8 -*-
"""
重新生成猫和老鼠动画片插图 - 使用正确的尺寸参数
9:16, FHD (1080x1920, 2.1MP) - API支持的最大竖屏分辨率
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("=" * 60)
print("重新生成《猫和老鼠》动画片插图")
print("规格: 9:16, FHD (1080x1920)")
print("=" * 60)

result = generator.generate_image(
    prompt="Tom and Jerry classic cartoon scene, Tom the cat chasing Jerry the mouse, vintage Hanna-Barbera animation style, colorful and vibrant, dynamic action pose, comic book style, highly detailed, cinematic, 9:16 portrait aspect ratio, nostalgic cartoon aesthetic",
    size="1080x1920",  # 9:16 FHD - API支持的最大竖屏分辨率
    output_path="tom_jerry_cartoon_9_16.jpg",
    verbose=True
)

print("\n" + "=" * 60)
if result["success"]:
    # 验证实际尺寸
    img = Image.open(result["output_path"])
    w, h = img.size
    pixels = w * h
    megapixels = pixels / 1000000

    print("✅ 插图生成成功！")
    print(f"📁 保存位置: {result['output_path']}")
    print(f"📐 实际尺寸: {w} x {h}")
    print(f"📊 宽高比: {w/h:.2f}:1 (9:16 = 0.56:1)")
    print(f"🎨 分辨率: {megapixels:.2f}MP (FHD级别)")
    print(f"✨ 状态: {'✓ 完美匹配9:16' if abs(w/h - 9/16) < 0.01 else '比例偏差'}")
else:
    print(f"❌ 生成失败: {result.get('error', '未知错误')}")

print("=" * 60)
