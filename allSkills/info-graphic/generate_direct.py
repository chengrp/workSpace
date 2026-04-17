# -*- coding: utf-8 -*-
"""
直接调用 Google AI API 生成信息图
"""
import requests
import json
import base64
import os
from datetime import datetime

API_KEY = os.environ.get('ALL_IMAGE_GOOGLE_API_KEY', '')
MODEL = "gemini-3-pro-image-preview"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

if not API_KEY:
    print("请设置 ALL_IMAGE_GOOGLE_API_KEY 环境变量")
    exit(1)

def generate_image(prompt, filename_prefix, ratio="3:4"):
    """Generate image using Google AI API"""
    url = f"{BASE_URL}/models/{MODEL}:generateContent?key={API_KEY}"

    # Add aspect ratio to prompt
    full_prompt = f"{prompt}\n\nAspect ratio: {ratio}."

    data = {
        "contents": [{"parts": [{"text": full_prompt}]}]
    }

    response = requests.post(url, json=data, timeout=180)

    if response.status_code == 200:
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            image_data = result['candidates'][0]['content']['parts'][0]['inlineData']['data']
            image_bytes = base64.b64decode(image_data)

            # Save image
            output_dir = "C:/Users/RyanCh/.claude/skills/info-graphic/output/ai_agent_article/images"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{filename_prefix}_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, 'wb') as f:
                f.write(image_bytes)

            return True, filepath
    return False, response.text

# Prompts for 5 images
prompts = [
    {
        "name": "01_六把刀拆解旧世界",
        "prefix": "six_blades",
        "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

CASE FILE: 六把刀拆解旧世界

AESTHETIC:
Mixed-Media Scrapbook with torn paper edges, paper clips, red push pins
Vintage Earth Tones: Kraft paper brown background, cream white content areas
Typography: Typewriter fonts, handwritten annotations

CONTENT MODULES:

[MODULE 1: TRIGGER EVENT]
IBM暴跌13% | 2000年来最大跌幅 | 市值蒸发310亿美元
日期：2025年2月23日 | TRIGGER EVENT

[MODULE 2: 第一刀 DAU]
旧：DAU=资产 | 网络效应=指数增长
新：AI每多1用户=多烧1份推理成本
微信网状拓扑 vs ChatGPT星型拓扑
DAU从资产变为负债

[MODULE 3: 第二三刀]
工具→平台失效：AI直接给完美结果
SaaS危机：Agent才是新用户(2A)
社区价值基础坍塌

[MODULE 4: 第四五刀]
AI应用思维→服务Agent思维
注意力经济→生产力经济
零和博弈→双赢创造价值

[MODULE 5: 第六刀]
出海已死：Agent世界没有海
只需API+文档
全世界Agent自动调用

[MODULE 6: 旧地图碎裂]
六刀砍完，旧地图碎了一地
DAU、平台、SaaS、应用、注意力、出海全部失效

VISUAL ELEMENTS:
Red string connectors, paper clips, highlighter marks
Stamp: PARADIGM SHIFT DETECTED
Evidence numbers: circled 1-6

CRITICAL: All text in CHINESE
Aspect ratio: 3:4 portrait'''
    },
    {
        "name": "02_奇点后的智能变革",
        "prefix": "singularity",
        "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

CASE FILE: 奇点后的智能变革

AESTHETIC:
Mixed-Media Scrapbook with torn paper edges, red push pins
Vintage Earth Tones: Kraft paper brown, cream white areas

CONTENT MODULES:

[MODULE 1: 窗口关闭]
200美金时代：大学生=CEO
窗口关闭：开发者月消耗过千
未来：有人月花10万美金，有人只花20美金

[MODULE 2: 边际成本→0]
培养人类专家：20年
复制Agent：只需算力
智能边际成本→0
认知劳动者价值→0

[MODULE 3: Agent爆发]
一个人管几十上百Agent
每个Agent分裂子Agent
顶级智能成本无上限
差距指数级扩大

[MODULE 4: 认知劳动危机]
内容、分析、研究
不把Agent协作拉到极限
产出<电费成本

[MODULE 5: 推演结论]
纯认知劳动边际成本→0
纯认知劳动者价值→0

[MODULE 6: 证据编号]
来源：我们，已迈过奇点
作者：赛博禅心

VISUAL ELEMENTS:
Red string: 边际成本→劳动者价值→0
Highlight: 20年 vs 只需算力
Stamp: PARADIGM SHIFT CONFIRMED

CRITICAL: All text in CHINESE
Aspect ratio: 3:4'''
    },
    {
        "name": "03_算力权力结构重组",
        "prefix": "power_structure",
        "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

CASE FILE: 算力权力结构重组

AESTHETIC:
Mixed-Media Scrapbook with torn edges, paper clips, red pins
Vintage Earth Tones: Kraft brown, cream white

CONTENT MODULES:

[MODULE 1: 算力=新石油]
核心生产资料：算力
被少数公司垄断
每次API调用=缴纳算力地租

[MODULE 2: 正反馈循环]
更多算力→更好结果→更多收入→更多算力
差距只会越来越大
循环一旦转动，无法停止

[MODULE 3: 劳动力议价权丧失]
旧：资本需要劳动力=人有筹码
新：Agent替代劳动力
你不干，Agent可以干

[MODULE 4: 连锁反应]
议价权↓→政治影响力↓
劳动者政策更难推行
财富向算力拥有者集中

[MODULE 5: 三层结构]
第一层：算力拥有者(全球几千人)
掌握模型、芯片、能源、数据
定义规则，制定Token价格

第二层：算力驱动者
有资源购买算力
驱动上百Agent=中型公司

第三层：算力依附者(大多数人)
物质生活不差
权力被边缘化

[MODULE 6: 舒服≠自由]
第三层不会饿死
可能比今天中产还好
但舒适≠自由
中世纪农奴：年工作150天
现代打工人：年工作250天+

VISUAL ELEMENTS:
Pyramid diagram: 三层结构
Red string: 正反馈→三层固化
Stamp: POWER STRUCTURE ANALYSIS

CRITICAL: All text in CHINESE
Aspect ratio: 3:4'''
    },
    {
        "name": "04_软件世界的静默转向",
        "prefix": "software_shift",
        "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

CASE FILE: 软件世界的静默转向

AESTHETIC:
Mixed-Media Scrapbook with torn edges, paper clips
Vintage Earth Tones: Kraft brown, cream white

CONTENT MODULES:

[MODULE 1: Obsidian CLI]
笔记应用突然有命令行接口
创建、读取、编辑、删除
搜索、任务、标签
全部命令化

[MODULE 2: 给Agent用的]
这个CLI压根不是给人用的
是给AI Agent用的
以人为中心→悄无声息转向

[MODULE 3: EvoMap进化系统]
AI不只执行任务
积累经验、传承策略、持续进化
记忆+自我优化
边际效率越来越高

[MODULE 4: 趋势判断]
不是个例，是趋势
传统应用为Agent开发接口
Agent迭代加剧
差距快速拉大

[MODULE 5: 人类vs机器]
人类：停止学习=停滞
机器：持续优化=提升
机器优化，人类停止
差距指数扩大

[MODULE 6: 软件世界转向]
路还没修好，但速度在加剧
软件世界已静默转向
以人为中心→以Agent为中心

[MODULE 7: 证据标签]
观察日期：2025年春节后
关键事件：Obsidian CLI、EvoMap
趋势：Agent原生接口爆发

VISUAL ELEMENTS:
Split: 人类中心 vs Agent中心
Red string: 给Agent用→软件转向
Stamp: PARADIGM SHIFT IN PROGRESS

CRITICAL: All text in CHINESE
Aspect ratio: 3:4'''
    },
    {
        "name": "05_普通人行动指南",
        "prefix": "action_guide",
        "prompt": r'''Create a high-density infographic in "Archival Scrapbook / Detective Evidence Board" style.

CASE FILE: 普通人行动指南

AESTHETIC:
Mixed-Media Scrapbook with torn edges, paper clips
Vintage Earth Tones: Kraft brown, cream white
Visual elements: Checklist boxes, priority stamps

CONTENT MODULES:

[MODULE 1: 重新审视可替代性]
Agent不需要睡觉、工资、24小时工作
能在多大程度上替代我？
真正提供价值的是什么？
不要焦虑，要定位

[MODULE 2: 与Agent协作成核心能力]
未来差距=能驱动多少Agent
把复杂任务拆成20个子任务
设计每个Agent的指令和工作流
处理依赖和异常

[MODULE 3: 把Agent当同事]
不是工具，是同事
学习给清晰目标
怎么拆解复杂任务
怎么验证输出

[MODULE 4: 关注算力分布]
短期：算力集中，三层固化
长期：能源、芯片、开源生态
关注这些遥远的东西
决定你在三层结构的位置

[MODULE 5: 创业建议]
别做更好的工具
做新世界基建
Agent原生基础设施
欲望的催化剂

[MODULE 6: 下一代教育]
四年学的技能，毕业前被Agent掌握
AI时代窗口期极短且缩小
不只是知识传授
更重要的是：欲望想象力、定义问题、跟AI协作、选择智慧

[MODULE 7: 行动优先级]
checklist: 审视可替代性
checklist: Agent协作核心能力
checklist: 关注算力分布
checklist: 新世界基建
checklist: 教育重心转移

VISUAL ELEMENTS:
Checklist boxes with priorities
Priority stamps: circled 1-5
Highlight: 欲望的催化剂
Stamp: ACTION REQUIRED

CRITICAL: All text in CHINESE
Aspect ratio: 3:4'''
    }
]

print("Starting generation of 5 archival style infographics...")
print("=" * 50)

for i, p in enumerate(prompts, 1):
    print(f"\n[{i}/5] Generating: {p['name']}...")

    success, result = generate_image(p['prompt'], p['prefix'])

    if success:
        print(f"    SUCCESS! Saved to: {result}")
    else:
        print(f"    FAILED: {result}")

print("\n" + "=" * 50)
print("Generation complete!")
