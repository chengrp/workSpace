"""
ms-image 增强功能测试脚本
测试新功能：风格模板、Prompt优化、额度管理、批量生成
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from ms_image_enhanced import (
    EnhancedImageGenerator,
    PromptOptimizer,
    QuotaManager,
    STYLE_TEMPLATES
)


def test_prompt_optimizer():
    """测试Prompt优化器"""
    print("\n" + "="*60)
    print("🧪 测试1: Prompt优化器")
    print("="*60)

    # 测试1: 基础优化
    original = "A golden cat"
    enhanced = PromptOptimizer.enhance(original)
    print(f"\n原始: {original}")
    print(f"优化: {enhanced}")

    # 测试2: 配合风格模板
    cyberpunk_prompt = PromptOptimizer.enhance("A cityscape", style="cyberpunk")
    print(f"\n赛博朋克风格: {cyberpunk_prompt}")

    # 测试3: 水彩画风格
    watercolor_prompt = PromptOptimizer.enhance("A landscape", style="watercolor")
    print(f"水彩画风格: {watercolor_prompt}")

    print("\n✅ Prompt优化器测试完成")


def test_style_templates():
    """测试风格模板"""
    print("\n" + "="*60)
    print("🧪 测试2: 风格模板")
    print("="*60)

    print(f"\n可用风格数量: {len(STYLE_TEMPLATES)}")
    print("\n所有风格列表:")
    for key, value in STYLE_TEMPLATES.items():
        print(f"  {key:15} - {value['name']}")

    print("\n✅ 风格模板测试完成")


def test_quota_manager():
    """测试额度管理器"""
    print("\n" + "="*60)
    print("🧪 测试3: 额度管理器")
    print("="*60)

    # 使用测试文件
    quota_manager = QuotaManager(quota_file="quota_test.json")

    print(f"\n当前已用: {quota_manager.get_used()}")
    print(f"剩余额度: {quota_manager.get_remaining()}")

    # 模拟使用
    print("\n模拟使用5张额度...")
    quota_manager.record_usage(5)

    print(f"使用后已用: {quota_manager.get_used()}")
    print(f"使用后剩余: {quota_manager.get_remaining()}")

    # 清理测试文件
    if os.path.exists("quota_test.json"):
        os.remove("quota_test.json")

    print("\n✅ 额度管理器测试完成")


def test_enhanced_generator_basic():
    """测试增强版生成器（基础功能）"""
    print("\n" + "="*60)
    print("🧪 测试4: 增强版生成器 - Prompt优化")
    print("="*60)

    generator = EnhancedImageGenerator()

    # 模拟生成（不实际调用API）
    print("\n测试Prompt优化功能:")
    test_prompts = [
        ("A cat", None),
        ("A city", "cyberpunk"),
        ("A portrait", "realistic")
    ]

    for prompt, style in test_prompts:
        optimized = PromptOptimizer.enhance(prompt, style=style)
        style_name = STYLE_TEMPLATES[style]['name'] if style else "无风格"
        print(f"\n风格: {style_name}")
        print(f"  原始: {prompt}")
        print(f"  优化: {optimized}")

    print("\n✅ 增强版生成器基础测试完成")


def test_batch_generation_preview():
    """预览批量生成功能"""
    print("\n" + "="*60)
    print("🧪 测试5: 批量生成功能预览")
    print("="*60)

    print("\n批量生成示例:")
    print("  命令: python scripts/ms_image_enhanced.py 'A golden cat' --batch 4")
    print("  说明: 一次性生成4张不同角度的猫咪图片")
    print("  输出: image/batch/batch_1_xxx.jpg, batch_2_xxx.jpg, ...")

    print("\n配合风格模板:")
    print("  命令: python scripts/ms_image_enhanced.py 'A city' --style cyberpunk --batch 3")
    print("  说明: 生成3张赛博朋克风格的城市图片")

    print("\n✅ 批量生成功能预览完成")


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("🚀 ms-image 增强功能测试套件")
    print("="*60)

    try:
        # 运行测试
        test_prompt_optimizer()
        test_style_templates()
        test_quota_manager()
        test_enhanced_generator_basic()
        test_batch_generation_preview()

        # 总结
        print("\n" + "="*60)
        print("✅ 所有测试完成！")
        print("="*60)
        print("\n新增功能:")
        print("  ✨ 8种预设风格模板")
        print("  ✨ Prompt智能优化")
        print("  ✨ 额度管理系统")
        print("  ✨ 批量生成功能")
        print("\n开始使用:")
        print("  python scripts/ms_image_enhanced.py --help")
        print("  python scripts/ms_image_enhanced.py --list-styles")
        print("  python scripts/ms_image_enhanced.py --quota")
        print("")

    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
