"""
ModelScope图片生成器测试脚本
"""

import sys
import os
import io

# 设置stdout为utf-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_generator import ModelScopeImageGenerator


def test_basic_generation():
    """测试基本图片生成"""
    print("=" * 50)
    print("测试1: 基本图片生成")
    print("=" * 50)

    generator = ModelScopeImageGenerator()

    # 输出到examples目录
    output_path = os.path.join(os.path.dirname(__file__), "test_cat.jpg")

    result = generator.generate_image(
        prompt="A cute cat sitting on a windowsill, digital art, cute",
        output_path=output_path,
        verbose=True
    )

    if result["success"]:
        print(f"\n✅ 测试通过！图片已保存到: {result['output_path']}")
        return True
    else:
        print(f"\n❌ 测试失败: {result.get('error', '未知错误')}")
        return False


def test_custom_output():
    """测试自定义输出路径"""
    print("\n" + "=" * 50)
    print("测试2: 自定义输出路径")
    print("=" * 50)

    generator = ModelScopeImageGenerator()

    # 输出到examples目录
    output_path = os.path.join(os.path.dirname(__file__), "custom_sunset.png")

    result = generator.generate_image(
        prompt="A beautiful sunset over mountains, landscape",
        output_path=output_path,
        verbose=True
    )

    if result["success"]:
        print(f"\n✅ 测试通过！图片已保存到: {result['output_path']}")
        return True
    else:
        print(f"\n❌ 测试失败: {result.get('error', '未知错误')}")
        return False


def test_english_prompt():
    """测试英文prompt效果"""
    print("\n" + "=" * 50)
    print("测试3: 英文Prompt")
    print("=" * 50)

    generator = ModelScopeImageGenerator()

    # 输出到examples目录
    output_path = os.path.join(os.path.dirname(__file__), "test_robot.jpg")

    result = generator.generate_image(
        prompt="A futuristic robot in a cyberpunk city, neon lights, highly detailed, 8K",
        output_path=output_path,
        verbose=True
    )

    if result["success"]:
        print(f"\n✅ 测试通过！图片已保存到: {result['output_path']}")
        return True
    else:
        print(f"\n❌ 测试失败: {result.get('error', '未知错误')}")
        return False


def main():
    """运行所有测试"""
    print("🚀 开始测试ModelScope图片生成器")
    print()

    results = []

    # 运行测试
    results.append(("基本生成", test_basic_generation()))
    results.append(("自定义路径", test_custom_output()))
    results.append(("英文Prompt", test_english_prompt()))

    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！技能工作正常。")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查配置和网络连接。")
        return 1


if __name__ == "__main__":
    exit(main())
