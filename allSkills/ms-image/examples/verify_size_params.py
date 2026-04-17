# -*- coding: utf-8 -*-
"""
验证尺寸参数是否生效 - 等待任务完成并检查图片
"""

import sys
import io
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import time
import json
from PIL import Image
from io import BytesIO

api_key = "ms-51dd7494-0706-45d9-a901-c395522c55f2"
base_url = 'https://api-inference.modelscope.cn/'

# 已提交的任务ID
test_tasks = [
    ("5058257", "size参数", "1024x1792"),
    ("5058258", "width/height参数", "1080x1920"),
    ("5058259", "resolution参数", "未知")
]

print("=" * 60)
print("等待任务完成并验证尺寸参数")
print("=" * 60)

results = []

for task_id, param_name, expected_size in test_tasks:
    print(f"\n检查任务 {task_id} ({param_name})...")

    # 轮询任务状态
    max_wait = 120  # 最多等待120秒
    waited = 0
    image_url = None

    while waited < max_wait:
        response = requests.get(
            f"{base_url}v1/tasks/{task_id}",
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-ModelScope-Task-Type": "image_generation"
            }
        )

        data = response.json()
        status = data.get("task_status")

        if status == "SUCCEED":
            image_url = data["output_images"][0]
            break
        elif status == "FAILED":
            print(f"   ❌ 任务失败")
            break

        time.sleep(5)
        waited += 5

    if image_url:
        # 下载图片并检查尺寸
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        width, height = img.size

        print(f"   ✅ 实际尺寸: {width} x {height}")
        print(f"   期望尺寸: {expected_size}")

        results.append({
            "param": param_name,
            "actual": f"{width}x{height}",
            "expected": expected_size,
            "match": str(width) + "x" + str(height) == expected_size
        })
    else:
        print(f"   ⏰ 任务超时或失败")

# 总结
print("\n" + "=" * 60)
print("测试结果总结")
print("=" * 60)

for r in results:
    status = "✅ 匹配" if r["match"] else "❌ 不匹配"
    print(f"{r['param']}: {r['actual']} (期望: {r['expected']}) - {status}")

# 找出有效的参数
print("\n" + "=" * 60)
print("结论:")
print("=" * 60)

valid_params = [r["param"] for r in results if r["match"]]
if valid_params:
    print(f"✅ 有效参数: {', '.join(valid_params)}")
else:
    print("⚠️ 所有参数都被API忽略，使用默认尺寸")

    # 分析默认尺寸
    if results:
        actual = results[0]["actual"]
        print(f"\n📊 API默认尺寸: {actual}")
        w, h = map(int, actual.split('x'))
        ratio = w / h
        print(f"   默认宽高比: {ratio:.2f}:1")
        print(f"   默认分辨率: {w * h / 10000:.1f}万像素")
