# -*- coding: utf-8 -*-
import sys
import os

# 直接在ms_image_generator内部处理编码，所以这里不需要额外设置
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image

generator = ModelScopeImageGenerator()

print("Testing different image ratios with size parameter")
print("=" * 60)

tests = [
    ("9:16 Portrait", "1024x1792", "test_portrait.jpg"),
    ("16:9 Landscape", "1792x1024", "test_landscape.jpg"),
    ("1:1 Square", "1536x1536", "test_square.jpg"),
]

for name, size, output in tests:
    print(f"\nTesting: {name} ({size})")
    result = generator.generate_image(
        prompt=f"Test image {name}",
        size=size,
        output_path=output,
        verbose=False
    )

    if result['success']:
        img = Image.open(output)
        w, h = img.size
        actual = f"{w}x{h}"
        match = "✓" if actual == size else "✗"
        print(f"  Expected: {size}, Actual: {actual} {match}")
    else:
        print(f"  Failed: {result.get('error')}")

print("\n" + "=" * 60)
print("Test complete!")
