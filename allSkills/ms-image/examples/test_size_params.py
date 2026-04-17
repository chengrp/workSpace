# -*- coding: utf-8 -*-
"""
测试ModelScope API是否支持尺寸参数
"""

import sys
import io
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json

api_key = "ms-51dd7494-0706-45d9-a901-c395522c55f2"
base_url = 'https://api-inference.modelscope.cn/'

# 测试不同的尺寸参数
test_cases = [
    {
        "name": "测试1: 添加size参数 (1024x1792 9:16)",
        "payload": {
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A cute cat",
            "size": "1024x1792"
        }
    },
    {
        "name": "测试2: 添加width和height参数",
        "payload": {
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A cute cat",
            "width": 1080,
            "height": 1920
        }
    },
    {
        "name": "测试3: 添加resolution参数",
        "payload": {
            "model": "Tongyi-MAI/Z-Image-Turbo",
            "prompt": "A cute cat",
            "resolution": "2K"
        }
    }
]

print("=" * 60)
print("测试ModelScope API尺寸参数支持")
print("=" * 60)

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
        else:
            print(f"   ❌ 失败 - HTTP {response.status_code}")
            print(f"   响应: {response.text[:200]}")

    except Exception as e:
        print(f"   ❌ 错误: {str(e)}")

print("\n" + "=" * 60)
print("说明: 如果测试成功，说明API支持对应参数")
print("=" * 60)
