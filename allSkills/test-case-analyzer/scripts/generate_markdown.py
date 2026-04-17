"""
Markdown 测试用例生成器
"""

import os
from datetime import datetime
from typing import Dict, List, Any


class MarkdownGenerator:
    """Markdown 测试用例生成器"""

    def __init__(self, template_dir="../templates"):
        self.template_dir = template_dir

    def generate(self, analysis_result: Dict[str, Any], output_path: str) -> str:
        """
        生成 Markdown 测试用例文档

        Args:
            analysis_result: 需求分析结果
            output_path: 输出文件路径

        Returns:
            生成的 Markdown 内容
        """
        lines = []

        # 标题
        title = analysis_result.get("summary", {}).get("title", "未命名需求")
        lines.append(f"# {title} - 测试用例\n")
        lines.append(f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"> **分析方法**: 五维度需求分析框架\n")
        lines.append("---\n\n")

        # 需求分析摘要
        lines.append("## 📋 需求分析摘要\n\n")
        lines.append("### 核心功能\n")
        for func in analysis_result.get("summary", {}).get("core_functions", []):
            lines.append(f"- {func}")
        lines.append("\n")

        # 关键规则
        lines.append("### 关键规则\n")
        lines.append("| 规则类型 | 描述 |\n")
        lines.append("|----------|------|\n")

        # 核心要素
        for trigger in analysis_result.get("core_elements", {}).get("trigger_conditions", []):
            lines.append(f"| 触发条件 | {trigger[:50]}... |\n")

        # 计时条件
        for timing in analysis_result.get("core_elements", {}).get("timing_conditions", []):
            lines.append(f"| 计时条件 | {timing['value']}{timing['unit']} |\n")
        lines.append("\n")

        # 测试用例
        lines.append("## 🧪 测试用例\n\n")

        # 按类型分组
        test_cases_by_type = {}
        for tc in analysis_result.get("test_cases", []):
            tc_type = tc.get("type", "其他")
            if tc_type not in test_cases_by_type:
                test_cases_by_type[tc_type] = []
            test_cases_by_type[tc_type].append(tc)

        # 类型映射
        type_names = {
            "功能测试": "1. 功能测试",
            "边界值测试": "2. 边界值测试",
            "并发测试": "3. 并发测试",
            "状态测试": "4. 状态流转测试",
            "回归测试": "5. 回归测试",
            "交互测试": "6. 前端交互测试",
            "配置测试": "7. 配置测试",
        }

        for tc_type, cases in test_cases_by_type.items():
            type_name = type_names.get(tc_type, tc_type)
            lines.append(f"### {type_name}\n\n")

            # 表格头
            lines.append("| 用例ID | 标题 | 优先级 | 前置条件 | 测试步骤 | 预期结果 |\n")
            lines.append("|--------|------|--------|----------|----------|----------|\n")

            for tc in cases:
                steps = "\n".join(tc.get("steps", []))
                lines.append(f"| {tc['id']} | {tc['title'][:30]} | {tc['priority']} | - | {steps[:50]}... | {tc.get('expected', '')[:30]}... |\n")
            lines.append("\n")

        # 待确认事项
        questions = analysis_result.get("questions_to_confirm", [])
        if questions:
            lines.append("## ❓ 待确认事项\n\n")
            for i, q in enumerate(questions, 1):
                lines.append(f"{i}. {q}\n")
            lines.append("\n")

        # 测试范围评估
        lines.append("## 📊 测试范围评估\n\n")
        lines.append("| 测试类型 | 用例数 | 说明 |\n")
        lines.append("|----------|--------|------|\n")
        for tc_type, cases in test_cases_by_type.items():
            lines.append(f"| {tc_type} | {len(cases)} | 覆盖核心场景 |\n")
        lines.append("\n")

        # 最佳实践提醒
        lines.append("## 💡 测试建议\n\n")
        lines.append("### 执行顺序\n")
        lines.append("1. 先执行 P0 优先级用例\n")
        lines.append("2. 功能测试 → 边界值测试 → 异常测试\n")
        lines.append("3. 最后执行回归测试\n\n")

        lines.append("### 注意事项\n")
        lines.append("- 时间相关用例注意计时精度\n")
        lines.append("- 并发用例需要模拟真实场景\n")
        lines.append("- 状态测试关注状态流转完整性\n")

        content = "".join(lines)

        # 写入文件
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return content


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python generate_markdown.py <analysis.json> <output.md>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    generator = MarkdownGenerator()
    output = sys.argv[2] if len(sys.argv) > 2 else "output/test_cases.md"
    result = generator.generate(analysis, output)

    print(f"✅ Markdown 已生成: {output}")
