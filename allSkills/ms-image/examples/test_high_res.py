# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("Testing higher resolutions (close to 2K)")
print("=" * 60)

# 测试更高分辨率
tests = [
    ("9:16 ~2K Portrait", "1440x2560", "test_2k_portrait.jpg"),
    ("16:9 ~2K Landscape", "2560x1440", "test_2k_landscape.jpg"),
    ("9:16 HD Portrait", "1080x1920", "test_hd_portrait.jpg"),
    ("16:9 HD Landscape", "1920x1080", "test_hd_landscape.jpg"),
]

for name, size, output in tests:
    print(f"\nTesting: {name} ({size})")
    result = generator.generate_image(
        prompt=f"Beautiful landscape {name}",
        size=size,
        output_path=output,
        verbose=False
    )

    if result['success']:
        img = Image.open(output)
        w, h = img.size
        pixels = w * h
        megapixels = pixels / 1000000

        # 判断分辨率等级
        if pixels >= 2560 * 1440:
            res_level = "2K+"
        elif pixels >= 1920 * 1080:
            res_level = "FHD"
        else:
            res_level = "HD"

        actual = f"{w}x{h}"
        match = "✓" if actual == size else "✗"
        print(f"  Expected: {size}, Actual: {actual} {match}")
        print(f"  Resolution: {megapixels:.1f}MP ({res_level})")
    else:
        print(f"  Failed: {result.get('error')}")

print("\n" + "=" * 60)
print("High-resolution test complete!")
