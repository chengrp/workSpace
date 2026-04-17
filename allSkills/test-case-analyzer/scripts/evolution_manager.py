"""
进化管理器 - 学习与反馈机制
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any


class EvolutionManager:
    """学习进化管理器"""

    def __init__(self, evolution_file="../evolution.json"):
        self.evolution_file = evolution_file
        self.data = self._load_evolution()

    def _load_evolution(self) -> Dict:
        """加载进化数据"""
        try:
            with open(self.evolution_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "version": "1.0.0",
                "last_updated": datetime.now().isoformat(),
                "patterns": {},
                "user_corrections": [],
                "learned_insights": {}
            }

    def _save_evolution(self) -> None:
        """保存进化数据"""
        self.data["last_updated"] = datetime.now().isoformat()
        with open(self.evolution_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def record_feedback(self, requirement_type: str, feedback: Dict[str, Any]) -> None:
        """
        记录用户反馈

        Args:
            requirement_type: 需求类型（如 "电商订单超时"）
            feedback: 反馈数据
        """
        correction = {
            "date": datetime.now().isoformat(),
            "requirement_type": requirement_type,
            "coverage": feedback.get("coverage", []),
            "accuracy": feedback.get("accuracy", []),
            "usability": feedback.get("usability", [])
        }

        self.data["user_corrections"].append(correction)
        self._save_evolution()

    def learn_patterns(self, requirement_text: str, missed_scenarios: List[str]) -> None:
        """
        学习遗漏的测试场景

        Args:
            requirement_text: 需求文本
            missed_scenarios: 遗漏的场景列表
        """
        # 识别需求类型
        req_type = self._identify_requirement_type(requirement_text)

        if req_type and req_type not in self.data["patterns"]:
            self.data["patterns"][req_type] = {
                "missed_scenarios": [],
                "auto_add": True,
                "priority_keywords": []
            }

        if req_type:
            pattern = self.data["patterns"][req_type]
            pattern["missed_scenarios"].extend(missed_scenarios)
            # 去重
            pattern["missed_scenarios"] = list(set(pattern["missed_scenarios"]))
            self._save_evolution()

    def _identify_requirement_type(self, text: str) -> str:
        """识别需求类型"""
        # 基于关键词匹配
        keywords_map = {
            "订单超时": ["订单", "超时", "关闭", "支付"],
            "库存管理": ["库存", "商品", "购买"],
            "支付流程": ["支付", "金额", "回调"],
            "用户权限": ["权限", "角色", "访问"],
            "状态流转": ["状态", "流转", "变更"]
        }

        for req_type, keywords in keywords_map.items():
            if any(kw in text for kw in keywords):
                return req_type

        return "通用"

    def get_suggestions(self, requirement_text: str) -> List[str]:
        """
        基于学习数据获取建议

        Args:
            requirement_text: 需求文本

        Returns:
            建议列表
        """
        suggestions = []
        req_type = self._identify_requirement_type(requirement_text)

        # 从模式中获取建议
        for pattern_name, pattern in self.data["patterns"].items():
            # 检查关键词匹配
            keywords = pattern.get("priority_keywords", [])
            if not keywords or any(kw in requirement_text for kw in keywords):
                for scenario in pattern.get("missed_scenarios", []):
                    if scenario not in suggestions:
                        suggestions.append(scenario)

        return suggestions

    def summarize_learnings(self) -> Dict[str, Any]:
        """
        总结学习到的经验

        Returns:
            学习总结
        """
        summary = {
            "total_corrections": len(self.data["user_corrections"]),
            "patterns_learned": len(self.data["patterns"]),
            "insights": self.data.get("learned_insights", {}),
            "recent_corrections": self.data["user_corrections"][-5:]  # 最近5次
        }

        return summary

    def evolve(self, new_insights: Dict[str, str]) -> None:
        """
        进化 - 整合新学到的经验

        Args:
            new_insights: 新学到的经验
        """
        self.data["learned_insights"].update(new_insights)
        self._save_evolution()


def collect_user_feedback() -> Dict[str, List[str]]:
    """
    收集用户反馈（交互式）

    Returns:
        反馈数据
    """
    feedback = {
        "coverage": [],
        "accuracy": [],
        "usability": []
    }

    print("\n📝 反馈收集（帮助我们改进）")
    print("=" * 40)

    # 覆盖率
    print("\n1️⃣ 覆盖率 - 是否遗漏了重要测试场景？")
    print("   （输入遗漏的场景，一行一个，空行结束）")
    while True:
        line = input("   > ").strip()
        if not line:
            break
        feedback["coverage"].append(line)

    # 准确性
    print("\n2️⃣ 准确性 - 测试用例描述是否准确反映了需求？")
    print("   （输入不准确的地方，空行结束）")
    while True:
        line = input("   > ").strip()
        if not line:
            break
        feedback["accuracy"].append(line)

    # 可用性
    print("\n3️⃣ 可用性 - 测试步骤是否清晰可执行？")
    print("   （输入需要改进的地方，空行结束）")
    while True:
        line = input("   > ").strip()
        if not line:
            break
        feedback["usability"].append(line)

    return feedback


if __name__ == "__main__":
    import sys

    manager = EvolutionManager()

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # 测试模式
        manager.learn_patterns("订单超时30分钟自动关闭", [
            "边界值：29分59秒支付",
            "并发：支付与关闭同时发生"
        ])

        suggestions = manager.get_suggestions("订单超时30分钟自动关闭")
        print("建议：", suggestions)

        summary = manager.summarize_learnings()
        print("总结：", json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("进化管理器")
        print("用法: python evolution_manager.py --test")
