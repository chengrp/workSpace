#!/usr/bin/env python3
"""
Life Reset Coach - 一日人生重启辅导助手

基于 Dan Koe 的深度心理学框架，提供交互式反思辅导。

使用方法:
    python coach.py              # 启动辅导模式
    python coach.py --card       # 抽取一个问题卡片
    python coach.py --full       # 完整一日反思模式
    python coach.py --daily      # 每日提醒模式
"""

import json
import random
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class LifeResetCoach:
    """人生重启辅导助手"""

    def __init__(self):
        self.cards_file = Path(__file__).parent / "cards.json"
        self.data = self._load_cards()
        self.session_log = []

    def _load_cards(self) -> Dict:
        """加载问题卡片数据"""
        if not self.cards_file.exists():
            print(f"错误: 找不到问题卡片文件 {self.cards_file}")
            sys.exit(1)
        with open(self.cards_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_session(self, category: str, question: str, answer: str):
        """保存会话记录"""
        log_dir = Path.home() / ".life-reset" / "sessions"
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = log_dir / f"{timestamp}.md"

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## {category}\n\n")
            f.write(f"**问题**: {question}\n\n")
            f.write(f"**回答**: {answer}\n\n")
            f.write("---\n")

        print(f"\n✓ 已保存到: {log_file}")

    def draw_card(self, category: Optional[str] = None) -> Dict:
        """抽取一个问题卡片"""
        if category:
            if category not in self.data["categories"]:
                print(f"错误: 分类 '{category}' 不存在")
                print(f"可选分类: {', '.join(self.data['categories'].keys())}")
                sys.exit(1)
            categories = {category: self.data["categories"][category]}
        else:
            categories = self.data["categories"]

        # 随机选择分类和问题
        cat_name = random.choice(list(categories.keys()))
        cat_data = categories[cat_name]
        question = random.choice(cat_data["questions"])

        return {
            "category": cat_name,
            "category_desc": cat_data["description"],
            "question": question
        }

    def display_card(self, card: Dict):
        """显示问题卡片"""
        print("\n" + "="*60)
        print(f"📚 分类: {card['category']}")
        print(f"   {card['category_desc']}")
        print("="*60)
        print(f"\n💭 问题:\n")
        print(f"   {card['question']['question']}\n")

        if "followup" in card["question"]:
            print(f"💡 深入思考:\n")
            print(f"   {card['question']['followup']}\n")

        if "prompts" in card["question"]:
            print(f"📝 引导提示:\n")
            for prompt in card["question"]["prompts"]:
                print(f"   • {prompt}")
            print()

        print(f"⏱ 建议反思时间: {card['question'].get('reflection_time', '5-10分钟')}")
        print("="*60)

    def interactive_mode(self):
        """交互式辅导模式"""
        print("\n🌟 Life Reset Coach - 一日人生重启辅导助手")
        print("="*60)
        print("\n选择模式:")
        print("  1. 抽取问题卡片")
        print("  2. 完整一日反思 (早上/全天/晚上)")
        print("  3. 每日提醒模式")
        print("  4. 查看所有分类")
        print("  0. 退出")

        while True:
            choice = input("\n请选择 (0-4): ").strip()

            if choice == "0":
                print("\n再见！祝你反思愉快！")
                break
            elif choice == "1":
                self._card_mode()
            elif choice == "2":
                self._full_session_mode()
            elif choice == "3":
                self._daily_reminder_mode()
            elif choice == "4":
                self._list_categories()
            else:
                print("无效选择，请重新输入")

    def _card_mode(self):
        """问题卡片模式"""
        print("\n--- 问题卡片模式 ---")
        print("选择分类 (留空随机):")
        for i, cat_name in enumerate(self.data["categories"].keys(), 1):
            print(f"  {i}. {cat_name}")
        print("  0. 随机")

        choice = input("\n请选择: ").strip()

        if choice == "0" or choice == "":
            category = None
        else:
            try:
                cat_idx = int(choice) - 1
                category = list(self.data["categories"].keys())[cat_idx]
            except (ValueError, IndexError):
                print("无效选择，使用随机模式")
                category = None

        card = self.draw_card(category)
        self.display_card(card)

        # 询问是否记录回答
        record = input("\n是否记录你的回答？(y/n): ").strip().lower()
        if record == 'y':
            answer = input("\n你的回答: ").strip()
            self._save_session(card["category"], card["question"]["question"], answer)

    def _full_session_mode(self):
        """完整一日反思模式"""
        print("\n--- 完整一日反思模式 ---")
        print("\n选择时段:")
        print("  1. 🌅 早上 - 心理挖掘")
        print("  2. ☀️ 全天 - 打断自动驾驶")
        print("  3. 🌙 晚上 - 综合洞察")
        print("  0. 返回")

        choice = input("\n请选择: ").strip()

        if choice == "1":
            self._morning_session()
        elif choice == "2":
            self._daily_interruption()
        elif choice == "3":
            self._evening_session()
        elif choice == "0":
            return
        else:
            print("无效选择")

    def _morning_session(self):
        """早上 - 心理挖掘"""
        print("\n🌅 早上：心理挖掘")
        print("="*60)
        print("\n【第一步】揭示当前痛苦 (15分钟)")
        print("\n请准备纸笔，诚实地回答以下问题...")
        print("(按回车继续)")
        input()

        questions = self.data["categories"]["自我觉察"]["questions"]
        for i, q in enumerate(questions[:4], 1):
            print(f"\n问题 {i}: {q['question']}")
            if "followup" in q:
                print(f"深入: {q['followup']}")
            print("\n请写下你的答案...")
            input("(完成后按回车继续)")

        print("\n" + "="*60)
        print("\n【第二步】创建反愿景 (15分钟)")
        input("(按回车继续)")

        av_questions = self.data["categories"]["反愿景"]["questions"]
        for i, q in enumerate(av_questions[:4], 1):
            print(f"\n问题 {i}: {q['question']}")
            if "prompts" in q:
                for p in q["prompts"]:
                    print(f"  • {p}")
            print("\n请写下你的答案...")
            input("(完成后按回车继续)")

        print("\n" + "="*60)
        print("\n【第三步】创建愿景 (15分钟)")
        input("(按回车继续)")

        v_questions = self.data["categories"]["愿景"]["questions"]
        for i, q in enumerate(v_questions, 1):
            print(f"\n问题 {i}: {q['question']}")
            if "note" in q:
                print(f"注意: {q['note']}")
            print("\n请写下你的答案...")
            input("(完成后按回车继续)")

        print("\n✅ 早上心理挖掘完成！")
        print("\n接下来，请在全天使用提醒模式，打破无意识模式。")

    def _daily_interruption(self):
        """全天 - 打断自动驾驶"""
        print("\n☀️ 全天：打断自动驾驶")
        print("="*60)
        print("\n以下是全天定时提醒问题：")
        print("\n建议设置以下时间的提醒：\n")

        reminders = [
            ("上午11:00", "我现在通过正在做的事在逃避什么？"),
            ("下午1:30", "如果有有人拍下过去两个小时，他们会得出什么结论？"),
            ("下午3:15", "我是在向我讨厌的生活还是我想要的生活推进？"),
            ("下午5:00", "什么是我假装不重要最重要的事？"),
            ("晚上7:30", "我今天做什么是出于身份保护而不是真正的欲望？"),
            ("晚上9:00", "今天什么时候我感觉最 alive？什么时候感觉最死？"),
        ]

        for time, question in reminders:
            print(f"  {time}: {question}")

        print("\n" + "="*60)
        print("\n💡 建议在手机日历或闹钟中设置这些提醒")
        print("\n【额外反思】(通勤/散步时):")
        extra = [
            "如果我不再需要人们把我看作【某个身份】，会发生什么？",
            "在我的生活中，我在哪里用活力换取了安全？",
            "我想成为的那个人的最小版本的什么，我明天就可以成为？"
        ]
        for q in extra:
            print(f"  • {q}")

    def _evening_session(self):
        """晚上 - 综合洞察"""
        print("\n🌙 晚上：综合洞察")
        print("="*60)
        print("\n请回想今天的反思，回答以下问题...\n")

        print("【综合反思】")
        questions = [
            "今天之后，关于你为什么一直被困住，什么感觉最真实？",
            "真正的敌人是什么？（清楚地命名它）",
            "写一句话概括你拒绝让你的生活变成什么",
            "写一句话概括你正在建设什么"
        ]

        for i, q in enumerate(questions, 1):
            print(f"\n问题 {i}: {q}")
            print("\n请写下你的答案...")
            input("(完成后按回车继续)")

        print("\n" + "="*60)
        print("\n【创建时间透镜目标】")
        print("\n记住：目标是透镜/观点，不是终点线\n")

        lenses = [
            ("一年透镜", "一年内什么必须为真，你才能知道你打破了旧的模式？"),
            ("一个月透镜", "一个月内什么必须为真，才能让一年透镜保持可能？"),
            ("每日透镜", "明天你可以时间阻塞的2-3个行动是什么？")
        ]

        for lens, question in lenses:
            print(f"\n{lens}: {question}")
            print("\n请写下你的答案...")
            input("(完成后按回车继续)")

        print("\n✅ 晚上综合洞察完成！")
        print("\n" + "="*60)
        print("\n🎮 六要素生活游戏")
        print("\n将你今天的洞察整理成六个部分：")
        print("  1. 反愿景 - 什么是我的存在之痛？")
        print("  2. 愿景 - 什么是理想的我要的生活？")
        print("  3. 一年目标 - 一年后我的生活会是什么样的？")
        print("  4. 一个月项目 - 我需要学什么/做什么？")
        print("  5. 每日杠杆 - 每天最重要的2-3件事")
        print("  6. 约束 - 我绝不妥协的底线是什么？")
        print("\n把这六点写在显眼的地方，每天查看！")

    def _daily_reminder_mode(self):
        """每日提醒模式"""
        print("\n📅 每日提醒模式")
        print("="*60)

        reminder = random.choice(self.data["daily_reminders"])
        print(f"\n今日反思问题:\n")
        print(f"  {reminder}\n")
        print("="*60)

    def _list_categories(self):
        """列出所有分类"""
        print("\n📚 问题卡片分类:\n")
        for name, data in self.data["categories"].items():
            print(f"  {name}:")
            print(f"    {data['description']}")
            print(f"    问题数量: {len(data['questions'])}")
            print()


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="Life Reset Coach - 一日人生重启辅导助手")
    parser.add_argument("--card", action="store_true", help="抽取一个问题卡片")
    parser.add_argument("--category", type=str, help="指定问题分类")
    parser.add_argument("--full", action="store_true", help="完整一日反思模式")
    parser.add_argument("--daily", action="store_true", help="每日提醒模式")

    args = parser.parse_args()

    coach = LifeResetCoach()

    if args.card:
        card = coach.draw_card(args.category)
        coach.display_card(card)
    elif args.daily:
        coach._daily_reminder_mode()
    elif args.full:
        coach._full_session_mode()
    else:
        coach.interactive_mode()


if __name__ == "__main__":
    main()
