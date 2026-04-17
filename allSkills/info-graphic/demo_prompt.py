#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Info-Graphic Skill - Demo Prompt Generator (Multi-Style)
支持 6 种高密度信息图风格

所有生成的提示词和图片自动保存到 output/ 文件夹
"""

import os
import re
from datetime import datetime
from pathlib import Path
from styles import INFOGRAPHIC_STYLES, get_style_by_id, display_styles

# 输出目录配置
OUTPUTS_DIR = Path(__file__).parent / "output"


def sanitize_filename(name: str) -> str:
    """清理文件名，移除非法字符"""
    # 移除或替换 Windows 文件名中的非法字符
    illegal_chars = r'[<>:"/\\|?*]'
    return re.sub(illegal_chars, '_', name)


def get_topic_folder(topic: str) -> Path:
    """获取主题对应的输出文件夹"""
    clean_name = sanitize_filename(topic)
    topic_folder = OUTPUTS_DIR / clean_name

    # 创建主题子文件夹
    (topic_folder / "prompts").mkdir(parents=True, exist_ok=True)
    (topic_folder / "images").mkdir(parents=True, exist_ok=True)

    return topic_folder


def generate_infographic_prompt(
    topic: str,
    modules: list,
    style_id: str = "1"
) -> str:
    """
    生成高密度信息图的 Prompt

    Args:
        topic: 主题（如 "AI写作工具对比"）
        modules: 模块列表（如 ["品牌阵列", "参数刻度", "功能拆解", ...]）
        style_id: 风格 ID (1-6)
    """
    style = get_style_by_id(style_id)

    prompt = f"""Create a high-density, professional information design infographic for Xiaohongshu about "{topic}".

=== CRITICAL STYLE REQUIREMENTS - {style.name.upper()} ({style.name_en.upper()}) ===

【STYLE DESCRIPTION】
{style.description}

【COLOR PALETTE】
- BACKGROUND: {style.background}
- BASE COLORS: {', '.join(style.base_colors)}
- ACCENT COLORS: {', '.join(style.accent_colors)}

【LAYOUT & INFORMATION DENSITY】
{style.layout_style}

【ILLUSTRATION & GRAPHIC ELEMENTS】
{style.visual_elements}

【TYPOGRAPHY】
{style.typography}

【AVOID】"""

    for item in style.avoid:
        prompt += f"\n- {item}"

    prompt += f"""

【SPECIFIC MODULE STRUCTURE - MUST HAVE {len(modules)}】"""

    # Add modules
    for i, module in enumerate(modules, 1):
        prompt += f"\n- [MOD {i}: {module.upper()}]"

    prompt += f"""

【STYLE KEYWORDS】
{', '.join(style.keywords)}

Aspect Ratio: 3:4 (Portrait)"""

    return prompt


def save_prompt_to_file(topic: str, style_name: str, prompt: str) -> Path:
    """
    保存提示词到文件

    Args:
        topic: 主题名称
        style_name: 风格名称
        prompt: 生成的提示词内容

    Returns:
        保存的文件路径
    """
    topic_folder = get_topic_folder(topic)
    prompts_folder = topic_folder / "prompts"

    # 生成文件名: 主题_风格_Prompt.txt
    clean_topic = sanitize_filename(topic)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{clean_topic}_{style_name}_Prompt.txt"
    filepath = prompts_folder / filename

    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(prompt)

    return filepath


def interactive_prompt():
    """交互式 Prompt 生成器"""
    print("=" * 70)
    print("高密度信息图 Prompt 生成器 - 多风格版本")
    print("=" * 70)
    print()

    # Step 1: 显示所有风格
    display_styles()

    # Step 2: 选择风格
    print("\n请选择风格 (输入数字 1-6，直接回车使用默认风格 1):")
    style_choice = input("风格选择 > ").strip()

    if not style_choice:
        style_choice = "1"
    elif style_choice not in INFOGRAPHIC_STYLES:
        print(f"无效的选择，使用默认风格 1")
        style_choice = "1"

    selected_style = get_style_by_id(style_choice)
    print(f"\n已选择风格: {selected_style.name}")
    print()

    # Step 3: 输入主题
    print("请输入信息图主题 (例如: AI写作工具对比):")
    topic = input("主题 > ").strip()

    if not topic:
        topic = "AI写作工具对比"
        print(f"使用默认主题: {topic}")

    # Step 4: 输入模块数量
    print("\n请输入模块数量 (1-8，直接回车使用默认 6):")
    module_count_input = input("模块数量 > ").strip()

    try:
        module_count = int(module_count_input) if module_count_input else 6
        module_count = max(1, min(8, module_count))
    except ValueError:
        module_count = 6

    print(f"\n将生成 {module_count} 个模块")
    print()

    # Step 5: 输入模块描述 (可选)
    modules = []
    print("请输入每个模块的描述 (直接回车使用默认模块名称):")
    for i in range(module_count):
        default_name = f"模块 {i+1}"
        module_input = input(f"  模块 {i+1} [{default_name}] > ").strip()
        modules.append(module_input if module_input else default_name)

    # Generate prompt
    print("\n" + "=" * 70)
    print("生成的 Prompt:")
    print("=" * 70)

    prompt = generate_infographic_prompt(topic, modules, style_choice)
    print(prompt)

    # Save to file
    filepath = save_prompt_to_file(topic, selected_style.name.split("·")[0], prompt)

    # Usage instructions
    print("\n" + "=" * 70)
    print("使用方式:")
    print("=" * 70)
    print(f"""
风格: {selected_style.name}
主题: {topic}
模块: {module_count} 个

提示词已保存到:
  {filepath}

1. 复制上述 Prompt 到 all-image 技能
2. 设置 ratio="3:4", quality="4k", mode="quality"
3. 调用 Google AI Nano Banana Pro 4K 模型生成
4. 生成的图片将保存到: {filepath.parent.parent / "images"}

Python 示例:
    from all_image import ImageGenerator
    gen = ImageGenerator()
    result = gen.generate(
        prompt="<上述 Prompt>",
        ratio="3:4",
        quality="4k",
        mode="quality"
    )
    """)

    return prompt


def quick_demo():
    """快速演示 - 使用默认参数"""
    print("=" * 60)
    print("Info-Graphic Skill - 快速演示")
    print("=" * 60)

    # 测试所有 6 种风格
    topic = "AI写作工具对比"
    modules = ["品牌阵列", "参数刻度", "功能拆解", "场景对比", "避坑警告", "速查表格"]

    for style_id in INFOGRAPHIC_STYLES.keys():
        style = get_style_by_id(style_id)

        print(f"\n{'=' * 60}")
        print(f"风格 {style_id}: {style.name}")
        print(f"{'=' * 60}")

        prompt = generate_infographic_prompt(topic, [m.split()[0] for m in modules], style_id)

        # 显示预览 (前500字符)
        print("Prompt 预览 (前 500 字符):")
        print("-" * 60)
        print(prompt[:500] + "...")
        print()

    print("=" * 60)
    print("所有风格演示完成！")


def main():
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        quick_demo()
    else:
        interactive_prompt()


if __name__ == "__main__":
    main()
