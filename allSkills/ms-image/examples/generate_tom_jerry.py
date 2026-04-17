# -*- coding: utf-8 -*-
"""
生成猫和老鼠动画片插图
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator

# 创建生成器
generator = ModelScopeImageGenerator()

# 生成猫和老鼠插图
print("正在生成《猫和老鼠》动画片插图...")
print("尺寸: 9:16, 2K")
print()

result = generator.generate_image(
    prompt="Tom and Jerry classic cartoon scene, Tom the cat chasing Jerry the mouse, vintage Hanna-Barbera animation style, colorful and vibrant, dynamic action pose, comic book style, highly detailed, 2K resolution, 9:16 portrait aspect ratio, nostalgic cartoon aesthetic",
    output_path="tom_jerry_cartoon.jpg",
    verbose=True
)

print()
print("=" * 60)
if result["success"]:
    print("✅ 插图生成成功！")
    print(f"📁 保存位置: {result['output_path']}")
else:
    print(f"❌ 生成失败: {result.get('error', '未知错误')}")
