# -*- coding: utf-8 -*-
"""
测试ModelScope图生图(Image-to-Image)功能
"""

import sys
import io
import sys
import os
import base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

api_key = "ms-51dd7494-0706-45d9-a901-c395522c55f2"
base_url = 'https://api-inference.modelscope.cn/'

# 读取一张参考图
reference_image = "tom_jerry_cartoon_9_16.jpg"

print("=" * 60)
print("测试ModelScope图生图功能")
print("=" * 60)

# 读取并编码图片
img_path = os.path.join(os.path.dirname(__file__), reference_image)
if not os.path.exists(img_path):
    print(f"❌ 参考图不存在: {reference_image}")
    sys.exit(1)

with open(img_path, 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

print(f"参考图: {reference_image}")
print(f"图片大小: {len(image_data)} 字符 (base64编码)")

# 测试不同的图生图参数
test_cases = [
    {
        "name": "测试1: 使用image参数",
        "payload": {
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A cat and mouse playing together",
            "image": image_data
        }
    },
    {
        "name": "测试2: 使用input_image参数",
        "payload": {
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A cat and mouse playing together",
            "input_image": image_data
        }
    },
    {
        "name": "测试3: 使用image_url参数（模拟）",
        "payload": {
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A cat and mouse playing together",
            "image_url": "https://example.com/ref.jpg"
        }
    }
]

for test in test_cases:
    print(f"\n{test['name']}")

    try:
        response = requests.post(
            f"{base_url}v1/images/generations",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "X-ModelScope-Async-Mode": "true"
            },
            data=json.dumps(test['payload'], ensure_ascii=False).encode('utf-8')
        )

        if response.status_code == 200:
            task_id = response.json().get("task_id")
            print(f"   ✅ 成功提交 - Task ID: {task_id}")
            print(f"   说明: API支持该参数")
        else:
            print(f"   ❌ HTTP {response.status_code}")
            print(f"   响应: {response.text[:200]}")

    except Exception as e:
        print(f"   ❌ 错误: {str(e)}")

print("\n" + "=" * 60)
print("结论:")
print("  如果测试成功，说明ModelScope支持图生图功能")
print("  如果失败，可能需要使用其他方式实现同风格生成")
print("=" * 60)
