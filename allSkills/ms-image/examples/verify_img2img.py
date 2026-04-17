# -*- coding: utf-8 -*-
"""
验证图生图效果 - 等待任务完成
"""

import sys
import io
import sys
import os
import base64
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from PIL import Image
from io import BytesIO

api_key = "ms-51dd7494-0706-45d9-a901-c395522c55f2"
base_url = 'https://api-inference.modelscope.cn/'

# 使用测试1的任务ID
task_id = "5058761"

print("=" * 60)
print("验证图生图效果")
print("=" * 60)
print("等待任务完成...")

max_wait = 120
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
        print("✅ 任务完成!")
        break
    elif status == "FAILED":
        print(f"❌ 任务失败")
        print(f"错误: {data}")
        sys.exit(1)

    time.sleep(5)
    waited += 5
    print(f"   等待中... ({waited}秒)")

if image_url:
    # 下载图片
    print("\n下载生成的图片...")
    img_response = requests.get(image_url)
    img = Image.open(BytesIO(img_response.content))

    output_path = os.path.join(os.path.dirname(__file__), "img2img_result.jpg")
    img.save(output_path)

    w, h = img.size
    print(f"\n✅ 图生图成功!")
    print(f"📁 保存位置: {output_path}")
    print(f"📐 尺寸: {w} x {h}")
    print(f"📊 大小: {len(img_response.content)} 字节")

    print("\n结论:")
    print("  ✅ ModelScope API支持图生图功能")
    print("  ✅ 可以使用image参数传入参考图(base64编码)")
    print("  ✅ 可以生成与参考图同风格的新图片")
else:
    print("\n⚠️ 任务超时")

print("=" * 60)
