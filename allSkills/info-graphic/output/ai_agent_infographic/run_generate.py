#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 AI 时代变革信息图
"""
import sys
import os
from pathlib import Path

# 获取 all-image 的绝对路径
all_image_path = Path('d:/ProjectAI/CC/CC_record/skills/all-image').resolve()
all_image_parent = str(all_image_path.parent)

# 添加父目录到 sys.path
if all_image_parent not in sys.path:
    sys.path.insert(0, all_image_parent)

# 导入 all_image 模块
import all_image
ImageGenerator = all_image.ImageGenerator

# 构建提示词
prompt = '''当智能不再稀缺 - 时代变革账单

Create a high-density infographic in Receipt Ticket Aesthetic style (打印热敏纸风).

=== CONTENT (7 modules) ===
TITLE: 当智能不再稀缺 - 时代变革账单

Module 01: 信号事件 - IBM暴跌13%，一天蒸发310亿美元，认知劳动边际成本趋零的信号
Module 02: 六把刀理论 - DAU失效、平台化路径断裂、SaaS转向2A、AI应用概念错误、注意力经济过时、出海概念消亡
Module 03: 奇点推演 - 智能可无限生产，200美金就能买到CEO级能力，窗口正在关闭
Module 04: 三层社会 - 第一层算力拥有者(定义规则)、第二层算力驱动者(调度Agent)、第三层算力依附者(被边缘化)
Module 05: 变化信号 - Obsidian CLI发布、EvoMap进化型系统、Agent雇佣人类、企业减员增效引入AI
Module 06: 行动清单 - 重新审视可替代性、学会驱动Agent协作、关注算力和能源分布、创业做新世界基建、教育重心转移
Module 07: 金句收尾 - 悲观者是远见，乐观者才是智慧

=== STYLE: Receipt Ticket Aesthetic ===
- Receipt format vertical layout with perforated edges on both sides
- 3D/Claymorphism rendered icons (currency, charts, AI chip, social hierarchy, signal lights)
- Monospace/pixel font headers (retro digital receipt printer style)
- Clean sans-serif body text with high readability
- White/Off-white thermal paper texture background
- Colors: Pure black text #000000, Cyan accents #00AEEF, Yellow highlights #FFD100, Orange call-to-action #FF6B35
- Receipt sequence numbers, date stamps, time stamps
- Hand-drawn style checkboxes with fluorescent marker effects
- High information density, no empty white space
- Modern skeuomorphism design with claymorphism icons

Style Keywords: receipt, ticket, 3D-icons, perforated, sequential, claymorphism, modern-skeuomorphism

CRITICAL LANGUAGE REQUIREMENT:
- ALL content text MUST be in CHINESE (中文)
- DO NOT translate any Chinese content to English
- Keep all titles, labels, and content in original Chinese
- Numbers and symbols can remain as-is
- This is a non-negotiable requirement

=== OUTPUT SPECIFICATIONS ===
- Aspect Ratio: 3:4 (portrait vertical)
- Quality: 4K ultra high definition
- High information density with 7 modules
- No empty white space, fully packed with information'''

print("[INFO] Starting infographic generation...")
print(f"[STYLE] Receipt Ticket Aesthetic (打印热敏纸风)")
print(f"[RATIO] 3:4 portrait")
print(f"[QUALITY] 4K")
print("-" * 50)

# 创建生成器
gen = ImageGenerator(
    auto_fallback=True,  # 自动降级
    debug=True           # 启用调试日志
)

# 生成图片
result = gen.generate(
    prompt=prompt,
    ratio='3:4',
    quality='4k',
    mode='quality'  # 质量优先模式
)

# 输出结果
print("-" * 50)
if result.success:
    print("[SUCCESS] Image generated successfully!")
    print(f"[PROVIDER] {result.provider}")
    print(f"[PATH] {result.image_path}")
    if result.metadata:
        print(f"[TIME] {result.metadata.get('generation_time', 'N/A')} seconds")
else:
    print("[FAILED] Image generation failed")
    print(f"[ERROR] {result.error}")
    if hasattr(result, 'suggestions') and result.suggestions:
        print(f"[SUGGESTIONS] {result.suggestions}")
    if hasattr(result, 'attempted_providers'):
        print(f"[ATTEMPTED] {result.attempted_providers}")

sys.exit(0 if result.success else 1)
