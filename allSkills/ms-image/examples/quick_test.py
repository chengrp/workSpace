"""
快速测试脚本 - 生成一张示例图片
"""

import sys
import os
import io

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator


def main():
    """生成一张测试图片"""
    print("=" * 60)
    print("ms-image 技能快速测试")
    print("=" * 60)
    print()

    print("功能说明:")
    print("- 模型: Tongyi-MAI/Z-Image-Turbo")
    print("- 免费额度: 每天2000张")
    print("- API: ModelScope")
    print()

    # 创建生成器
    generator = ModelScopeImageGenerator()

    # 生成图片
    output_path = os.path.join(os.path.dirname(__file__), "demo_image.jpg")

    print("正在生成测试图片...")
    print("Prompt: A serene Japanese garden with cherry blossoms, peaceful, high quality")
    print()

    result = generator.generate_image(
        prompt="A serene Japanese garden with cherry blossoms, peaceful, high quality",
        output_path=output_path,
        verbose=True
    )

    print()
    print("=" * 60)

    if result["success"]:
        print("✅ 测试成功!")
        print(f"📁 图片已保存到: {output_path}")
        print()
        print("技能已就绪，可以在Claude Code中使用!")
        print()
        print("使用示例:")
        print('  对Claude说: "帮我生成一张图片，内容是..."')
        return 0
    else:
        print("❌ 测试失败")
        print(f"错误: {result.get('error', '未知错误')}")
        return 1


if __name__ == "__main__":
    exit(main())
