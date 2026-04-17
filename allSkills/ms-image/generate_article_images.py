#!/usr/bin/env python3
"""
为《AI狂飙之后，我们留下了什么》文章生成配图
"""

import sys
import os
sys.path.append('scripts')

from ms_image_generator import ModelScopeImageGenerator
import time

def generate_article_images():
    """生成文章配图"""

    # 创建生成器实例
    generator = ModelScopeImageGenerator()

    # 创建输出目录
    os.makedirs("article_images", exist_ok=True)

    # 定义图片配置
    images = [
        {
            "name": "封面图",
            "prompt": "Cream paper texture, colored pencil drawing style, a sports car racing on highway, fork road ahead, one road leads to starry sky (prosperity), one road leads to mist (unknown), background with blurred code flow and data symbols, 16:9 aspect ratio, title AI狂飙之后，我们留下了什么, subtitle when everyone is accelerating, who is thinking about the direction?",
            "size": "1920x1080",
            "output": "article_images/cover.jpg"
        },
        {
            "name": "价值判断三问",
            "prompt": "Cream paper texture, colored pencil drawing style, three question marks floating in center of image, each with text below: Will anyone still use this in three months? Is it close to money? Would I do this if AI didn't exist? background with light thought bubbles and light bulb icons, 16:9 aspect ratio",
            "size": "1920x1080",
            "output": "article_images/value_questions.jpg"
        },
        {
            "name": "术与道",
            "prompt": "Cream paper texture, colored pencil drawing style, top-down comparison layout, top section: SHU (tools and skills) with gear and lightning icons, labeled quick response, efficiency improvement, short-term gains; bottom section: DAO (essential insight) with brain and eye icons, labeled industry understanding, user insight, deep thinking, gradient transition in middle, 16:9 aspect ratio",
            "size": "1920x1080",
            "output": "article_images/shu_dao.jpg"
        }
    ]

    # 生成图片
    for img_config in images:
        print(f"\n{'='*60}")
        print(f"正在生成：{img_config['name']}")
        print(f"{'='*60}")

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

        # 等待一下，避免请求过快
        time.sleep(3)

    print(f"\n{'='*60}")
    print("所有图片生成完成！")
    print(f"{'='*60}")

if __name__ == "__main__":
    generate_article_images()