# -*- coding: utf-8 -*-
"""
重新生成木偶奇遇记插图 - 使用正确的尺寸参数
16:9, FHD (1920x1080, 2.1MP) - API支持的最大横屏分辨率
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("=" * 60)
print("重新生成《木偶奇遇记》插图")
print("规格: 16:9, FHD (1920x1080)")
print("=" * 60)

result = generator.generate_image(
    prompt="Pinocchio the wooden puppet, classic Disney illustration style, warm golden lighting, fairy tale atmosphere, sitting at a workshop bench, highly detailed, cinematic, 16:9 wide aspect ratio",
    size="1920x1080",  # 16:9 FHD - API支持的最大横屏分辨率
    output_path="pinocchio_illustration_16_9.jpg",
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
    print(f"📊 宽高比: {w/h:.2f}:1 (16:9 = 1.78:1)")
    print(f"🎨 分辨率: {megapixels:.2f}MP (FHD级别)")
    print(f"✨ 状态: {'✓ 完美匹配16:9' if abs(w/h - 16/9) < 0.01 else '比例偏差'}")
else:
    print(f"❌ 生成失败: {result.get('error', '未知错误')}")

print("=" * 60)
