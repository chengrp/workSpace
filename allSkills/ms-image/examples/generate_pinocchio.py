# -*- coding: utf-8 -*-
"""
生成木偶奇遇记插图
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator

# 创建生成器
generator = ModelScopeImageGenerator()

# 生成木偶奇遇记插图
print("正在生成《木偶奇遇记》插图...")
print("尺寸: 16:9, 2K")
print()

result = generator.generate_image(
    prompt="Pinocchio the wooden puppet, classic Disney illustration style, warm golden lighting, fairy tale atmosphere, sitting at a workshop bench, highly detailed, 2K resolution, cinematic, 16:9 wide aspect ratio",
    output_path="pinocchio_illustration.jpg",
    verbose=True
)

print()
print("=" * 60)
if result["success"]:
    print("✅ 插图生成成功！")
    print(f"📁 保存位置: {result['output_path']}")
else:
    print(f"❌ 生成失败: {result.get('error', '未知错误')}")
