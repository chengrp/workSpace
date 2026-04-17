# -*- coding: utf-8 -*-
"""
测试多种比例的图片生成
验证size参数是否真的生效
"""

import sys
import io
import os

# 设置stdout为utf-8编码（需要先保存原始stdout）
original_stdout = sys.stdout
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator
from PIL import Image
import time

print("=" * 70)
print("测试多种比例的图片生成 - 验证size参数")
print("=" * 70)

# 定义测试用例：多种常见比例
test_cases = [
    {
        "name": "9:16 竖屏 (2K)",
        "size": "1024x1792",
        "output": "test_9_16_2k.jpg",
        "description": "手机壁纸、短视频封面"
    },
    {
        "name": "16:9 横屏 (2K)",
        "size": "1792x1024",
        "output": "test_16_9_2k.jpg",
        "description": "桌面壁纸、视频封面"
    },
    {
        "name": "1:1 正方形",
        "size": "1536x1536",
        "output": "test_1_1_square.jpg",
        "description": "社交媒体贴图"
    },
    {
        "name": "4:3 横屏",
        "size": "1536x1152",
        "output": "test_4_3.jpg",
        "description": "传统照片比例"
    },
    {
        "name": "3:4 竖屏",
        "size": "1152x1536",
        "output": "test_3_4.jpg",
        "description": "传统照片竖版"
    }
]

generator = ModelScopeImageGenerator()

results = []

for i, test in enumerate(test_cases, 1):
    print(f"\n{'=' * 70}")
    print(f"测试 {i}/{len(test_cases)}: {test['name']}")
    print(f"{'=' * 70}")
    print(f"说明: {test['description']}")
    print(f"期望尺寸: {test['size']}")

    output_path = os.path.join(os.path.dirname(__file__), test['output'])

    # 生成图片
    result = generator.generate_image(
        prompt=f"A beautiful landscape with mountains and lake, test {i}, {test['name']}",
        size=test['size'],
        output_path=output_path,
        verbose=False  # 减少输出
    )

    if result['success']:
        # 检查实际尺寸
        with Image.open(output_path) as img:
            width, height = img.size
            actual_size = f"{width}x{height}"
            match = actual_size == test['size']

            # 计算实际宽高比
            ratio = width / height
            # 计算期望宽高比
            exp_w, exp_h = map(int, test['size'].split('x'))
            exp_ratio = exp_w / exp_h

            # 判断比例是否正确
            ratio_match = abs(ratio - exp_ratio) < 0.01

            status = "✅ 完全匹配" if match else ("⚠️ 比例正确但尺寸不符" if ratio_match else "❌ 不匹配")

            print(f"实际尺寸: {actual_size}")
            print(f"状态: {status}")

            if not match:
                if ratio_match:
                    print(f"   → 比例正确 ({ratio:.2f}:1) 但像素值不同")
                else:
                    print(f"   → 期望比例 {exp_ratio:.2f}:1，实际 {ratio:.2f}:1")

            results.append({
                "name": test['name'],
                "expected": test['size'],
                "actual": actual_size,
                "match": match,
                "ratio_match": ratio_match
            })
    else:
        print(f"❌ 生成失败: {result.get('error')}")
        results.append({
            "name": test['name'],
            "expected": test['size'],
            "actual": "FAILED",
            "match": False,
            "ratio_match": False
        })

    # 等待一下，避免请求过快
    if i < len(test_cases):
        time.sleep(2)

# 总结
print(f"\n{'=' * 70}")
print("测试结果总结")
print(f"{'=' * 70}")

print(f"\n{'测试名称':<20} {'期望尺寸':<12} {'实际尺寸':<12} {'状态'}")
print("-" * 70)

perfect_match = 0
ratio_ok = 0
total = len(results)

for r in results:
    if r['actual'] == "FAILED":
        status = "❌ 失败"
    elif r['match']:
        status = "✅ 完美"
        perfect_match += 1
        ratio_ok += 1
    elif r['ratio_match']:
        status = "⚠️ 比例OK"
        ratio_ok += 1
    else:
        status = "❌ 错误"

    print(f"{r['name']:<20} {r['expected']:<12} {r['actual']:<12} {status}")

print(f"\n{'=' * 70}")
print(f"统计:")
print(f"  完全匹配: {perfect_match}/{total} ({perfect_match*100//total}%)")
print(f"  比例正确: {ratio_ok}/{total} ({ratio_ok*100//total}%)")

if perfect_match == total:
    print(f"\n✅✅✅ 完美！所有尺寸参数都生效了！")
elif ratio_ok == total:
    print(f"\n✅ 比例控制有效，但具体像素值可能有调整")
else:
    print(f"\n⚠️ 部分参数未生效，需要进一步调试")

print(f"{'=' * 70}")
