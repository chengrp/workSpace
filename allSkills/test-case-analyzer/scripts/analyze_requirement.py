"""
需求分析引擎 - 基于五维度分析框架
"""

import re
import json
from typing import Dict, List, Any
from datetime import datetime


class RequirementAnalyzer:
    """需求分析器"""

    def __init__(self, evolution_file="../evolution.json"):
        self.evolution_file = evolution_file
        self.patterns = self._load_patterns()

    def _identify_requirement_type(self, text: str) -> str:
        """
        识别需求类型（支持自动学习和模式匹配）

        Args:
            text: 需求文本

        Returns:
            需求类型
        """
        # 首先从学习的模式中匹配
        if "requirement_patterns" in self.patterns:
            for req_type, pattern_info in self.patterns["requirement_patterns"].items():
                keywords = pattern_info.get("keywords", [])
                match_count = sum(1 for kw in keywords if kw in text)
                if match_count >= 2:  # 至少匹配2个关键词
                    return req_type

        # 默认关键词匹配
        keywords_map = {
            "订单超时": ["订单", "超时", "关闭", "支付", "自动"],
            "库存管理": ["库存", "商品", "购买", "扣减", "释放"],
            "支付流程": ["支付", "金额", "回调", "异步", "同步"],
            "用户权限": ["权限", "角色", "访问", "控制", "登录"],
            "状态流转": ["状态", "流转", "变更", "转换", "触发"],
            "金融交易": ["转账", "金额", "账户", "余额", "交易"],
        }

        best_match = None
        best_score = 0

        for req_type, keywords in keywords_map.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_match = req_type

        return best_match if best_match else "通用"

    def _load_patterns(self) -> Dict:
        """加载学习到的模式"""
        try:
            with open(self.evolution_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "patterns": {},
                "user_corrections": []
            }

    def analyze(self, requirement_text: str) -> Dict[str, Any]:
        """
        分析需求文档

        Args:
            requirement_text: 需求文档文本

        Returns:
            分析结果字典
        """
        result = {
            "summary": self._extract_summary(requirement_text),
            "core_elements": self._analyze_core_elements(requirement_text),
            "conditions": self._analyze_conditions(requirement_text),
            "expected_results": self._analyze_expected_results(requirement_text),
            "exceptions": self._analyze_exceptions(requirement_text),
            "dependencies": self._analyze_dependencies(requirement_text),
            "questions_to_confirm": self._generate_questions(requirement_text),
            "test_cases": []
        }

        # 生成测试用例
        result["test_cases"] = self._generate_test_cases(result)

        return result

    def _extract_summary(self, text: str) -> Dict:
        """提取需求摘要"""
        # 提取标题
        title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
        title = title_match.group(1) if title_match else "未命名需求"

        # 提取核心功能
        lines = text.split('\n')
        core_functions = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                core_functions.append(line[:100])
                if len(core_functions) >= 3:
                    break

        return {
            "title": title,
            "core_functions": core_functions,
            "text_length": len(text)
        }

    def _analyze_core_elements(self, text: str) -> Dict:
        """分析核心要素和业务流程"""
        elements = {
            "trigger_conditions": [],
            "timing_conditions": [],
            "business_flow": []
        }

        # 触发条件关键词
        trigger_keywords = ['用户', '下单', '提交', '触发', '启动', '当', '如果']
        for keyword in trigger_keywords:
            if keyword in text:
                # 提取相关句子
                sentences = re.split(r'[。！？\n]', text)
                for sent in sentences:
                    if keyword in sent:
                        elements["trigger_conditions"].append(sent.strip())

        # 时间条件
        time_pattern = r'(\d+)\s*(分钟|小时|秒|分|时|天)'
        time_matches = re.findall(time_pattern, text)
        for match in time_matches:
            elements["timing_conditions"].append({
                "value": match[0],
                "unit": match[1]
            })

        return elements

    def _analyze_conditions(self, text: str) -> Dict:
        """分析判断和执行条件"""
        conditions = {
            "execution_actions": [],
            "judgment_timing": [],
            "implementation_method": []
        }

        # 执行动作
        action_keywords = ['关闭', '取消', '释放', '删除', '发送', '通知']
        for keyword in action_keywords:
            if keyword in text:
                sentences = re.split(r'[。！？\n]', text)
                for sent in sentences:
                    if keyword in sent:
                        conditions["execution_actions"].append(sent.strip())

        return conditions

    def _analyze_expected_results(self, text: str) -> Dict:
        """分析预期结果"""
        results = {
            "state_changes": [],
            "data_changes": [],
            "user_perception": []
        }

        # 状态变化
        state_keywords = ['状态', '变为', '变成', '转为']
        for keyword in state_keywords:
            if keyword in text:
                sentences = re.split(r'[。！？\n]', text)
                for sent in sentences:
                    if keyword in sent:
                        results["state_changes"].append(sent.strip())

        # 用户感知
        user_keywords = ['用户', '收到', '看到', '提示', '通知']
        for keyword in user_keywords:
            if keyword in text:
                sentences = re.split(r'[。！？\n]', text)
                for sent in sentences:
                    if keyword in sent:
                        results["user_perception"].append(sent.strip())

        return results

    def _analyze_exceptions(self, text: str) -> Dict:
        """分析异常流程"""
        exceptions = {
            "boundary_values": [],
            "concurrency": [],
            "business_interaction": []
        }

        # 边界值
        if '30' in text or '边界' in text:
            exceptions["boundary_values"].append("时间边界值测试")

        # 并发
        if '同时' in text or '并发' in text:
            exceptions["concurrency"].append("并发操作测试")

        return exceptions

    def _analyze_dependencies(self, text: str) -> Dict:
        """分析外部依赖和配置"""
        dependencies = {
            "configurable_items": [],
            "external_services": [],
            "special_scenarios": []
        }

        # 可配置项
        if '配置' in text or '可调' in text:
            dependencies["configurable_items"].append("时间参数可配置")

        return dependencies

    def _generate_questions(self, text: str) -> List[str]:
        """生成待确认问题"""
        questions = []

        # 计时相关问题
        if '分钟' in text or '秒' in text:
            questions.append("计时单位是分钟还是秒？")

        if '分钟' in text:
            questions.append("计时实现方式（定时任务轮询 / 消息队列延迟处理）？")

        # 并发问题
        if '同时' in text or '关闭' in text:
            questions.append("并发处理机制如何保证？")

        # 状态问题
        if '状态' in text:
            questions.append("状态流转规则是什么？")

        return questions

    def _generate_test_cases(self, analysis: Dict) -> List[Dict]:
        """生成测试用例（支持模式自动匹配）"""
        test_cases = []
        case_id = 1

        # 获取需求类型以匹配模式
        req_type = self._identify_requirement_type(analysis.get("summary", {}).get("title", ""))

        # 从学习模式中获取额外测试场景
        learned_scenarios = self._get_learned_scenarios(req_type)

        # 1. 功能测试
        for action in analysis["conditions"]["execution_actions"]:
            test_cases.append({
                "id": f"TC-F-{case_id:03d}",
                "type": "功能测试",
                "title": action[:50],
                "priority": "P1",
                "steps": ["1. 执行前置条件", f"2. {action}", "3. 验证结果"],
                "expected": action
            })
            case_id += 1

        # 2. 边界值测试
        for exception in analysis["exceptions"]["boundary_values"]:
            test_cases.append({
                "id": f"TC-B-{case_id:03d}",
                "type": "边界值测试",
                "title": exception,
                "priority": "P1",
                "steps": ["1. 设置边界条件", "2. 执行操作", "3. 验证结果"],
                "expected": "系统正确处理边界值"
            })
            case_id += 1

        # 3. 并发测试
        for exception in analysis["exceptions"]["concurrency"]:
            test_cases.append({
                "id": f"TC-C-{case_id:03d}",
                "type": "并发测试",
                "title": exception,
                "priority": "P0",
                "steps": ["1. 模拟并发操作", "2. 同时执行多个操作", "3. 验证数据一致性"],
                "expected": "系统正确处理并发，数据一致"
            })
            case_id += 1

        # 4. 从学习模式中添加额外测试场景
        for scenario in learned_scenarios:
            test_cases.append({
                "id": f"TC-L-{case_id:03d}",
                "type": "回归测试",
                "title": f"[学习] {scenario}",
                "priority": "P1",
                "steps": ["1. 设置场景条件", f"2. {scenario}", "3. 验证结果"],
                "expected": "系统按预期处理"
            })
            case_id += 1

        # 5. 状态测试（如果有状态变化）
        if analysis["expected_results"]["state_changes"]:
            test_cases.append({
                "id": f"TC-S-{case_id:03d}",
                "type": "状态测试",
                "title": "状态流转测试",
                "priority": "P1",
                "steps": ["1. 初始状态", "2. 触发状态变更", "3. 验证新状态"],
                "expected": "状态正确流转"
            })
            case_id += 1

        return test_cases

    def _get_learned_scenarios(self, req_type: str) -> List[str]:
        """从学习模式中获取测试场景"""
        scenarios = []

        if "requirement_patterns" in self.patterns:
            pattern = self.patterns["requirement_patterns"].get(req_type, {})
            scenarios = pattern.get("test_scenarios", [])

        return scenarios


# CLI 接口
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python analyze_requirement.py <requirement_file>")
        sys.exit(1)

    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()

    analyzer = RequirementAnalyzer()
    result = analyzer.analyze(text)

    print(json.dumps(result, ensure_ascii=False, indent=2))
