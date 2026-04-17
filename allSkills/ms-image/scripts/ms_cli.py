"""
简单的命令行工具 - 快速生成图片
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from ms_image_generator import ModelScopeImageGenerator


def quick_generate(prompt: str, output_path: str = None):
    """
    快速生成图片

    Args:
        prompt: 图片描述
        output_path: 输出路径（可选）
    """
    generator = ModelScopeImageGenerator()

    if output_path is None:
        output_path = "result_image.jpg"

    result = generator.generate_image(
        prompt=prompt,
        output_path=output_path
    )

    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python ms_cli.py '<prompt>' [output_path]")
        print("示例: python ms_cli.py 'A golden cat' my_cat.jpg")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None

    quick_generate(prompt, output)
