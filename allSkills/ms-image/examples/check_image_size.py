# -*- coding: utf-8 -*-
"""
检查生成的图片尺寸
"""

import sys
import io
from PIL import Image
import os

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

examples_dir = os.path.dirname(__file__)

images = [
    "pinocchio_illustration.jpg",
    "tom_jerry_cartoon.jpg"
]

print("=" * 60)
print("检查生成图片的实际尺寸")
print("=" * 60)

for img_name in images:
    img_path = os.path.join(examples_dir, img_name)
    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            width, height = img.size
            ratio = width / height if height > 0 else 0

            print(f"\n📷 {img_name}")
            print(f"   尺寸: {width} x {height} 像素")
            print(f"   宽高比: {ratio:.2f}:1")

            # 判断实际比例
            if abs(ratio - 16/9) < 0.1:
                print(f"   实际比例: 16:9 ✓")
            elif abs(ratio - 9/16) < 0.1:
                print(f"   实际比例: 9:16 ✓")
            else:
                print(f"   实际比例: 自定义")

            # 判断分辨率等级
            total_pixels = width * height
            if total_pixels >= 3840 * 2160:  # 4K
                print(f"   分辨率: 4K")
            elif total_pixels >= 2560 * 1440:  # 2K
                print(f"   分辨率: 2K")
            elif total_pixels >= 1920 * 1080:  # FHD
                print(f"   分辨率: FHD")
            else:
                print(f"   分辨率: {total_pixels // 10000}万像素")
    else:
        print(f"\n❌ {img_name} - 文件不存在")

print("\n" + "=" * 60)
