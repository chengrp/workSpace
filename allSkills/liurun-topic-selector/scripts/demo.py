#!/usr/bin/env python3
"""
刘润选题智能体 - 演示版 (使用模拟数据)
展示完整的选题推荐功能
"""

import sys
from datetime import datetime
from pathlib import Path

# 模拟新闻数据
MOCK_EVENTS = [
    {
        'title': '比亚迪2024年财报发布：营收增长50%，新能源车销量突破300万辆',
        'url': 'https://www.example.com/byd-2024-report',
        'source': '36氪',
        'published': datetime.now(),
        'summary': '比亚迪今日发布2024年财报，全年营收突破6000亿元，同比增长50%。新能源车销量达到300万辆，超越特斯拉成为全球第一。',
        'event_type': '财报业绩',
        'key_numbers': ['50%', '300万辆', '6000亿'],
        'entities': ['比亚迪', '特斯拉'],
        'impact_score': 88,
        'relevance_score': 75
    },
    {
        'title': '英伟达发布新一代AI芯片H200，性能提升30%',
        'url': 'https://www.example.com/nvidia-h200',
        'source': '晚点LatePost',
        'published': datetime.now(),
        'summary': '英伟达正式发布新一代数据中心AI芯片H200，采用HBM3e内存，在AI训练场景下性能相比H100提升30%。',
        'event_type': '产品发布',
        'key_numbers': ['H200', '30%', 'HBM3e'],
        'entities': ['Nvidia', '英伟达'],
        'impact_score': 85,
        'relevance_score': 80
    },
    {
        'title': '理想汽车宣布裁员15%，组织架构调整以应对价格战',
        'url': 'https://www.example.com/li-auto-restructure',
        'source': '虎嗅',
        'published': datetime.now(),
        'summary': '理想汽车CEO李想发布内部信，宣布裁员15%以优化组织效率，应对新能源车市场的激烈价格竞争。',
        'event_type': '组织调整',
        'key_numbers': ['15%'],
        'entities': ['理想', '李想'],
        'impact_score': 78,
        'relevance_score': 72
    },
    {
        'title': '小米SU7上市首月订单突破10万辆，雷军称将加大产能',
        'url': 'https://www.example.com/xiaomi-su7',
        'source': '界面新闻',
        'published': datetime.now(),
        'summary': '小米汽车SU7上市首月订单量突破10万辆，雷军表示将加快生产节奏，力争年底交付20万辆。',
        'event_type': '产品发布',
        'key_numbers': ['10万辆', '20万辆'],
        'entities': ['小米', '雷军'],
        'impact_score': 82,
        'relevance_score': 70
    },
    {
        'title': 'OpenAI发布GPT-4.5 Turbo，推理成本降低50%',
        'url': 'https://www.example.com/openai-gpt4-turbo',
        'source': '36氪',
        'published': datetime.now(),
        'summary': 'OpenA I低调发布GPT-4.5 Turbo模型，在保持性能的同时将API推理成本降低50%，进一步推动AI应用普及。',
        'event_type': '产品发布',
        'key_numbers': ['50%', 'GPT-4.5'],
        'entities': ['OpenAI'],
        'impact_score': 90,
        'relevance_score': 85
    },
    {
        'title': '腾讯AI实验室发布新一代多模态大模型',
        'url': 'https://www.example.com/tencent-ai',
        'source': '钛媒体',
        'published': datetime.now(),
        'summary': '腾讯AI实验室发布新一代多模态大模型混元3.0，在图像理解、视频生成等任务上达到业界领先水平。',
        'event_type': '产品发布',
        'key_numbers': ['混元3.0'],
        'entities': ['腾讯'],
        'impact_score': 75,
        'relevance_score': 68
    },
    {
        'title': '蔚来汽车推出BaaS电池租赁服务升级，租电价格下调20%',
        'url': 'https://www.example.com/nio-baas',
        'source': '36氪',
        'published': datetime.now(),
        'summary': '蔚来宣布BaaS电池租赁服务升级，标准续航电池包月租价格下调20%，进一步降低用户购车门槛。',
        'event_type': '战略调整',
        'key_numbers': ['20%', 'BaaS'],
        'entities': ['蔚来'],
        'impact_score': 70,
        'relevance_score': 65
    },
    {
        'title': '字节跳动启动今年第三轮裁员，重点调整AI业务线',
        'url': 'https://www.example.com/bytedance-ai',
        'source': '晚点LatePost',
        'published': datetime.now(),
        'summary': '字节跳动启动今年第三轮组织调整，本次重点在于优化AI业务线，整合资源聚焦核心项目。',
        'event_type': '组织调整',
        'key_numbers': ['第三轮'],
        'entities': ['字节跳动'],
        'impact_score': 72,
        'relevance_score': 63
    },
    {
        'title': '阿里云宣布大模型API调用价格全面下调，最高降幅达80%',
        'url': 'https://www.example.com/aliyun-price',
        'source': '虎嗅',
        'published': datetime.now(),
        'summary': '阿里云宣布大模型平台灵积全线产品价格下调，开源模型Qwen-72B调用价格降低80%，推动企业AI应用落地。',
        'event_type': '战略调整',
        'key_numbers': ['80%', 'Qwen-72B'],
        'entities': ['阿里', '阿里云'],
        'impact_score': 80,
        'relevance_score': 75
    },
    {
        'title': '特斯拉上海储能超级工厂投产，年产能达40GWh',
        'url': 'https://www.example.com/tesla-shanghai',
        'source': '36氪',
        'published': datetime.now(),
        'summary': '特斯拉上海储能超级工厂正式投产，年产能达40GWh，将成为全球最大的储能电池生产基地之一。',
        'event_type': '产品发布',
        'key_numbers': ['40GWh'],
        'entities': ['Tesla', '特斯拉'],
        'impact_score': 76,
        'relevance_score': 70
    },
    {
        'title': '京东物流发布智能仓储机器人，效率提升300%',
        'url': 'https://www.example.com/jd-logistics',
        'source': '界面新闻',
        'published': datetime.now(),
        'summary': '京东物流自主研发的新一代智能仓储机器人投入使用，分拣效率相比人工提升300%，大幅降低运营成本。',
        'event_type': '产品发布',
        'key_numbers': ['300%'],
        'entities': ['京东'],
        'impact_score': 65,
        'relevance_score': 60
    },
    {
        'title': '华为鸿蒙系统原生应用突破150万，生态建设加速',
        'url': 'https://www.example.com/huawei-harmony',
        'source': '36氪',
        'published': datetime.now(),
        'summary': '华为宣布鸿蒙系统原生应用数量突破150万，覆盖主流应用场景，生态建设进入快车道。',
        'event_type': '产品发布',
        'key_numbers': ['150万'],
        'entities': ['华为'],
        'impact_score': 83,
        'relevance_score': 78
    },
    {
        'title': '拼多多海外版Temu宣布进军欧洲市场',
        'url': 'https://www.example.com/pdd-temu',
        'source': '虎嗅',
        'published': datetime.now(),
        'summary': '拼多多旗下跨境电商平台Temu正式宣布进入欧洲市场，首批在5个国家上线，延续低价策略快速扩张。',
        'event_type': '战略扩张',
        'key_numbers': ['5个'],
        'entities': ['拼多多', 'Temu'],
        'impact_score': 74,
        'relevance_score': 68
    },
    {
        'title': '美团Q4财报：外卖业务增长放缓，即时零售成新引擎',
        'url': 'https://www.example.com/meituan-q4',
        'source': '晚点LatePost',
        'published': datetime.now(),
        'summary': '美团发布Q4财报，传统外卖业务增速放缓至15%，即时零售业务增长50%成为新的增长引擎。',
        'event_type': '财报业绩',
        'key_numbers': ['15%', '50%'],
        'entities': ['美团'],
        'impact_score': 71,
        'relevance_score': 66
    },
    {
        'title': '百度文心一言用户突破2亿，推出企业定制版',
        'url': 'https://www.example.com/baidu-ernie',
        'source': '钛媒体',
        'published': datetime.now(),
        'summary': '百度宣布文心一言累计用户突破2亿，同时推出面向企业客户的定制化版本，强化B端服务能力。',
        'event_type': '产品发布',
        'key_numbers': ['2亿'],
        'entities': ['百度'],
        'impact_score': 68,
        'relevance_score': 62
    }
]


def generate_liurun_style_topics(events):
    """生成刘润风格选题"""

    # 类刘润风格筛选标准
    scored = []
    for event in events:
        score = 0

        # 微观性: 有具体数据
        if event.get('key_numbers'):
            score += min(len(event['key_numbers']) * 5, 20)

        # 深度性: 财报/组织调整类事件
        if event['event_type'] in ['财报业绩', '组织调整', '战略调整']:
            score += 25

        # 启发性: 高影响力事件
        if event.get('impact_score', 0) >= 80:
            score += 25

        # 素材性: 有详细摘要
        if len(event.get('summary', '')) > 50:
            score += 15

        scored.append({**event, 'liurun_score': score})

    # 按评分排序
    scored.sort(key=lambda x: x.get('liurun_score', 0), reverse=True)

    # 生成选题
    topics = []
    for event in scored[:3]:
        topic_name = generate_topic_name(event)
        reason = generate_reason(event)
        angles = generate_angles(event)

        topics.append({
            'topic_name': topic_name,
            'core_event': event['title'],
            'event_type': event['event_type'],
            'source': event['source'],
            'url': event['url'],
            'recommendation_reason': reason,
            'writing_angles': angles,
            'key_data': event.get('key_numbers', []),
            'liurun_score': event.get('liurun_score', 0)
        })

    return topics


def generate_topic_name(event):
    """生成刘润风格选题名称"""
    title = event['title']
    entities = event.get('entities', [])
    event_type = event['event_type']

    if event_type == '财报业绩':
        if '比亚迪' in title:
            return '从比亚迪300万辆看懂中国新能源车的"规模之战"'
        elif '美团' in title:
            return '从美团Q4财报看懂即时零售的崛起逻辑'

    elif event_type == '产品发布':
        if '英伟达' in title or 'Nvidia' in title:
            return '从英伟达H200看懂AI算力的"军备竞赛"'
        elif 'OpenAI' in title:
            return '从GPT-4.5降价看懂AI应用的"普及拐点"'
        elif '小米' in title and 'SU7' in title:
            return '从小米SU7的10万订单看懂"造车新逻辑"'

    elif event_type == '组织调整':
        if '理想' in title:
            return '从理想裁员看懂新能源车企的"生存之战"'
        elif '字节跳动' in title:
            return '从字节三裁看懂互联网公司的"效率革命"'

    elif event_type == '战略调整':
        if '蔚来' in title and 'BaaS' in title:
            return '从蔚来降价看懂"车电分离"的商业逻辑'

    # 默认
    if entities:
        return f"从{entities[0]}看懂行业变化背后的商业逻辑"
    return '从事件背后看懂商业逻辑'


def generate_reason(event):
    """生成推荐理由"""
    reasons = []

    if event.get('impact_score', 0) >= 85:
        reasons.append('🔥 行业焦点事件，关注度极高')

    if event.get('key_numbers'):
        reasons.append(f'📊 包含{len(event["key_numbers"])}个关键数据')

    if event.get('entities'):
        important = ['比亚迪', 'Tesla', 'Nvidia', '英伟达', 'OpenAI', '华为', '小米']
        for entity in event['entities']:
            if entity in important:
                reasons.append(f'🏢 {entity}相关')
                break

    if event['event_type'] in ['财报业绩', '组织调整']:
        reasons.append(f'📌 {event["event_type"]}类事件，商业价值高')

    return ' | '.join(reasons) if reasons else '具有观察价值的事件'


def generate_angles(event):
    """生成写作角度"""
    event_type = event['event_type']
    entities = event.get('entities', [])

    if event_type == '财报业绩':
        return {
            '切入点': f'从{entities[0] if entities else "公司"}财报的关键数字变化切入',
            '核心探讨问题': '增长背后的真正驱动力是什么？这种增长可持续吗？',
            '类比案例': '就像看一个人的体检报告，数字背后是企业的健康状态',
            '潜在启发': '理解财务数据背后的商业逻辑和行业趋势'
        }
    elif event_type == '产品发布':
        return {
            '切入点': f'从{entities[0] if entities else "公司"}新品的功能特性切入',
            '核心探讨问题': '这个产品解决了什么问题？反映了什么行业趋势？',
            '类比案例': '就像智能手机取代功能机，产品创新往往预示着时代变革',
            '潜在启发': '理解产品创新背后的用户需求变化和技术趋势'
        }
    elif event_type == '组织调整':
        return {
            '切入点': f'从{entities[0] if entities else "公司"}组织变动的具体举措切入',
            '核心探讨问题': '企业为什么在这个时候做组织调整？',
            '类比案例': '就像园丁修剪树枝，短期的痛是为了长期的生长',
            '潜在启发': '理解企业生命周期中的必经阶段和应对之道'
        }
    else:
        return {
            '切入点': '从事件中的具体场景/细节切入',
            '核心探讨问题': '这个事件反映了什么深层逻辑？',
            '类比案例': '用生活中的类似现象类比',
            '潜在启发': '给读者带来新的认知视角'
        }


def print_report(events, topics):
    """打印报告"""

    print("\n" + "=" * 70)
    print("📊 刘润公众号选题智能体 - 报告摘要")
    print("=" * 70)
    print(f"\n📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📈 总计事件: {len(events)}")

    # 事件类型统计
    type_counts = {}
    for e in events:
        t = e['event_type']
        type_counts[t] = type_counts.get(t, 0) + 1

    print(f"\n   事件类型分布:")
    for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {t}: {count}")

    # Top 5 事件
    print(f"\n🔥 Top 5 事件:")
    for i, event in enumerate(events[:5], 1):
        print(f"   {i}. [{event['event_type']}] {event['title'][:50]}...")
        print(f"      来源: {event['source']} | 影响力: {event['impact_score']}")

    # Top 3 选题
    print(f"\n✨ Top 3 选题推荐:")
    print("=" * 70)

    for i, topic in enumerate(topics, 1):
        print(f"\n{'=' * 70}")
        print(f"## 选题 {i}: {topic['topic_name']}")
        print(f"{'=' * 70}")
        print(f"\n**核心事件**: {topic['core_event']}")
        print(f"**事件类型**: {topic['event_type']}")
        print(f"**来源**: {topic['source']}")
        print(f"\n**推荐理由**: {topic['recommendation_reason']}")
        print(f"**刘润适配度**: {topic['liurun_score']:.0f}/100")

        if topic.get('key_data'):
            print(f"\n**关键数据**: {', '.join(topic['key_data'])}")

        print(f"\n**📝 写作角度**:")
        angles = topic['writing_angles']
        print(f"   • 切入点: {angles['切入点']}")
        print(f"   • 核心探讨问题: {angles['核心探讨问题']}")
        print(f"   • 类比案例: {angles['类比案例']}")
        print(f"   • 潜在启发: {angles['潜在启发']}")

        print(f"\n**参考链接**: {topic['url']}")

    print("\n" + "=" * 70)
    print("✨ 报告生成完成！")
    print("=" * 70)


if __name__ == "__main__":
    print("🚀 刘润公众号选题智能体 - 演示版")
    print("   (使用模拟数据展示功能)")

    # 生成选题
    topics = generate_liurun_style_topics(MOCK_EVENTS)

    # 打印报告
    print_report(MOCK_EVENTS, topics)
