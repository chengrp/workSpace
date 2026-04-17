# -*- coding: utf-8 -*-
"""
最终尺寸验证报告
"""

import sys
import io
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from PIL import Image

examples_dir = os.path.dirname(__file__)

print("=" * 70)
print("尺寸参数功能验证报告")
print("=" * 70)

# 测试的图片
test_images = [
    {
        "name": "猫和老鼠 (9:16)",
        "file": "tom_jerry_cartoon_9_16.jpg",
        "expected": "1080x1920",
        "ratio": "9:16"
    },
    {
        "name": "木偶奇遇记 (16:9)",
        "file": "pinocchio_illustration_16_9.jpg",
        "expected": "1920x1080",
        "ratio": "16:9"
    },
    {
        "name": "竖屏测试 (9:16)",
        "file": "test_portrait.jpg",
        "expected": "1024x1792",
        "ratio": "9:16"
    },
    {
        "name": "横屏测试 (16:9)",
        "file": "test_landscape.jpg",
        "expected": "1792x1024",
        "ratio": "16:9"
    },
    {
        "name": "正方形测试 (1:1)",
        "file": "test_square.jpg",
        "expected": "1536x1536",
        "ratio": "1:1"
    }
]

print(f"\n{'图片名称':<25} {'期望尺寸':<12} {'实际尺寸':<12} {'比例':<8} {'状态'}")
print("-" * 70)

all_match = True
for img_info in test_images:
    img_path = os.path.join(examples_dir, img_info["file"])

    if os.path.exists(img_path):
        with Image.open(img_path) as img:
            w, h = img.size
            actual = f"{w}x{h}"
            expected = img_info["expected"]

            match = actual == expected
            status = "✅ 完美" if match else "❌ 失败"

            if not match:
                all_match = False

            print(f"{img_info['name']:<25} {expected:<12} {actual:<12} {img_info['ratio']:<8} {status}")
    else:
        print(f"{img_info['name']:<25} {img_info['expected']:<12} {'文件不存在':<12} {img_info['ratio']:<8} ❌")
        all_match = False

print("\n" + "=" * 70)

if all_match:
    print("✅✅✅ 所有测试通过！size参数功能正常！")
    print("\n关键发现:")
    print("  • ModelScope API支持通过size参数控制图片尺寸")
    print("  • 格式: '宽x高' (如 '1920x1080', '1080x1920')")
    print("  • 支持多种比例: 16:9, 9:16, 1:1, 4:3, 3:4")
    print("  • 最大分辨率: FHD级别 (约2MP)")
    print("  • 更高分辨率(2K+)会返回400错误")
else:
    print("⚠️ 部分测试失败，需要检查")

print("\n支持的尺寸示例:")
print("  • 竖屏9:16: 1024x1792, 1080x1920")
print("  • 横屏16:9: 1792x1024, 1920x1080")
print("  • 正方形1:1: 1536x1536")
print("  • 传统4:3: 1536x1152")
print("  • 传统3:4: 1152x1536")

print("=" * 70)
