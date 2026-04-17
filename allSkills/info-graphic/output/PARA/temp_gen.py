import sys
import os

# 添加 all-image 模块路径
all_image_path = 'd:/ProjectAI/CC/CC_record/skills/all-image'
if all_image_path not in sys.path:
    sys.path.insert(0, all_image_path)

# 导入 ImageGenerator
import importlib.util
spec = importlib.util.spec_from_file_location("all_image", f"{all_image_path}/__init__.py")
all_image = importlib.util.module_from_spec(spec)
sys.modules['all_image'] = all_image
spec.loader.exec_module(all_image)

ImageGenerator = all_image.ImageGenerator

gen = ImageGenerator()

prompt = """Stationery Style infographic about PARA Method. ALL TEXT MUST BE IN CHINESE.

Main Title: PARA 信息管理法则 - 打造第二大脑

Visual Composition: A vertical cream-colored clipboard (#F5F5DC) with layered 3D folders and index tabs. Klein Blue (#002FA7) accents, Vibrant Orange (#FF6B35) emphasis, Soft Grey text.

7 Content Modules arranged as document sheets:

Module 1 - 四分类命名:
Projects 项目 · Areas 领域 · Resources 资源 · Archives 归档

Module 2 - 分类对比:
❌ 按主题: 编程/营销/设计/写作
✅ 按行动频率: 正在做/长期关注/可能用到/已完成

Module 3 - 时间跨度标准:
Projects: 天/周/月 | Areas: 年/永久 | Resources: 永久 | Archives: 永久存储

Module 4 - 判断标准流程:
这是要立即做的任务吗？ → Projects
这是长期关注的事吗？ → Areas
这对未来有价值吗？ → Resources
不再需要 → Archives

Module 5 - 适用场景:
Projects: 发布产品/学Python/装修房子
Areas: 健康/财务/职业发展
Resources: 设计灵感/文章收藏/教程
Archives: 2023年项目/旧工作文档

Module 6 - 常见误区:
⚠️ 不要按主题分类
⚠️ 不要把 Areas 当 Projects
⚠️ 定期归档，不要囤积

Module 7 - 快速决策:
新信息 → Resources（收集）
需要行动 → Projects（执行）
完成后 → Archives（归档）
长期关注 → Areas（维护）

Style: Neo-skeuomorphism stationery, 3D render, clean organized, index tabs, 3D mouse cursor decoration, notification icons. High-density information layout."""

result = gen.generate(
    prompt=prompt,
    ratio='3:4',
    quality='4k',
    mode='quality'
)

if result.success:
    print(f'✅ {result.image_path}')
else:
    print(f'❌ {result.error}')
