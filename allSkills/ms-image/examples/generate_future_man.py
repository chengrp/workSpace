# -*- coding: utf-8 -*-
"""
根据参考图生成未来男士照片
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("=" * 70)
print("根据参考图生成未来男士照片")
print("=" * 70)

# 参考图路径
reference_image = r"C:\Users\RyanCh\Desktop\Pic_huxiu\1572148055691.jpg"

# 检查参考图是否存在
if os.path.exists(reference_image):
    print(f"✓ 参考图: {reference_image}")

    # 获取参考图信息
    with Image.open(reference_image) as img:
        w, h = img.size
        print(f"  参考图尺寸: {w} x {h}")
        print(f"  参考图格式: {img.format}")
else:
    print(f"✗ 参考图不存在: {reference_image}")
    print("将使用文生图模式...")

print()
print("生成参数:")
print("  风格: 未来科技感")
print("  比例: 16:9")
print("  分辨率: 1920x1080 (FHD - API最高支持)")
print("  说明: 严格2K(2560x1440)超出API限制，使用FHD代替")
print()

# 生成图片
result = generator.generate_image(
    prompt="Futuristic man portrait, advanced technology style, holographic elements, cyberpunk aesthetic, highly detailed face, professional photography, cinematic lighting",
    size="1920x1080",  # 16:9 FHD - API支持的最高分辨率
    reference_image=reference_image if os.path.exists(reference_image) else None,
    output_path="future_man_16_9.jpg",
    verbose=True
)

print("\n" + "=" * 70)
if result["success"]:
    # 验证生成结果
    output = result["output_path"]
    with Image.open(output) as img:
        w, h = img.size
        pixels = w * h
        megapixels = pixels / 1000000

        print("✓ 照片生成成功！")
        print(f"  保存位置: {output}")
        print(f"  实际尺寸: {w} x {h}")
        print(f"  宽高比: {w/h:.2f}:1 (16:9 = 1.78:1)")
        print(f"  分辨率: {megapixels:.2f}MP (FHD级别)")
        print(f"  比例匹配: {'✓ 完美' if abs(w/h - 16/9) < 0.01 else '✗ 偏差'}")

        if os.path.exists(reference_image):
            print(f"  说明: 已根据参考图风格生成")
else:
    print(f"✗ 生成失败: {result.get('error', '未知错误')}")

print("=" * 70)
