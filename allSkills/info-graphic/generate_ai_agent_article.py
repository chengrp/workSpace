# -*- coding: utf-8 -*-
"""
生成《当智能不再稀缺》信息图 - 档案风
"""
import sys
import os

# Add all-image to path
sys.path.insert(0, 'C:/Users/RyanCh/.claude/skills/all-image')

try:
    from all_image import ImageGenerator

    gen = ImageGenerator()

    prompts = [
        {
            "name": "六把刀拆解旧世界",
            "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

=== CASE FILE: 六把刀拆解旧世界 ===

**AESTHETIC:**
Mixed-Media Scrapbook with torn paper edges, paper clips, red push pins, dashed line connectors
Vintage Earth Tones: Kraft paper brown background, cream white content areas
Typography: Typewriter fonts for headers, handwritten notes for annotations
Visual elements: Polaroid-style photo frames, highlighter marks, stamped dates

**LAYOUT:**
Detective evidence board style with 6-7 distinct "clipped document" modules
Hand-drawn arrows connecting related information
Paperclip and tape textures for authentic archival feel

**CONTENT MODULES (6-7):**

[MODULE 1: TRIGGER EVENT - Polaroid frame]
IBM暴跌13% / 2000年来最大跌幅 / 市值蒸发310亿美元
日期：2025年2月23日
标签：TRIGGER / CASE OPENER

[MODULE 2: 第一刀 DAU - Clipped document]
旧逻辑：DAU = 资产 / 网络效应 = 指数增长
新现实：AI每多1用户 = 多烧1份推理成本
微信：网状拓扑√ | ChatGPT：星型拓扑×
结论：DAU从资产变为负债

[MODULE 3: 第二三刀 - Torn paper section]
工具→平台路径失效：AI直接给完美结果，无需社区补充
SaaS危机：人口饱和，Agent才是新用户（2A to Agent时代）
社区价值基础坍塌

[MODULE 4: 第四五刀 - Red highlighter marks]
"AI应用"是错的思维 → 应该"服务Agent"
注意力经济 → 生产力经济
零和博弈 → 双方创造价值

[MODULE 5: 第六刀 - Paper clip attached]
出海已死：Agent世界没有海
只需做好API + 文档
全世界Agent自动调用

[MODULE 6: 旧世界地图碎裂 - Stamped graphic]
六刀砍完，旧地图碎了一地
DAU、平台、SaaS、应用、注意力、出海 - 全部失效

**VISUAL ELEMENTS:**
Red string connectors, paper clip, highlighter marks
Stamp: PARADIGM SHIFT DETECTED
Evidence numbers: ①, ②, ③, ④, ⑤, ⑥

CRITICAL: All text must be in CHINESE except stylistic elements like "CASE FILE", "TRIGGER", "EVIDENCE"
Aspect ratio: 3:4 portrait'''
        },
        {
            "name": "奇点后的智能变革",
            "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

=== CASE FILE: 奇点后的智能变革 ===

**AESTHETIC:**
Mixed-Media Scrapbook with torn paper edges, paper clips, red push pins
Vintage Earth Tones: Kraft paper brown background, cream white content areas

**CONTENT MODULES (6-7):**

[MODULE 1: 窗口关闭 - Polaroid frame]
200美金时代：刚毕业大学生 = CEO
窗口正在关闭：重度开发者月消耗过千
未来：有人月花10万美金，有人只花20美金

[MODULE 2: 边际成本→0 - Clipped document]
培养人类专家：需要20年
复制同等Agent：只需算力
智能边际生产成本：第一次接近于零
认知劳动者经济价值：趋近于零

[MODULE 3: Agent爆发 - Torn paper section]
一个人管着几十上百个Agent
每个Agent分裂出子Agent
顶级智能消耗成本：没有上限
差距：指数级扩大

[MODULE 4: 认知劳动危机 - Red highlighter marks]
做内容、做分析、做研究
如果不把跟Agent协作能力拉到极限
产出很快就会低于产出它所需的电费

[MODULE 5: 推演结论 - Stamped graphic]
纯认知劳动的边际成本趋近于零
纯认知劳动者的经济价值也趋近于零

[MODULE 6: 证据编号 - Evidence tag]
来源：《我们，已迈过奇点》
作者：赛博禅心

**VISUAL ELEMENTS:**
Red string from "边际成本→0" to "劳动者价值→0"
Highlighter marks on "20年" vs "只需算力"
Stamp: PARADIGM SHIFT CONFIRMED

CRITICAL: All text must be in CHINESE
Aspect ratio: 3:4 portrait'''
        },
        {
            "name": "算力权力结构重组",
            "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

=== CASE FILE: 算力权力结构重组 ===

**AESTHETIC:**
Mixed-Media Scrapbook with torn paper edges, paper clips, red push pins
Vintage Earth Tones: Kraft paper brown background, cream white content areas

**CONTENT MODULES (6-7):**

[MODULE 1: 算力=新石油 - Polaroid frame]
核心生产资料：算力
正在被少数公司垄断
每次API调用 = 缴纳算力地租

[MODULE 2: 正反馈循环 - Diagram]
更多算力 → 更好结果 → 更多收入 → 买更多算力
差距只会越来越大
循环一旦转动，无法停止

[MODULE 3: 劳动力议价权丧失 - Clipped document]
旧前提：资本需要劳动力 = 人有筹码
新现实：Agent替代劳动力本身
你不干，Agent可以干

[MODULE 4: 连锁反应 - Torn paper section]
劳动者议价权↓ → 政治影响力↓
有利于劳动者的政策更难推行
财富向算力拥有者集中

[MODULE 5: 三层结构 - Hierarchy diagram]
第一层：算力拥有者（全球几千人）
- 掌握模型、芯片、能源、数据
- 定义规则，制定Token价格

第二层：算力驱动者
- 有资源购买算力
- 驱动上百个Agent = 过去中型公司

第三层：算力依附者（大多数人）
- 物质生活不差
- 权力结构被边缘化

[MODULE 6: 舒服≠自由 - Handwritten note]
第三层的人不会饿死
可能过得比今天中产还好
但舒适和自由是两回事
中世纪农奴：年工作150天
现代打工人：年工作250天以上

**VISUAL ELEMENTS:**
Pyramid diagram showing three layers
Red string from "正反馈循环" to "三层结构固化"
Stamp: POWER STRUCTURE ANALYSIS

CRITICAL: All text must be in CHINESE
Aspect ratio: 3:4 portrait'''
        },
        {
            "name": "软件世界的静默转向",
            "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

=== CASE FILE: 软件世界的静默转向 ===

**AESTHETIC:**
Mixed-Media Scrapbook with torn paper edges, paper clips, red push pins
Vintage Earth Tones: Kraft paper brown background, cream white content areas

**CONTENT MODULES (6-7):**

[MODULE 1: Obsidian CLI - Polaroid frame]
笔记应用突然有命令行接口
创建、读取、编辑、删除笔记
搜索内容、管理任务、操作标签
全部命令化

[MODULE 2: 给Agent用的 - Red highlighter marks]
这个CLI压根就不是给人用的
是给AI Agent用的
以人为中心的软件世界
正在悄无声息地转向

[MODULE 3: EvoMap进化系统 - Clipped document]
让AI不只执行任务
而是积累经验、传承策略、持续进化
当系统拥有"记忆"与"自我优化"能力
边际效率会越来越高

[MODULE 4: 趋势判断 - Torn paper section]
不是个例，而会是一个趋势
很多传统应用都会为AI Agent开发接口
Agent迭代在加剧
差距快速拉大

[MODULE 5: 人类vs机器 - Comparison chart]
人类：停止学习 = 能力停滞
机器：持续优化 = 效率提升
当机器持续优化，人类停止学习
差距会指数级扩大

[MODULE 6: 软件世界转向 - Stamped graphic]
路，还远远没修好
但速度在加剧
软件世界已静默转向
从以人为中心 → 到以Agent为中心

**VISUAL ELEMENTS:**
Split diagram: Human-Centered vs Agent-Centered
Red string from "给Agent用的" to "软件世界转向"
Stamp: PARADIGM SHIFT IN PROGRESS

CRITICAL: All text must be in CHINESE
Aspect ratio: 3:4 portrait'''
        },
        {
            "name": "普通人行动指南",
            "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

=== CASE FILE: 普通人行动指南 ===

**AESTHETIC:**
Mixed-Media Scrapbook with torn paper edges, paper clips, red push pins
Vintage Earth Tones: Kraft paper brown background, cream white content areas
Visual elements: Checklist boxes, priority stamps, action arrows

**CONTENT MODULES (6-7):**

[MODULE 1: 重新审视可替代性 - Question mark]
Agent不需要睡觉、不需要工资、24小时工作
能在多大程度上替代我现在做的事？
真正提供价值的那个部分是什么？
不要焦虑，要定位

[MODULE 2: 与Agent协作成核心能力 - Red highlighter marks]
未来人和人的差距
不取决于你自己能做什么
而在乎你能驱动多少Agent为你做事
把复杂任务拆成20个子任务
设计好每个Agent的指令和工作流

[MODULE 3: 把Agent当同事 - Clipped document]
不是工具，是同事
学习给它清晰的目标
怎么拆解复杂任务
怎么验证它的输出

[MODULE 4: 关注算力分布 - Torn paper section]
短期：算力持续集中，三层社会固化
长期：取决于能源技术、芯片产业、开源生态
关注这些看似遥远的东西
最终决定你在三层结构中的位置

[MODULE 5: 创业建议 - Stamped graphic]
别做"更好的工具"
做"新世界的基建"
Agent原生基础设施：让Agent直接通信、交易、交互
欲望的催化剂：AGI能满足任何欲望，但不能制造欲望

[MODULE 6: 下一代教育 - Handwritten notes]
花四年学的技能，毕业前就被Agent掌握了
AI时代教育窗口期极短，而且在缩小
教育价值不应只是知识传授
更重要的是：欲望和想象力的保护、定义问题的能力、跟AI协作的习惯

**VISUAL ELEMENTS:**
Checklist boxes for action items
Priority stamps: ①②③④⑤
Highlighter marks on "欲望的催化剂"
Stamp: ACTION REQUIRED

CRITICAL: All text must be in CHINESE
Aspect ratio: 3:4 portrait'''
        }
    ]

    print("📋 开始生成5张档案风信息图...")
    print("=" * 50)

    for i, p in enumerate(prompts, 1):
        print(f"\n🖼️  正在生成第{i}张：{p['name']}...")
        result = gen.generate(
            prompt=p['prompt'],
            ratio='3:4',
            quality='4k',
            mode='quality',
            auto_fallback=True
        )

        if result.success:
            print(f"   ✅ 成功! Provider: {result.provider}")
            print(f"   📁 路径: {result.image_path}")
        else:
            print(f"   ❌ 失败: {result.error}")
            if result.suggestions:
                print(f"   💡 建议: {result.suggestions}")

    print("\n" + "=" * 50)
    print("🎉 生成完成!")

except ImportError as e:
    print(f"❌ 无法导入 all-image 模块: {e}")
    print("💡 请确保 all-image 技能已正确安装")
    sys.exit(1)
except Exception as e:
    print(f"❌ 生成过程出错: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
