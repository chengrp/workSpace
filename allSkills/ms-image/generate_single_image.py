#!/usr/bin/env python3
"""
单独生成第三张图片：术与道
"""

import sys
import os
sys.path.append('scripts')

from ms_image_generator import ModelScopeImageGenerator

def generate_single_image():
    """生成第三张图片"""

    # 创建生成器实例
    generator = ModelScopeImageGenerator()

    # 创建输出目录
    os.makedirs("article_images", exist_ok=True)

    # 生成第三张图片
    img_config = {
        "name": "术与道",
        "prompt": "Cream paper texture, colored pencil drawing style, top-down comparison layout, top section: SHU (tools and skills) with gear and lightning icons, labeled quick response, efficiency improvement, short-term gains; bottom section: DAO (essential insight) with brain and eye icons, labeled industry understanding, user insight, deep thinking, gradient transition in middle, 16:9 aspect ratio",
        "size": "1920x1080",
        "output": "article_images/shu_dao.jpg"
    }

    print(f"正在生成：{img_config['name']}")
    print(f"Prompt: {img_config['prompt']}")

    # 生成图片
    result = generator.generate_image(
        prompt=img_config['prompt'],
        size=img_config['size'],
        output_path=img_config['output'],
        verbose=True
    )

    if result['success']:
        print(f"✅ {img_config['name']} 生成成功！")
        print(f"   保存路径：{img_config['output']}")
    else:
        print(f"❌ {img_config['name']} 生成失败：{result['error']}")

if __name__ == "__main__":
    generate_single_image()